from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier


class TemplateCarrier(Carrier):

    name: str = "template_carrier"

    def __init__(self, model: Model):
        super().__init__(model=model)