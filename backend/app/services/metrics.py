def calculate_rate(value: int, impressions: int) -> float:
    if impressions == 0:
        return 0.0

    return value / impressions * 100
