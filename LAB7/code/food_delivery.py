import math
import re


def parse_order(items_csv):
    """
    Parse a CSV-style food order.

    Expected format:
        pizza:2,burger:1

    Returns:
        Dictionary containing food names and quantities.

    Raises:
        TypeError: When input is not a string.
        ValueError: When the order format or values are invalid.
    """

    if not isinstance(items_csv, str):
        raise TypeError("Order must be provided as a string.")

    if not items_csv.strip():
        raise ValueError("Order cannot be empty.")

    order = {}

    items = items_csv.split(",")

    for item in items:

        if not item.strip():
            raise ValueError("Empty food item is not allowed.")

        parts = item.split(":")

        if len(parts) != 2:
            raise ValueError(
                "Each food item must follow name:quantity format."
            )

        name = parts[0].strip()
        qty_text = parts[1].strip()

        if not name:
            raise ValueError("Food name cannot be empty.")

        if not re.fullmatch(r"\d+", qty_text):
            raise ValueError(
                "Quantity must be a positive integer."
            )

        qty = int(qty_text)

        if qty <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        if qty > 100:
            raise ValueError(
                "Quantity cannot exceed 100."
            )

        normalized_name = name.casefold()

        if normalized_name in order:
            raise ValueError(
                "Duplicate food items are not allowed."
            )

        order[normalized_name] = qty

    return order


def delivery_eta(distance_km):
    """
    Calculate the estimated delivery time.

    ETA formula:
        15 + (distance_km * 4)

    Returns:
        Estimated delivery time in minutes.

    Raises:
        TypeError: For non-numeric or boolean input.
        ValueError: For invalid or negative distances.
    """

    if isinstance(distance_km, bool):
        raise TypeError(
            "Distance must be a numeric value."
        )

    try:
        distance = float(distance_km)

    except (ValueError, TypeError, OverflowError) as exc:
        raise TypeError(
            "Distance must be a valid numeric value."
        ) from exc

    if not math.isfinite(distance):
        raise ValueError(
            "Distance must be finite."
        )

    if distance < 0:
        raise ValueError(
            "Distance cannot be negative."
        )

    if distance > 10000:
        raise ValueError(
            "Distance is unrealistically large."
        )

    return int(15 + distance * 4)


def coupon_discount(code):
    """
    Extract the discount percentage from a coupon code.

    Valid format:
        SAVE followed by a percentage from 0 to 100.

    Example:
        SAVE50 -> 50

    Raises:
        TypeError: When input is not a string.
        ValueError: When coupon format or percentage is invalid.
    """

    if not isinstance(code, str):
        raise TypeError(
            "Coupon code must be a string."
        )

    code = code.strip().upper()

    match = re.fullmatch(
        r"SAVE(\d+)",
        code
    )

    if not match:
        raise ValueError(
            "Invalid coupon format. Expected SAVE followed by a percentage."
        )

    discount = int(match.group(1))

    if not 0 <= discount <= 100:
        raise ValueError(
            "Discount must be between 0 and 100."
        )

    return discount


def main():

    print("==== Running parse_order ====")

    user_input = input(
        "Enter items as name:qty CSV (e.g. pizza:2,burger:1): "
    )

    try:
        result = parse_order(user_input)
        print("Order:", result)

    except (ValueError, TypeError) as exc:
        print("Order Error:", exc)


    print("\n==== Running delivery_eta ====")

    user_input = input(
        "Enter distance in km (e.g. 4.5): "
    )

    try:
        result = delivery_eta(user_input)
        print("ETA in Minutes:", result)

    except (ValueError, TypeError) as exc:
        print("Delivery Error:", exc)


    print("\n==== Running coupon_discount ====")

    user_input = input(
        "Enter a coupon code (e.g. SAVE50): "
    )

    try:
        result = coupon_discount(user_input)
        print("Discount:", result)

    except (ValueError, TypeError) as exc:
        print("Coupon Error:", exc)


if __name__ == "__main__":
    main()