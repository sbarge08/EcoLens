# EcoLens

### Environmental Decision Intelligence

[![Open Live App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ecolens-decision.streamlit.app/)

EcoLens combines environmental conditions, available resources, and transparent decision logic to help identify practical interventions for a specific location.

> **Understand your environment. Decide what to do next.**

---

## The Problem

Environmental data is widely available, but data alone does not tell people what action makes sense.

A location may have high temperatures, poor air quality, water-related risks, or strong solar potential, but the best intervention also depends on factors such as:

- Available budget
- Expected environmental benefit
- Implementation feasibility
- Estimated cost
- Potential savings

EcoLens connects these factors into a single decision-support workflow.

---

## What EcoLens Does

A user selects a location, provides an available budget, and optionally considers solar.

EcoLens then:

1. Retrieves environmental conditions and short-term forecast data.
2. Evaluates potential interventions.
3. Scores each intervention using multiple decision factors.
4. Ranks the available options.
5. Selects the strongest recommendation for the current resources.
6. Allows the user to test different budget scenarios.
7. Identifies resource thresholds where the recommendation changes.
8. Generates an explanation of the decision.

The goal is not simply to display environmental data, but to turn that data into an understandable decision.

---

## Key Features

### Environmental Assessment

EcoLens retrieves environmental information for the selected location, including:

- Temperature
- Humidity
- Air quality
- PM2.5
- Precipitation
- Short-term temperature trends

### Multi-Factor Decision Engine

Potential interventions are evaluated using:

- Environmental opportunity
- Environmental impact
- Affordability
- Implementation feasibility

The recommendation is generated using deterministic scoring rather than an AI model.

### Budget-Aware Recommendations

Available resources directly affect which interventions are competitive.

For example, an intervention with a higher environmental benefit may not be recommended if its estimated cost exceeds the available budget.

### Solar Consideration

EcoLens can incorporate solar potential when evaluating intervention options.

Solar is treated as one factor in the decision rather than automatically becoming the recommendation.

### Intervention Ranking

Instead of showing only one recommendation, EcoLens ranks multiple possible interventions so users can compare alternatives.

Example interventions include:

- HVAC Optimization
- Energy Efficiency Upgrade
- Heat Mitigation Upgrade
- Solar Energy Installation
- Water Conservation Upgrade

### What-If Scenario Analysis

Users can change the available budget and see how the decision responds.

The scenario engine recalculates:

- Recommendation
- Opportunity score
- Estimated cost
- Estimated savings
- Intervention ranking

### Decision Thresholds

EcoLens identifies approximately where additional resources cause the recommended intervention to change.

This helps answer questions such as:

> "At what budget would a different intervention become the better option?"

### Explainable AI

AI is used as an explanation layer rather than the underlying decision maker.

The deterministic decision engine produces the recommendation first.

The AI then interprets the evidence and explains:

- Why the intervention was selected
- What factors influenced the decision
- What tradeoffs exist
- What should be validated before implementation

### Evidence Transparency

EcoLens distinguishes between information that is measured or retrieved from environmental data and values that are model estimates.

This helps prevent estimated financial or intervention outcomes from being mistaken for observed measurements.

### Location Visualization

The assessment includes a geographic visualization of the selected location.

---

# How the Decision Works

EcoLens separates **measurement, decision-making, and explanation**.

```text
Environmental Data
       ↓
Data Processing
       ↓
Decision Scoring
       ↓
Intervention Ranking
       ↓
Recommendation
       ↓
Scenario Analysis
       ↓
AI Explanation