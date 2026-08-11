from scoring import (
    affordability_score,
    heat_opportunity,
    solar_potential,
    air_quality_pressure,
    intervention_score,
)


# ============================================================
# INTERVENTION DATABASE
# ============================================================

INTERVENTIONS = [
    {
        "name": "Energy Efficiency Upgrade",
        "cost": 5000,
        "annual_savings": 1100,
        "impact": "Medium-High",
        "environmental_impact": 82,
        "feasibility": 92,
        "type": "energy",
    },

    {
        "name": "Solar Energy Installation",
        "cost": 12000,
        "annual_savings": 1800,
        "impact": "High",
        "environmental_impact": 94,
        "feasibility": 70,
        "type": "solar",
    },

    {
        "name": "HVAC Optimization",
        "cost": 3000,
        "annual_savings": 750,
        "impact": "Medium",
        "environmental_impact": 72,
        "feasibility": 95,
        "type": "hvac",
    },

    {
        "name": "Water Conservation Upgrade",
        "cost": 4000,
        "annual_savings": 500,
        "impact": "Medium",
        "environmental_impact": 70,
        "feasibility": 88,
        "type": "water",
    },

    {
        "name": "Heat Mitigation Upgrade",
        "cost": 7000,
        "annual_savings": 650,
        "impact": "High",
        "environmental_impact": 86,
        "feasibility": 76,
        "type": "heat",
    },
]


# ============================================================
# SCORE INTERVENTION
# ============================================================

def score_intervention(
    intervention,
    *,
    budget,
    heat_score,
    solar_score,
    air_score,
    total_rain,
):
    intervention_type = intervention["type"]

    # --------------------------------------------------------
    # Environmental opportunity
    # --------------------------------------------------------

    if intervention_type == "solar":

        environmental_opportunity = (
            heat_score * 0.40
            + solar_score * 0.60
        )

    elif intervention_type == "energy":

        environmental_opportunity = (
            heat_score * 0.70
            + solar_score * 0.20
            + air_score * 0.10
        )

    elif intervention_type == "hvac":

        environmental_opportunity = (
            heat_score * 0.85
            + air_score * 0.15
        )

    elif intervention_type == "water":

        rain_factor = (
            min(total_rain, 80)
            / 80
            * 100
        )

        environmental_opportunity = (
            rain_factor * 0.55
            + air_score * 0.10
            + (100 - heat_score) * 0.35
        )

    else:

        environmental_opportunity = (
            heat_score * 0.75
            + air_score * 0.25
        )

    environmental_opportunity = min(
        100,
        max(
            0,
            environmental_opportunity
        )
    )

    # --------------------------------------------------------
    # Affordability
    # --------------------------------------------------------

    affordability = affordability_score(
        budget=budget,
        cost=intervention["cost"],
    )

    # --------------------------------------------------------
    # Final score
    # --------------------------------------------------------

    score = intervention_score(
        environmental_opportunity=environmental_opportunity,
        environmental_impact=intervention[
            "environmental_impact"
        ],
        affordability=affordability,
        feasibility=intervention[
            "feasibility"
        ],
    )

    result = intervention.copy()

    result["score"] = score

    result["affordability"] = affordability

    result["environmental_opportunity"] = round(
        environmental_opportunity
    )

    return result


# ============================================================
# MAIN DECISION ENGINE
# ============================================================

def generate_recommendation(
    temperature,
    budget,
    solar=True,
    humidity=50,
    aqi=60,
    total_rain=10,
):
    """
    Main deterministic EcoLens decision engine.
    """

    heat_score = heat_opportunity(
        temperature=temperature,
        humidity=humidity,
    )

    solar_score = solar_potential(
        temperature=temperature,
    )

    air_score = air_quality_pressure(
        aqi=aqi,
    )

    ranked = []

    for intervention in INTERVENTIONS:

        if (
            intervention["type"]
            == "solar"
            and not solar
        ):
            continue

        result = score_intervention(
            intervention,
            budget=budget,
            heat_score=heat_score,
            solar_score=solar_score,
            air_score=air_score,
            total_rain=total_rain,
        )

        ranked.append(result)

    ranked.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    winner = ranked[0]

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    if len(ranked) >= 2:

        score_gap = (
            winner["score"]
            - ranked[1]["score"]
        )

    else:

        score_gap = 15

    confidence = min(
        96,
        max(
            68,
            round(
                70 + score_gap * 2
            )
        )
    )

    # --------------------------------------------------------
    # Reason
    # --------------------------------------------------------

    if winner["type"] == "solar":

        reason = (
            "Solar energy ranks strongly because the "
            "environmental opportunity is high and the "
            "larger investment becomes more practical "
            "as available resources increase."
        )

    elif winner["type"] == "hvac":

        reason = (
            "HVAC optimization provides a relatively "
            "low-cost way to address heat-related energy "
            "demand while maintaining strong implementation "
            "feasibility."
        )

    elif winner["type"] == "water":

        reason = (
            "Water conservation provides a practical "
            "resource-efficiency pathway when precipitation "
            "patterns and available project resources make "
            "water management relevant."
        )

    elif winner["type"] == "heat":

        reason = (
            "Heat mitigation offers a strong response to "
            "elevated thermal conditions, with meaningful "
            "environmental impact but a higher upfront "
            "investment."
        )

    else:

        reason = (
            "Energy efficiency provides a practical "
            "balance between environmental opportunity, "
            "upfront cost, expected savings, and "
            "implementation feasibility."
        )

    return {
        "recommendation": winner["name"],
        "reason": reason,
        "estimated_cost": winner["cost"],
        "annual_savings": winner["annual_savings"],
        "impact": winner["impact"],
        "confidence": confidence,
        "decision_score": winner["score"],
        "heat_score": heat_score,
        "budget_score": winner["affordability"],
        "solar_score": solar_score,
        "air_score": air_score,
        "environmental_opportunity": winner[
            "environmental_opportunity"
        ],
        "ranked_interventions": ranked,
    }