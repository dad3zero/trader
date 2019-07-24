#!/usr/bin/env python 

from startrader import model as st


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