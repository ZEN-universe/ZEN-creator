# import difflib
import difflib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# ----------------------------
# JSON DEEP DIFF
# ----------------------------
TOLERANCE = 10**-12


def json_diff(obj1: Any, obj2: Any, path: str = "") -> list[str]:
    diffs: list[str] = []

    if (type(obj1) is not type(obj2)) and not (
        isinstance(obj1, int) and isinstance(obj2, float)  # exclude int -> float
    ):
        diffs.append(f"{path} - Type changed: {type(obj1)} -> {type(obj2)}")
        return diffs

    if isinstance(obj1, dict):
        keys = set(obj1.keys()).union(obj2.keys())
        for key in keys:
            new_path = f"{path}.{key}" if path else key
            if key not in obj1:
                diffs.append(f"{new_path} - Key missing in Tree1")
            elif key not in obj2:
                diffs.append(f"{new_path} - Key missing in Tree2")
            else:
                diffs.extend(json_diff(obj1[key], obj2[key], new_path))

    elif isinstance(obj1, list):
        # If both lists contain only strings, compare as sets
        if all(isinstance(x, str) for x in obj1 + obj2):
            set1, set2 = set(obj1), set(obj2)
            for item in set1 - set2:
                diffs.append(f"{path} - Extra in Tree1: {item}")
            for item in set2 - set1:
                diffs.append(f"{path} - Extra in Tree2: {item}")
        else:
            min_len = min(len(obj1), len(obj2))
            for i in range(min_len):
                diffs.extend(json_diff(obj1[i], obj2[i], f"{path}[{i}]"))
            if len(obj1) > len(obj2):
                diffs.append(f"{path} - Extra items in Tree1")
            elif len(obj2) > len(obj1):
                diffs.append(f"{path} - Extra items in Tree2")

    else:
        # compare numbers to machine precision
        if isinstance(obj1, (int, float, complex)) and isinstance(
            obj2, (int, float, complex)
        ):
            if abs(obj1 - obj2) >= max(abs(obj1), abs(obj2), 1) * TOLERANCE:
                diffs.append(f"{path} - Value changed: {obj1} -> {obj2}")

        elif obj1 != obj2:
            diffs.append(f"{path} - Value changed: {obj1} -> {obj2}")

    return diffs


# ----------------------------
# TEXT DIFF
# ----------------------------


def text_diff(file1: str | Path, file2: str | Path) -> list[str]:
    with open(file1, "r", encoding="utf-8") as f1:
        lines1 = f1.readlines()

    with open(file2, "r", encoding="utf-8") as f2:
        lines2 = f2.readlines()

    diff = difflib.unified_diff(
        lines1, lines2, fromfile=str(file1), tofile=str(file2), lineterm=""
    )
    return list(diff)


# ----------------------------
# CSV DIFF
# ----------------------------


def csv_diff(file1: str | Path, file2: str | Path, tol: float = 1e-10) -> list[str]:

    differences: list[str] = []

    # Load CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Check columns
    if not df1.columns.equals(df2.columns):
        differences.append(
            f"Different columns:\n"
            f"File1: {df1.columns.tolist()}\n"
            f"File2: {df2.columns.tolist()}"
        )
        return differences  # Cannot compare further safely

    # Check shape
    if df1.shape != df2.shape:
        differences.append(f"Different shapes: File1 {df1.shape}, File2 {df2.shape}")
        return differences

    # Compare column-by-column
    for col in df1.columns:
        s1 = df1[col]
        s2 = df2[col]

        # Numeric columns → compare with tolerance
        if pd.api.types.is_numeric_dtype(s1):
            comparison = np.isclose(s1, s2, atol=0, rtol=TOLERANCE, equal_nan=True)
        else:
            comparison = (s1 == s2) | (s1.isna() & s2.isna())

        # Record differences
        diff_indices = np.where(~comparison)[0]
        for idx in diff_indices:
            differences.append(
                f"Row {idx}, Column '{col}': {s1.iloc[idx]} != {s2.iloc[idx]}"
            )

    return differences


# ----------------------------
# FILE COMPARISON
# ----------------------------


def compare_files(file1: Path, file2: Path) -> list[str]:
    ext = file1.suffix.lower()

    if ext == ".json":
        with open(file1, "r", encoding="utf-8") as f1:
            obj1 = json.load(f1)
        with open(file2, "r", encoding="utf-8") as f2:
            obj2 = json.load(f2)

        return json_diff(obj1, obj2)

    if ext == ".csv":
        return csv_diff(file1, file2)

    else:
        # fallback to text diff
        return text_diff(file1, file2)


# ----------------------------
# TREE BUILDING
# ----------------------------


def build_file_map(root: str | Path) -> dict[Path, Path]:
    root = Path(root)
    file_map: dict[Path, Path] = {}
    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(root)
            file_map[rel] = path
    return file_map


# ----------------------------
# MAIN TREE COMPARISON
# ----------------------------


def compare_trees(dir1: str | Path, dir2: str | Path, raise_error: bool = True) -> bool:
    map1 = build_file_map(dir1)
    map2 = build_file_map(dir2)

    all_paths = set(map1.keys()).union(map2.keys())

    is_equal = True

    log: list[str] = []

    for rel_path in sorted(all_paths):
        f1 = map1.get(rel_path)
        f2 = map2.get(rel_path)

        if f1 and not f2:
            diffs = ["Only in Tree1"]
            is_equal = False
        elif f2 and not f1:
            diffs = ["Only in Tree2"]
            is_equal = False
        else:
            assert f1 is not None and f2 is not None
            diffs = compare_files(f1, f2)

        if diffs:
            log.extend([f"\n=== {rel_path} ==="])
            log.extend(diffs)

    # check for differences
    if log:
        log_str = "\n".join(log)
        is_equal = False

        # raise error or print differences
        if raise_error:
            raise AssertionError(
                f"The file trees do not match. \n\n"
                f"Tree 1: {dir1} \n"
                f"Tree 2: {dir2} \n\n"
                f"The following differences were found: \n {log_str}"
            )
        else:
            print(log_str)

    return is_equal


# ----------------------------
# RUN
# ----------------------------

if __name__ == "__main__":
    dir1 = (
        "C:\\Users\\funkec\\Documents\\GITHUB\\01_Models\\01_ZEN_universe"
        "\\03_ZEN_data\\Test\\test_8a"
    )
    dir2 = (
        "C:\\Users\\funkec\\Documents\\GITHUB\\01_Models\\01_ZEN_universe\\"
        "03_ZEN_data\\Test\\test_8a_replica"
    )

    compare_trees(dir1, dir2)
