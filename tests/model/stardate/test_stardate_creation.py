#!/usr/bin/env python 

from startrader import model as st
import pytest


def test_creation_with_only_year_is_first_day():
    date = st.StarDate(2070)
    assert 1 == date.month
    assert 1 == date.day


def test_with_early_year():
    with pytest.raises(ValueError):
        st.StarDate(2060)


def test_with_inconsistent_month():
    with pytest.raises(ValueError):
        st.StarDate(month=0)

    with pytest.raises(ValueError):
        st.StarDate(month=15)


def test_with_inconsistent_day():
    with pytest.raises(ValueError):
        st.StarDate(day=0)

    with pytest.raises(ValueError):
        st.StarDate(day=34)


def test_creation_with_other_year():
    date = st.StarDate(2080)
    assert 2080 == date.year
    assert 1 == date.month
    assert 1 == date.day


def test_creation_with_month():
    date = st.StarDate(2070, 5)
    assert 2070 == date.year
    assert 5 == date.month
    assert 1 == date.day


def test_creation_with_day():
    date = st.StarDate(2070, day=20)
    assert 2070 == date.year
    assert 1 == date.month
    assert 20 == date.day
