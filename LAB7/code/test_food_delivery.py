from hypothesis import given, strategies as st
import pytest

from food_delivery import (
    parse_order,
    delivery_eta,
    coupon_discount
)


# ============================================================
# 1. PARSE ORDER - FUZZ TESTING
# ============================================================

@given(st.one_of(st.text(), st.none()))
def test_parse_order_no_crash(s):
    try:
        parse_order(s)
    except (ValueError, TypeError):
        pass


# Test valid order inputs using Hypothesis
@given(
    st.dictionaries(
        keys=st.text(
            alphabet="abcdefghijklmnopqrstuvwxyz",
            min_size=1,
            max_size=15
        ),
        values=st.integers(min_value=1, max_value=100),
        min_size=1,
        max_size=10
    )
)
def test_parse_order_valid_input(items):

    order_string = ",".join(
        f"{name}:{qty}" for name, qty in items.items()
    )

    result = parse_order(order_string)

    assert isinstance(result, dict)
    assert len(result) == len(items)

    assert result == {
        name.casefold(): qty
        for name, qty in items.items()
    }


# Test invalid order inputs
@pytest.mark.parametrize("invalid_order", [
    "",
    "pizza",
    "pizza:two",
    "pizza:-2",
    "pizza:0",
    "pizza:101",
    "pizza:2,,burger:1",
    "pizza:2:3",
    "pizza:2,pizza:3",
    None
])
def test_parse_order_invalid_inputs(invalid_order):

    with pytest.raises((ValueError, TypeError)):
        parse_order(invalid_order)


# ============================================================
# 2. DELIVERY ETA - FUZZ TESTING
# ============================================================

@given(st.one_of(st.text(), st.none()))
def test_delivery_eta_no_crash(s):
    try:
        delivery_eta(s)
    except (ValueError, TypeError):
        pass


# Test valid delivery distances
@given(
    st.floats(
        min_value=0,
        max_value=10000,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_delivery_eta_valid_distance(distance):

    result = delivery_eta(distance)

    assert isinstance(result, int)
    assert result >= 15


# Test invalid delivery distances
@pytest.mark.parametrize("invalid_distance", [
    -1,
    "hello",
    "",
    None,
    float("inf"),
    float("-inf"),
    float("nan"),
    10001,
    True
])
def test_delivery_eta_invalid_inputs(invalid_distance):

    with pytest.raises((ValueError, TypeError)):
        delivery_eta(invalid_distance)


# ============================================================
# 3. COUPON DISCOUNT - FUZZ TESTING
# ============================================================

@given(st.one_of(st.text(), st.none()))
def test_coupon_discount_no_crash(s):
    try:
        coupon_discount(s)
    except (ValueError, TypeError):
        pass


# Test valid coupon codes
@given(st.integers(min_value=0, max_value=100))
def test_coupon_discount_valid_code(discount):

    code = f"SAVE{discount}"

    result = coupon_discount(code)

    assert result == discount


# Test invalid coupon codes
@pytest.mark.parametrize("invalid_coupon", [
    "",
    "SAVE",
    "SAVEABC",
    "HELLO",
    "SAVE-50",
    "SAVE150",
    "SAVE50SAVE20",
    None,
    123
])
def test_coupon_discount_invalid_inputs(invalid_coupon):

    with pytest.raises((ValueError, TypeError)):
        coupon_discount(invalid_coupon)
