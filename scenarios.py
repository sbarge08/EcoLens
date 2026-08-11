from recommendations import generate_recommendation


# ============================================================
# SCENARIO EVALUATION
# ============================================================

def evaluate_scenario(
    *,
    temperature,
    humidity,
    aqi,
    total_rain,
    budget,
    solar,
):
    return generate_recommendation(
        temperature=temperature,
        humidity=humidity,
        aqi=aqi,
        total_rain=total_rain,
        budget=budget,
        solar=solar,
    )


# ============================================================
# DECISION CHANGE
# ============================================================

def compare_decisions(
    current,
    scenario,
):
    current_name = (
        current["recommendation"]
    )

    scenario_name = (
        scenario["recommendation"]
    )

    score_change = (
        scenario["decision_score"]
        - current["decision_score"]
    )

    savings_change = (
        scenario["annual_savings"]
        - current["annual_savings"]
    )

    cost_change = (
        scenario["estimated_cost"]
        - current["estimated_cost"]
    )

    recommendation_changed = (
        current_name != scenario_name
    )

    reasons = []

    if (
        scenario["budget_score"]
        > current["budget_score"]
    ):
        reasons.append(
            "higher budget improved affordability"
        )

    if (
        scenario["solar_score"]
        > current["solar_score"]
    ):
        reasons.append(
            "solar opportunity remained strong"
        )

    if (
        scenario["decision_score"]
        > current["decision_score"]
    ):
        reasons.append(
            "the highest-scoring option became more competitive"
        )

    if not reasons:
        reasons.append(
            "the relative ranking of the interventions remained similar"
        )

    return {
        "recommendation_changed":
            recommendation_changed,

        "current_name":
            current_name,

        "scenario_name":
            scenario_name,

        "score_change":
            score_change,

        "savings_change":
            savings_change,

        "cost_change":
            cost_change,

        "reasons":
            reasons,
    }


# ============================================================
# DECISION BOUNDARY
# ============================================================

def find_decision_boundary(
    *,
    temperature,
    humidity,
    aqi,
    total_rain,
    solar,
    current_recommendation,
    minimum_budget=1000,
    maximum_budget=25000,
    step=1000,
):
    """
    Finds the first budget at which the recommendation
    changes from the current recommendation.
    """

    for budget in range(
        minimum_budget,
        maximum_budget + step,
        step,
    ):

        scenario = evaluate_scenario(
            temperature=temperature,
            humidity=humidity,
            aqi=aqi,
            total_rain=total_rain,
            budget=budget,
            solar=solar,
        )

        if (
            scenario["recommendation"]
            != current_recommendation
        ):

            return budget, scenario

    return None, None