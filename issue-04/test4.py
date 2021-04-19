from typing import List, Tuple
import pytest


def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows


def test_1():
    assert fit_transform("Mask") == [("Mask", [1])]


def test_empty_str():
    assert fit_transform("") == [("", [1])]


def test_int():
    with pytest.raises(TypeError):
        fit_transform(2)


def test_empty():
    with pytest.raises(TypeError):
        fit_transform()


def test_two_args():
    assert fit_transform("Moscow", "Piter") == [('Moscow', [0, 1]), ('Piter', [1, 0])]


