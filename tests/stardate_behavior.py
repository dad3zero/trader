#!/usr/bin/env python 

from startrader.creation import starsystem as st
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


def test_0_day_creation():
    with pytest.raises(ValueError):
        st.StarDate.for_days(0)


def test_next_month_creation():
    my_date = st.StarDate.for_days((2070 * 360) + 31)
    assert 2070 == my_date.year
    assert 2 == my_date.month
    assert 1 == my_date.day


def test_next_year_creation():
    my_date = st.StarDate.for_days((2070 * 360) + 361)
    assert 2071 == my_date.year
    assert 1 == my_date.month
    assert 1 == my_date.day


def test_add_one_day():
    ref_day = st.StarDate(2070)
    assert 1 == ref_day.month
    assert 1 == ref_day.day
    later_day = ref_day + 1
    assert 2070 == later_day.year
    assert 2 == later_day.day


def test_add_one_day_later_year():
    ref_day = st.StarDate(2080)
    later_day = ref_day + 1
    assert 2080 == later_day.year
    assert 1 == later_day.month
    assert 2 == later_day.day


def test_add_more_than_a_month():
    ref_day = st.StarDate(2080)
    later_day = ref_day + 46
    assert 2080 == later_day.year
    assert 2 == later_day.month
    assert 17 == later_day.day


def test_next_year():
    ref_day = st.StarDate(2080)
    later_day = ref_day + 360
    assert 2081 == later_day.year
    assert 1 == later_day.month
    assert 1 == later_day.day
