"""Tracking of the datasets read while an attribute is built.

``sources.md`` cites, for every attribute, only the datasets that were read to
calculate it:

1. ``Element._build_attribute`` opens a record for each attribute it builds.
2. Reading a dataset from a collection (``self.data["<name>"]``) adds it to the
   record of the attribute being built.
3. ``SourceInformation`` keeps the record that was open when it was created and
   cites only the datasets in it, see ``SourceInformation.cited_metadata``.

A cache returns its value without reading the datasets again. A cache in a
dataset collection therefore stores the datasets read for its value and adds
them to the record on every call: ``instance_cache`` does this, and
``DatasetCollection`` applies the same to each ``functools.cached_property`` it
defines and rejects ``functools.cache`` and ``functools.lru_cache``.
"""

from __future__ import annotations

import functools
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, TypeVar, cast

if TYPE_CHECKING:
    from .datasets.metadata import MetaData, MetadataTree

F = TypeVar("F", bound=Callable[..., Any])

# the metadata of the datasets read, keyed by identity since MetaData is unhashable
Usage = dict[int, "MetaData"]

_usage: ContextVar[Usage | None] = ContextVar("dataset_usage", default=None)


@contextmanager
def track_usage() -> Iterator[Usage]:
    """Record the datasets read inside the block, separately from outer records."""
    usage: Usage = {}
    token = _usage.set(usage)
    try:
        yield usage
    finally:
        _usage.reset(token)


def active_usage() -> Usage | None:
    """The open record, None outside an attribute build."""
    return _usage.get()


def record_usage(metadata: MetadataTree) -> None:
    """Add a dataset, or all datasets of a collection's metadata, to the open
    record."""
    usage = _usage.get()
    if usage is None:
        return
    if isinstance(metadata, dict):
        for sub_metadata in metadata.values():
            record_usage(sub_metadata)
    else:
        usage[id(metadata)] = metadata


# ---------- caches ----------


def _cached(instance: Any, key: tuple, compute: Callable[[], Any]) -> Any:
    """Return the value of `key`, computed once per instance, and add the datasets
    read to compute it to the open record."""
    cache = instance.__dict__.setdefault("_dataset_usage_cache", {})
    if key not in cache:
        with track_usage() as usage:
            value = compute()
        cache[key] = (value, list(usage.values()))
    value, metadata = cache[key]
    for entry in metadata:
        record_usage(entry)
    return value


def instance_cache(method: F) -> F:
    """Memoize a method per instance and arguments, keeping the datasets it reads
    in ``sources.md`` of every attribute that uses the cached value."""

    @functools.wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        key = (method.__name__, args, tuple(sorted(kwargs.items())))
        return _cached(self, key, lambda: method(self, *args, **kwargs))

    return cast(F, wrapper)


class _CachedProperty:
    """``functools.cached_property`` that keeps the datasets it reads in
    ``sources.md`` of every attribute that uses the cached value."""

    def __init__(self, func: Callable[[Any], Any], name: str):
        self.func = func
        self.name = name
        self.__doc__ = func.__doc__

    def __get__(self, instance: Any, owner: type | None = None) -> Any:
        if instance is None:
            return self
        return _cached(instance, (self.name,), lambda: self.func(instance))


def track_caches(cls: type) -> None:
    """Make the caches defined on a dataset collection class record the datasets
    they read.

    Raises:
        TypeError: If a method uses ``functools.cache`` or ``functools.lru_cache``,
            whose cached values would drop the datasets read from ``sources.md``.
    """
    for name, value in list(vars(cls).items()):
        if isinstance(value, functools.cached_property):
            setattr(cls, name, _CachedProperty(value.func, name))
        elif hasattr(getattr(value, "__func__", value), "cache_info"):
            raise TypeError(
                f"'{cls.__name__}.{name}' uses functools.cache or lru_cache, which "
                "hides the datasets it reads from sources.md. Use "
                "zen_creator.instance_cache instead."
            )
