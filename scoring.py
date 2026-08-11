# ============================================================
# EcoLens Scoring Engine
# ============================================================


def clamp(
    value,
    minimum=0,
    maximum=100,
):
    return max(
        minimum,
        min(maximum, value),
    )


# ============================================================
# ENVIRONMENTAL SCORES
# ============================================================

def heat_opportunity(
    temperature,
    humidity,
):
    """
    Simplified heat-related opportunity score.

    Demonstration metric only.
    """

    temperature_component = (
        (temperature - 18)
        / 17
        * 100
    )

    humidity_penalty = max(
        0,
        (humidity - 60) * 0.35,
    )

    return round(
        clamp(
            temperature_component
            - humidity_penalty
        )
    )


def solar_potential(
    temperature,
):
    """
    Simplified solar opportunity estimate.

    This is not a solar irradiance model.
    """

    if temperature >= 32:
        return 90

    if temperature >= 30:
        return 85

    if temperature >= 27:
        return 80

    if temperature >= 24:
        return 72

    if temperature >= 20:
        return 65

    return 55


def air_quality_pressure(
    aqi,
):
    """
    Higher air-quality pressure means greater
    opportunity for interventions that reduce
    environmental burden.

    AQI is used only as a simplified contextual factor.
    """

    if aqi <= 50:
        return 50

    if aqi <= 100:
        return 65

    if aqi <= 150:
        return 80

    return 95


# ============================================================
# AFFORDABILITY
# ============================================================

def affordability_score(
    budget,
    cost,
):
    if cost <= 0:
        return 100

    if budget >= cost:

        extra_capacity = (
            budget - cost
        )

        result = (
            70
            + min(
                30,
                (extra_capacity / cost) * 30,
            )
        )

        return round(
            clamp(result)
        )

    ratio = budget / cost

    return round(
        clamp(
            ratio * 65
        )
    )


# ============================================================
# COMPOSITE SCORE
# ============================================================

def intervention_score(
    *,
    environmental_opportunity,
    environmental_impact,
    affordability,
    feasibility,
):
    """
    Transparent weighted score.

    30% environmental opportunity
    30% environmental impact
    25% affordability
    15% feasibility
    """

    score = (
        environmental_opportunity * 0.30
        + environmental_impact * 0.30
        + affordability * 0.25
        + feasibility * 0.15
    )

    return round(
        clamp(score)
    )