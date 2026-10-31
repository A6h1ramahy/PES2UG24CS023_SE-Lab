"""Test cases focused on executing every application statement (line coverage)."""

import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


def test_delivery_out_of_range_at_zero():
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(0, 250, False)


def test_delivery_out_of_range_above_maximum():
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(15.1, 250, False)


def test_delivery_free_for_order_value_at_least_500():
    assert delivery_charge(2, 500, False) == 0


def test_delivery_near_distance_band():
    assert delivery_charge(2, 200, False) == 20


def test_delivery_middle_distance_band():
    assert delivery_charge(5, 200, False) == 40


def test_delivery_far_distance_band():
    assert delivery_charge(10, 200, False) == 60


def test_delivery_rain_adds_surcharge():
    assert delivery_charge(2, 200, True) == 50


def test_no_coupon():
    assert apply_coupon(300, None, False) == 300


def test_invalid_coupon_raises_error():
    with pytest.raises(ValueError, match="invalid coupon"):
        apply_coupon(300, "NOTREAL", True)


def test_welcome_coupon_rejected_for_returning_customer():
    with pytest.raises(ValueError, match="coupon only for first order"):
        apply_coupon(300, "WELCOME", False)


def test_coupon_not_applied_below_minimum_order_value():
    assert apply_coupon(199, "SAVE50", False) == 199


def test_save50_coupon_applied():
    assert apply_coupon(300, "SAVE50", False) == 250


def test_welcome_coupon_applied_for_first_order():
    assert apply_coupon(300, "WELCOME", True) == 200


def test_estimated_time_without_peak_or_busy_restaurant():
    assert estimated_time(2, False, False) == 23


def test_estimated_time_during_peak_hour():
    assert estimated_time(2, True, False) == 33


def test_estimated_time_when_restaurant_is_busy_outside_peak():
    assert estimated_time(2, False, True) == 38


def test_estimated_time_when_restaurant_is_busy_during_peak():
    assert estimated_time(2, True, True) == 53
