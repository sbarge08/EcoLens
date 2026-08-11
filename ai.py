import os
import streamlit as st

from openai import OpenAI


# ============================================================
# GET API KEY
# ============================================================

def get_api_key():

    # --------------------------------------------------------
    # Streamlit Cloud / Streamlit Secrets
    # --------------------------------------------------------

    try:

        if "FEATHERLESS_API_KEY" in st.secrets:

            return st.secrets[
                "FEATHERLESS_API_KEY"
            ]

    except Exception:

        pass

    # --------------------------------------------------------
    # Local environment variable
    # --------------------------------------------------------

    return os.getenv(
        "FEATHERLESS_API_KEY"
    )


# ============================================================
# AI EXPLANATION
# ============================================================

def generate_explanation(
    *,
    temperature,
    humidity,
    aqi,
    pm25,
    precipitation,
    budget,
    recommendation,
    recommendation_cost,
    decision_score,
    heat_score,
    solar_score,
    ranked_interventions,
):
    """
    AI is used only as the explanation layer.

    The deterministic decision engine selects
    the intervention.
    """

    fallback = (
        f"{recommendation} is the strongest fit for this "
        f"assessment because it provides a practical balance "
        f"between environmental opportunity, available "
        f"resources, and implementation feasibility.\n\n"
        f"Before implementation, the estimated cost and "
        f"savings should be validated through a site-specific "
        f"assessment. Actual results will depend on building "
        f"conditions, equipment performance, utility rates, "
        f"incentives, and project design."
    )

    api_key = get_api_key()

    # --------------------------------------------------------
    # No API key
    # --------------------------------------------------------

    if not api_key:

        return fallback

    try:

        client = OpenAI(
            base_url="https://api.featherless.ai/v1",
            api_key=api_key,
            timeout=20,
        )

        ranking_text = "\n".join(
            [
                (
                    f"- {item['name']}: "
                    f"{item['score']}/100"
                )
                for item in ranked_interventions
            ]
        )

        prompt = f"""
You are the explainability layer for EcoLens,
an environmental decision-support application.

The deterministic decision engine has already selected
the intervention.

Do NOT make a new recommendation.

Environmental conditions:

Temperature: {temperature:.1f} °C
Humidity: {humidity:.0f}%
AQI: {aqi}
PM2.5: {pm25}
7-day precipitation: {precipitation:.1f} mm

Available budget:
${budget:,}

Selected intervention:
{recommendation}

Estimated cost:
${recommendation_cost:,}

Opportunity score:
{decision_score}/100

Heat opportunity:
{heat_score}/100

Solar potential:
{solar_score}/100

Intervention ranking:

{ranking_text}

Write two sections:

DECISION RATIONALE

Explain why the selected intervention fits the
current environmental conditions and available
resources.

TRADEOFFS AND VALIDATION

Explain what should be validated before implementation,
including engineering conditions, actual energy use,
cost, savings, utility rates, incentives, and site
specific information.

Rules:

- Do not write "Paragraph 1".
- Do not write "Paragraph 2".
- Do not use emojis.
- Do not say "the AI thinks".
- Do not invent measurements.
- Do not invent financial information.
- Do not create another recommendation.
- Do not claim weather data guarantees financial outcomes.
- Do not repeat the entire dashboard.
- Keep the writing concise and professional.
"""

        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_tokens=360,
            temperature=0.15,
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

    except Exception:

        return fallback