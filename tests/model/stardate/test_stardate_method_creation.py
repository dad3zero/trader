#!/usr/bin/env python 

from startrader import model as st


def test_0_day_creation():
    my_date = st.StarDate.for_days(0)
    assert 2070 == my_date.year
    assert 1 == my_date.month
    assert 1 == my_date.day


def test_next_month_creation():
    my_date = st.StarDate.for_days(31)
    assert 2070 == my_date.year
    assert 2 == my_date.month
    assert 1 == my_date.day


def test_next_year_creation():
    my_date = st.StarDate.for_days(361)
    assert 2071 == my_date.year
    assert 1 == my_date.month
    assert 1 == my_date.day