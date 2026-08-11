# EcoLens

### Environmental Decision Intelligence

[![Open Live App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ecolens-decision.streamlit.app/)

EcoLens transforms environmental conditions and resource constraints into practical, explainable intervention recommendations.

---

## Why EcoLens?

Environmental data can tell us what is happening, but it does not always tell us what action makes sense given the resources available.

EcoLens addresses that gap by combining environmental data with a deterministic decision engine, budget constraints, scenario analysis, and an explainable AI layer.

The goal is simple:

> **Given the conditions and resources available, what should we consider doing next?**

---

## What EcoLens Does

A user selects a location, defines an available budget, and optionally considers solar.

EcoLens then:

1. Retrieves environmental conditions and short-term forecast information.
2. Evaluates potential environmental interventions.
3. Scores each intervention using multiple decision factors.
4. Selects the strongest option for the current constraints.
5. Allows the user to change the available budget and explore alternative scenarios.
6. Explains the resulting decision using the evidence produced by the decision engine.

---

## Key Features

### Environmental Assessment

EcoLens provides a location-specific environmental profile including:

- Temperature
- Air quality
- Humidity
- Precipitation
- Short-term temperature trends

### Decision Engine

Potential interventions are evaluated using:

- Environmental opportunity
- Environmental impact
- Affordability
- Implementation feasibility
- Available budget
- Solar consideration

The recommendation is produced by deterministic scoring rather than by the AI model.

### Budget-Aware Recommendations

Available resources are part of the decision itself.

An intervention may have strong environmental potential but still rank lower if it does not fit the available budget or has lower implementation feasibility.

### Scenario Analysis

The budget can be changed after an assessment to explore how the decision responds to different resource levels.

EcoLens recalculates:

- Intervention rankings
- Opportunity scores
- Estimated costs
- Estimated savings
- Recommendation changes

### Decision Thresholds

The scenario engine can identify approximately where additional resources cause the recommended intervention to change.

This provides more information than a single recommendation because it shows how sensitive the decision is to the available budget.

### Explainable AI

The AI layer interprets the evidence produced by the decision engine and converts it into a human-readable rationale.

It does not generate the underlying environmental measurements or financial estimates.

---

## Decision Engine

EcoLens uses a deterministic scoring approach to compare potential interventions.

The scoring process considers environmental opportunity, environmental impact, affordability, and implementation feasibility.

The resulting scores are used to rank interventions and determine the recommendation for the current assessment.

Keeping this logic deterministic makes the core recommendation reproducible and easier to inspect.

---

## Scenario Analysis

A key part of EcoLens is the ability to explore:

> **What changes if the available resources change?**

For example, a user can compare the decision at:

```text
$1,000
$5,000
$10,000
$15,000
$25,000