"""Test cases exercising both outcomes of every decision (branch coverage)."""

import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


# delivery_charge: invalid-range decision (True and False), and all fee bands.
def test_delivery_distance_zero_is_rejected():
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(0, 200, False)


def test_delivery_distance_above_15_is_rejected():
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(16, 200, False)


def test_delivery_valid_distance_and_free_order_threshold():
    assert delivery_charge(1, 500, False) == 0


def test_delivery_order_below_500_and_distance_at_most_3():
    assert delivery_charge(3, 499, False) == 20


def test_delivery_distance_between_3_and_8():
    assert delivery_charge(3.1, 499, False) == 40


def test_delivery_distance_above_8_through_15():
    assert delivery_charge(15, 499, False) == 60


def test_delivery_rain_branch_true():
    assert delivery_charge(2, 200, True) == 50


def test_delivery_rain_branch_false():
    assert delivery_charge(2, 200, False) == 20


# apply_coupon: no-code, valid/invalid code, WELCOME eligibility and minimum value.
def test_coupon_code_none():
    assert apply_coupon(250, None, False) == 250


def test_coupon_code_invalid():
    with pytest.raises(ValueError, match="invalid coupon"):
        apply_coupon(250, "UNKNOWN", True)


def test_welcome_coupon_for_non_first_order_is_rejected():
    with pytest.raises(ValueError, match="coupon only for first order"):
        apply_coupon(250, "WELCOME", False)


def test_welcome_coupon_for_first_order_above_minimum():
    assert apply_coupon(250, "WELCOME", True) == 150


def test_save50_coupon_above_minimum():
    assert apply_coupon(250, "SAVE50", False) == 200


def test_valid_coupon_order_below_200_is_unchanged():
    assert apply_coupon(199, "SAVE50", False) == 199


def test_coupon_at_exact_minimum_order_value_is_applied():
    assert apply_coupon(200, "SAVE50", False) == 150


# estimated_time: peak-hour branch, busy branch and nested peak-hour branch.
def test_no_peak_and_not_busy():
    assert estimated_time(2, False, False) == 23


def test_peak_hour_and_not_busy():
    assert estimated_time(2, True, False) == 33


def test_busy_restaurant_outside_peak_hour():
    assert estimated_time(2, False, True) == 38


def test_busy_restaurant_during_peak_hour():
    assert estimated_time(2, True, True) == 53
