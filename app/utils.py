def base10_to_base62(str_num: str):
    """Convert base10 numeric uid into shorter string."""
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = 62

    num = int(str_num)

    # Edge case for zero
    if num == 0:
        return "0"

    # Convert the number to base62
    result = []
    while num > 0:
        remainder = num % base
        result.append(chars[remainder])
        num //= base

    # Reverse the result since the remainder is collected in reverse order
    return "".join(reversed(result))


def create_url_from_uid(uid: str, long_url: str):
    return {
        "id": uid,
        "long_url": long_url,
        "short_url": base10_to_base62(uid),
    }
