#!/usr/bin/env python 

import unittest as ut
from startrader import model as st


class TestStarDateCreation(ut.TestCase):

    def test_creation_with_only_year_is_first_day(self):
        date = st.StarDate(2070)
        self.assertEqual(1, date.month)
        self.assertEqual(1, date.day)

    def test_with_early_year(self):
        with self.assertRaises(ValueError):
            st.StarDate(2060)

    def test_with_inconsistent_month(self):
        with self.assertRaises(ValueError):
            st.StarDate(month=0)

        with self.assertRaises(ValueError):
            st.StarDate(month=15)

    def test_with_inconsistent_day(self):
        with self.assertRaises(ValueError):
            st.StarDate(day=0)

        with self.assertRaises(ValueError):
            st.StarDate(day=34)

    def test_creation_with_other_year(self):
        date = st.StarDate(2080)
        self.assertEqual(2080, date.year)
        self.assertEqual(1, date.month)
        self.assertEqual(1, date.day)

    def test_creation_with_month(self):
        date = st.StarDate(2070, 5)
        self.assertEqual(2070, date.year)
        self.assertEqual(5, date.month)
        self.assertEqual(1, date.day)

    def test_creation_with_day(self):
        date = st.StarDate(2070, day=20)
        self.assertEqual(2070, date.year)
        self.assertEqual(1, date.month)
        self.assertEqual(20, date.day)


class TestClassMethodCreation(ut.TestCase):

    def test_0_day_creation(self):
        my_date = st.StarDate.for_days(0)
        self.assertEqual(2070, my_date.year)
        self.assertEqual(1, my_date.month)
        self.assertEqual(1, my_date.day)

    def test_next_month_creation(self):
        my_date = st.StarDate.for_days(31)
        self.assertEqual(2070, my_date.year)
        self.assertEqual(2, my_date.month)
        self.assertEqual(1, my_date.day)

    def test_next_year_creation(self):
        my_date = st.StarDate.for_days(361)
        self.assertEqual(2071, my_date.year)
        self.assertEqual(1, my_date.month)
        self.assertEqual(1, my_date.day)


class TestDateManipulation(ut.TestCase):

    def test_add_one_day(self):
        ref_day = st.StarDate(2070)
        self.assertEqual(1, ref_day.month)
        self.assertEqual(1, ref_day.day)
        later_day = ref_day + 1
        self.assertEqual(2070, later_day.year)
        self.assertEqual(2, later_day.day)

    def test_add_one_day_later_year(self):
        ref_day = st.StarDate(2080)
        later_day = ref_day + 1
        self.assertEqual(2080, later_day.year)
        self.assertEqual(1, later_day.month)
        self.assertEqual(2, later_day.day)

    def test_add_more_than_a_month(self):
        ref_day = st.StarDate(2080)
        later_day = ref_day + 46
        self.assertEqual(2080, later_day.year)
        self.assertEqual(2, later_day.month)
        self.assertEqual(17, later_day.day)

    def test_next_year(self):
        ref_day = st.StarDate(2080)
        later_day = ref_day + 360
        self.assertEqual(2081, later_day.year)
        self.assertEqual(1, later_day.month)
        self.assertEqual(1, later_day.day)
