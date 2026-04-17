def classify_event(magnitude, depth, nearby_conflict=False):
    score = 0

    # Natural indicators
    if magnitude <= 3:
        score += 2
    if depth and depth > 5:
        score += 2

    # Explosion indicators
    if depth and depth < 2:
        score -= 2
    if nearby_conflict:
        score -= 2

    if score >= 2:
        return "Natural", score
    elif score <= -2:
        return "Munitions", score
    else:
        return "Uncertain", score