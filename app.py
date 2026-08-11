import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from data import (
    get_environmental_profile,
    LOCATIONS,
)

from recommendations import (
    generate_recommendation,
)

from scenarios import (
    evaluate_scenario,
    compare_decisions,
    find_decision_boundary,
)

from ai import (
    generate_explanation,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="EcoLens",
    page_icon="E",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "assessment_started" not in st.session_state:
    st.session_state.assessment_started = False


# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background-color: #F5F7F1;
    }

    .main {
        background-color: #F5F7F1;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 1.7rem;
        padding-bottom: 4rem;
    }


    /* ======================================================
       TYPOGRAPHY
       ====================================================== */

    h1 {
        color: #12372A !important;
        font-size: 3.5rem !important;
        font-weight: 850 !important;
        letter-spacing: -3px !important;
        line-height: 1 !important;
    }

    h2 {
        color: #12372A !important;
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
    }

    h3 {
        color: #183D30 !important;
        font-weight: 750 !important;
    }

    p {
        color: #52665D !important;
        line-height: 1.65 !important;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {
        background-color: #12372A !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #B9CCC2 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #315447 !important;
    }

    [data-testid="stSidebar"]
    [data-baseweb="select"]
    > div {
        background-color: #1A4435 !important;
        border-color: #416455 !important;
        border-radius: 8px !important;
    }

    [data-testid="stSidebar"]
    [data-baseweb="select"]
    span {
        color: #FFFFFF !important;
    }


    /* ======================================================
       PRIMARY BUTTON
       ====================================================== */

    [data-testid="stSidebar"]
    .stButton
    > button {
        background-color: #B8E986 !important;
        border: 1px solid #B8E986 !important;
        border-radius: 10px !important;
        min-height: 3rem !important;
        color: #12372A !important;
        font-weight: 800 !important;
    }

    [data-testid="stSidebar"]
    .stButton
    > button p,
    [data-testid="stSidebar"]
    .stButton
    > button span,
    [data-testid="stSidebar"]
    .stButton
    > button div {
        color: #12372A !important;
    }

    [data-testid="stSidebar"]
    .stButton
    > button:hover {
        background-color: #C9F39C !important;
        border-color: #C9F39C !important;
    }


    /* ======================================================
       SIDEBAR CONTROLS
       ====================================================== */

    [data-testid="stSidebar"]
    [data-testid="stSlider"]
    [role="slider"] {
        background-color: #B8E986 !important;
        border-color: #B8E986 !important;
        box-shadow: 0 0 0 2px #12372A !important;
    }

    [data-testid="stSidebar"]
    [data-testid="stSlider"]
    div[data-baseweb="slider"]
    > div
    > div {
        background-color: #B8E986 !important;
    }

    [data-testid="stSidebar"]
    [data-testid="stCheckbox"]
    label span {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"]
    [data-testid="stCheckbox"]
    input:checked + div {
        background-color: #B8E986 !important;
        border-color: #B8E986 !important;
    }


    /* ======================================================
       CONTAINERS
       ====================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE5DD !important;
        border-radius: 16px !important;
        box-shadow:
            0 8px 25px
            rgba(18,55,42,0.045) !important;
    }


    /* ======================================================
       METRICS
       ====================================================== */

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #DCE5DD;
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        box-shadow:
            0 6px 20px
            rgba(18,55,42,0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #708179 !important;
        font-size: 0.67rem !important;
        font-weight: 750 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    [data-testid="stMetricValue"] {
        color: #12372A !important;
        font-weight: 850 !important;
        letter-spacing: -1px !important;
    }


    /* ======================================================
       PROGRESS
       ====================================================== */

    [data-testid="stProgress"] > div {
        background-color: #DCE8DF !important;
        border-radius: 20px !important;
    }

    [data-testid="stProgress"] > div > div {
        background-color: #1D8F62 !important;
        border-radius: 20px !important;
    }


    /* ======================================================
       DATAFRAME
       ====================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #DCE5DD !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }


    /* ======================================================
       PLOTLY
       ====================================================== */

    [data-testid="stPlotlyChart"] {
        background-color: #FFFFFF;
        border: 1px solid #DCE5DD;
        border-radius: 16px;
        padding: 0.3rem;
        box-shadow:
            0 7px 22px
            rgba(18,55,42,0.04);
    }


    /* ======================================================
       EXPANDER
       ====================================================== */

    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE5DD !important;
        border-radius: 14px !important;
    }


    /* ======================================================
       ALERT
       ====================================================== */

    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# EcoLens")

    st.caption(
        "ENVIRONMENTAL INTELLIGENCE"
    )

    st.divider()

    st.subheader(
        "Assessment"
    )

    location_options = list(
        LOCATIONS.keys()
    )

    city = st.selectbox(
        "Location",
        location_options,
    )

    budget = st.slider(
        "Available budget",
        1000,
        25000,
        5000,
        step=1000,
        format="$%d",
    )

    solar = st.checkbox(
        "Consider solar",
        value=True,
    )

    st.divider()

    if st.button(
        "Run Assessment",
        width="stretch",
    ):

        st.session_state.assessment_started = True

    st.divider()

    st.caption(
        "Environmental data"
    )

    st.caption(
        "Decision engine"
    )

    st.caption(
        "Scenario analysis"
    )

    st.caption(
        "Explainable AI"
    )


# ============================================================
# HERO
# ============================================================

st.caption(
    "ENVIRONMENTAL INTELLIGENCE"
)

st.title(
    "EcoLens"
)

st.subheader(
    "Understand your environment. Decide what to do next."
)

st.write(
    "EcoLens combines environmental data, resource "
    "constraints, and transparent decision logic to "
    "identify practical interventions for a specific "
    "location."
)

st.divider()


# ============================================================
# EMPTY STATE
# ============================================================

if not st.session_state.assessment_started:

    st.caption(
        "GET STARTED"
    )

    st.header(
        "Ready to assess a location"
    )

    st.write(
        "Configure the location and available resources "
        "from the assessment panel to begin."
    )

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:

        with st.container(border=True):

            st.caption("01")

            st.subheader(
                "Observe"
            )

            st.write(
                "Analyze local environmental conditions "
                "and short-term trends."
            )

    with c2:

        with st.container(border=True):

            st.caption("02")

            st.subheader(
                "Evaluate"
            )

            st.write(
                "Compare environmental opportunity "
                "against available resources."
            )

    with c3:

        with st.container(border=True):

            st.caption("03")

            st.subheader(
                "Decide"
            )

            st.write(
                "Identify a practical intervention "
                "and explore alternative scenarios."
            )

    st.divider()

    st.caption(
        "EcoLens · Environmental Decision Intelligence"
    )

    st.stop()


# ============================================================
# DATA LOAD
# ============================================================

with st.spinner(
    "Retrieving environmental conditions..."
):

    profile = get_environmental_profile(
        city
    )

weather = profile["weather"]
air_quality = profile["air_quality"]

current = weather["current"]
daily = weather["daily"]

air_current = (
    air_quality["current"]
)

temperature = (
    current["temperature_2m"]
)

humidity = (
    current["relative_humidity_2m"]
)

aqi = (
    air_current["us_aqi"]
)

pm25 = (
    air_current["pm2_5"]
)

total_rain = sum(
    daily["precipitation_sum"]
)


# ============================================================
# CURRENT DECISION
# ============================================================

with st.spinner(
    "Evaluating intervention opportunities..."
):

    recommendation = (
        generate_recommendation(
            temperature=temperature,
            humidity=humidity,
            aqi=aqi,
            total_rain=total_rain,
            budget=budget,
            solar=solar,
        )
    )


# ============================================================
# ASSESSMENT HEADER
# ============================================================

st.caption(
    "ASSESSMENT"
)

location_col, budget_col = st.columns(
    [3, 1]
)

with location_col:

    st.header(
        city
    )

    if (
        profile["data_status"]
        == "live"
    ):

        st.caption(
            "Live environmental data"
        )

    else:

        st.warning(
            "Environmental API unavailable — "
            "using demonstration fallback data."
        )


with budget_col:

    st.metric(
        "Available budget",
        f"${budget:,}"
    )


# ============================================================
# DECISION SUMMARY
# ============================================================

st.caption(
    "DECISION SUMMARY"
)

summary_col1, summary_col2, summary_col3 = (
    st.columns(3)
)

with summary_col1:

    st.metric(
        "Recommended",
        recommendation[
            "recommendation"
        ]
    )

with summary_col2:

    st.metric(
        "Opportunity",
        f"{recommendation['decision_score']}/100"
    )

with summary_col3:

    st.metric(
        "Estimated annual savings",
        f"${recommendation['annual_savings']:,}"
    )


# ============================================================
# ENVIRONMENTAL SNAPSHOT
# ============================================================

st.caption(
    "ENVIRONMENTAL SNAPSHOT"
)

st.header(
    "Local Conditions"
)

e1, e2, e3, e4 = (
    st.columns(4)
)

with e1:

    st.metric(
        "Temperature",
        f"{temperature:.1f} °C"
    )

    if temperature >= 30:

        st.caption(
            "Elevated heat opportunity"
        )

    elif temperature >= 25:

        st.caption(
            "Moderate heat opportunity"
        )

    else:

        st.caption(
            "Lower heat opportunity"
        )


with e2:

    st.metric(
        "Air Quality",
        f"{aqi:.0f}"
    )

    if aqi <= 50:

        st.caption(
            "Good air quality"
        )

    elif aqi <= 100:

        st.caption(
            "Moderate air quality"
        )

    else:

        st.caption(
            "Elevated air-quality pressure"
        )


with e3:

    st.metric(
        "Humidity",
        f"{humidity:.0f}%"
    )

    if humidity >= 70:

        st.caption(
            "High humidity"
        )

    elif humidity >= 45:

        st.caption(
            "Moderate humidity"
        )

    else:

        st.caption(
            "Lower humidity"
        )


with e4:

    st.metric(
        "7-Day Precipitation",
        f"{total_rain:.1f} mm"
    )

    if total_rain >= 40:

        st.caption(
            "Higher precipitation"
        )

    elif total_rain >= 15:

        st.caption(
            "Moderate precipitation"
        )

    else:

        st.caption(
            "Lower precipitation"
        )


# ============================================================
# TEMPERATURE TREND
# ============================================================

st.caption(
    "ENVIRONMENTAL TREND"
)

st.header(
    "Temperature Forecast"
)

forecast_df = pd.DataFrame(
    {
        "Date": daily["time"],
        "Temperature": daily[
            "temperature_2m_max"
        ],
    }
)

average_temperature = (
    forecast_df["Temperature"]
    .mean()
)

if (
    len(forecast_df) >= 2
):

    trend_change = (
        forecast_df["Temperature"].iloc[-1]
        - forecast_df["Temperature"].iloc[0]
    )

else:

    trend_change = 0


if trend_change > 1:

    trend_label = (
        "Warming trend"
    )

elif trend_change < -1:

    trend_label = (
        "Cooling trend"
    )

else:

    trend_label = (
        "Relatively stable"
    )


trend_col1, trend_col2 = (
    st.columns([3, 1])
)

with trend_col1:

    forecast_fig = go.Figure()

    forecast_fig.add_trace(
        go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Temperature"],
            mode="lines+markers",
            line={
                "color": "#1D8F62",
                "width": 3,
            },
            marker={
                "color": "#1D8F62",
                "size": 7,
            },
            hovertemplate=(
                "%{x}<br>"
                "%{y:.1f} °C"
                "<extra></extra>"
            ),
        )
    )

    forecast_fig.update_layout(
        height=310,
        margin={
            "l": 15,
            "r": 15,
            "t": 20,
            "b": 15,
        },
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={
            "color": "#60726A"
        },
        xaxis={
            "title": None,
            "gridcolor": "#E8EEE9",
        },
        yaxis={
            "title": "Temperature (°C)",
            "gridcolor": "#E8EEE9",
        },
    )

    st.plotly_chart(
        forecast_fig,
        width="stretch",
    )


with trend_col2:

    with st.container(
        border=True
    ):

        st.metric(
            "7-Day Average",
            f"{average_temperature:.1f} °C"
        )

        st.metric(
            "Trend",
            trend_label
        )

        st.caption(
            "Trend interpretation is a simplified "
            "short-term signal."
        )


# ============================================================
# DECISION ENGINE
# ============================================================

st.divider()

st.caption(
    "DECISION ENGINE"
)

st.header(
    "Recommended Intervention"
)

recommendation_col, score_col = (
    st.columns([3, 1])
)

with recommendation_col:

    with st.container(
        border=True
    ):

        st.caption(
            "RECOMMENDED ACTION"
        )

        st.subheader(
            recommendation[
                "recommendation"
            ]
        )

        st.write(
            recommendation[
                "reason"
            ]
        )

        st.write("")

        r1, r2, r3, r4 = (
            st.columns(4)
        )

        with r1:

            st.metric(
                "Estimated cost",
                f"${recommendation['estimated_cost']:,}"
            )

        with r2:

            st.metric(
                "Annual savings",
                f"${recommendation['annual_savings']:,}"
            )

        with r3:

            st.metric(
                "Impact",
                recommendation[
                    "impact"
                ]
            )

        with r4:

            st.metric(
                "Confidence",
                f"{recommendation['confidence']}%"
            )


with score_col:

    with st.container(
        border=True
    ):

        st.metric(
            "Opportunity Score",
            f"{recommendation['decision_score']}/100"
        )

        st.progress(
            recommendation[
                "decision_score"
            ] / 100
        )

        st.caption(
            "Composite decision score based on "
            "environmental opportunity, impact, "
            "affordability, and feasibility."
        )


# ============================================================
# DECISION FACTORS
# ============================================================

st.caption(
    "DECISION FACTORS"
)

st.header(
    "Why the engine selected this option"
)

d1, d2, d3, d4 = (
    st.columns(4)
)

with d1:

    st.metric(
        "Heat opportunity",
        f"{recommendation['heat_score']}/100"
    )

with d2:

    st.metric(
        "Solar potential",
        f"{recommendation['solar_score']}/100"
    )

with d3:

    st.metric(
        "Budget fit",
        f"{recommendation['budget_score']}/100"
    )

with d4:

    st.metric(
        "Feasibility",
        f"{recommendation['ranked_interventions'][0]['feasibility']}/100"
    )


# ============================================================
# CURRENT INTERVENTION RANKING
# ============================================================

st.caption(
    "INTERVENTION COMPARISON"
)

st.header(
    "How EcoLens ranked the options"
)

st.write(
    "The engine evaluates environmental opportunity, "
    "environmental impact, affordability, and "
    "implementation feasibility."
)

ranked = (
    recommendation[
        "ranked_interventions"
    ]
)

current_rows = []

for index, item in enumerate(
    ranked
):

    current_rows.append(
        {
            "Rank": index + 1,
            "Intervention": item["name"],
            "Score": item["score"],
            "Cost": f"${item['cost']:,}",
            "Annual Savings": f"${item['annual_savings']:,}",
            "Impact": item["impact"],
            "Affordability": item["affordability"],
            "Feasibility": item["feasibility"],
        }
    )

current_df = pd.DataFrame(
    current_rows
)

st.dataframe(
    current_df,
    width="stretch",
    hide_index=True,
    column_config={
        "Rank": st.column_config.NumberColumn(
            "Rank"
        ),

        "Intervention": st.column_config.TextColumn(
            "Intervention"
        ),

        "Score": st.column_config.ProgressColumn(
            "Opportunity",
            min_value=0,
            max_value=100,
            format="%d/100"
        ),

        "Cost": st.column_config.TextColumn(
            "Estimated Cost"
        ),

        "Annual Savings": st.column_config.TextColumn(
            "Annual Savings"
        ),

        "Impact": st.column_config.TextColumn(
            "Impact"
        ),

        "Affordability": st.column_config.ProgressColumn(
            "Affordability",
            min_value=0,
            max_value=100,
            format="%d/100"
        ),

        "Feasibility": st.column_config.ProgressColumn(
            "Feasibility",
            min_value=0,
            max_value=100,
            format="%d/100"
        ),
    }
)


# ============================================================
# DECISION BASIS
# ============================================================

st.caption(
    "DECISION BASIS"
)

basis1, basis2, basis3 = (
    st.columns(3)
)

with basis1:

    st.metric(
        "Environmental opportunity",
        f"{ranked[0]['environmental_opportunity']}/100"
    )

with basis2:

    st.metric(
        "Affordability",
        f"{ranked[0]['affordability']}/100"
    )

with basis3:

    st.metric(
        "Implementation feasibility",
        f"{ranked[0]['feasibility']}/100"
    )


# ============================================================
# SCENARIO ANALYSIS
# ============================================================

st.divider()

st.caption(
    "SCENARIO ANALYSIS"
)

st.header(
    "Explore the decision"
)

st.write(
    "Change available resources and see how the "
    "recommendation, ranking, and opportunity score respond."
)

scenario_left, scenario_right = (
    st.columns([1, 1.35])
)

with scenario_left:

    with st.container(
        border=True
    ):

        st.caption(
            "WHAT-IF SIMULATOR"
        )

        st.subheader(
            "Change available resources"
        )

        scenario_budget = st.slider(
            "Scenario budget",
            1000,
            25000,
            budget,
            step=1000,
            format="$%d",
            key="scenario_budget",
        )

        st.metric(
            "Scenario budget",
            f"${scenario_budget:,}"
        )


scenario = evaluate_scenario(
    temperature=temperature,
    humidity=humidity,
    aqi=aqi,
    total_rain=total_rain,
    budget=scenario_budget,
    solar=solar,
)

with scenario_right:

    with st.container(
        border=True
    ):

        st.caption(
            "SCENARIO RESULT"
        )

        st.subheader(
            scenario[
                "recommendation"
            ]
        )

        s1, s2, s3 = (
            st.columns(3)
        )

        with s1:

            st.metric(
                "Opportunity",
                f"{scenario['decision_score']}/100"
            )

        with s2:

            st.metric(
                "Cost",
                f"${scenario['estimated_cost']:,}"
            )

        with s3:

            st.metric(
                "Savings",
                f"${scenario['annual_savings']:,}"
            )


# ============================================================
# SCENARIO CHANGE ANALYSIS
# ============================================================

change = compare_decisions(
    recommendation,
    scenario,
)

st.caption(
    "CHANGE FROM CURRENT"
)

change1, change2, change3 = (
    st.columns(3)
)

with change1:

    if (
        change[
            "recommendation_changed"
        ]
    ):

        st.metric(
            "Recommendation",
            scenario[
                "recommendation"
            ],
            delta="Changed"
        )

    else:

        st.metric(
            "Recommendation",
            scenario[
                "recommendation"
            ],
            delta="No change"
        )


with change2:

    st.metric(
        "Opportunity score",
        f"{scenario['decision_score']}/100",
        delta=(
            f"{change['score_change']:+d}"
        )
    )


with change3:

    st.metric(
        "Annual savings",
        f"${scenario['annual_savings']:,}",
        delta=(
            f"${change['savings_change']:+,}"
        )
    )


# ============================================================
# WHY DID IT CHANGE?
# ============================================================

with st.container(
    border=True
):

    st.caption(
        "WHY DID THE DECISION CHANGE?"
    )

    if (
        change[
            "recommendation_changed"
        ]
    ):

        st.write(
            f"EcoLens changed the recommendation "
            f"from **{change['current_name']}** "
            f"to **{change['scenario_name']}**."
        )

    else:

        st.write(
            "The recommended intervention remained "
            "the same under this budget scenario."
        )

    for reason in change["reasons"]:

        st.write(
            f"• {reason.capitalize()}."
        )


# ============================================================
# DECISION BOUNDARY
# ============================================================

boundary_budget, boundary_scenario = (
    find_decision_boundary(
        temperature=temperature,
        humidity=humidity,
        aqi=aqi,
        total_rain=total_rain,
        solar=solar,
        current_recommendation=(
            recommendation[
                "recommendation"
            ]
        ),
        minimum_budget=budget + 1000,
        maximum_budget=25000,
        step=1000,
    )
)


if boundary_budget is not None:

    with st.container(
        border=True
    ):

        st.caption(
            "DECISION THRESHOLD"
        )

        st.write(
            f"At approximately **${boundary_budget:,}** "
            f"in available resources, EcoLens first "
            f"changes the recommendation to "
            f"**{boundary_scenario['recommendation']}**."
        )

else:

    st.caption(
        "No recommendation change detected within "
        "the tested budget range."
    )


# ============================================================
# SCENARIO RANKING
# ============================================================

st.caption(
    "SCENARIO RANKING"
)

scenario_ranked = (
    scenario[
        "ranked_interventions"
    ]
)

scenario_rows = []

for index, item in enumerate(
    scenario_ranked
):

    scenario_rows.append(
        {
            "Rank": index + 1,
            "Intervention": item["name"],
            "Score": item["score"],
            "Cost": f"${item['cost']:,}",
            "Savings": f"${item['annual_savings']:,}",
            "Affordability": item["affordability"],
            "Feasibility": item["feasibility"],
        }
    )

scenario_df = pd.DataFrame(
    scenario_rows
)

st.dataframe(
    scenario_df,
    width="stretch",
    hide_index=True,
    column_config={
        "Rank": st.column_config.NumberColumn(
            "Rank"
        ),

        "Intervention": st.column_config.TextColumn(
            "Intervention"
        ),

        "Score": st.column_config.ProgressColumn(
            "Opportunity",
            min_value=0,
            max_value=100,
            format="%d/100"
        ),

        "Cost": st.column_config.TextColumn(
            "Estimated Cost"
        ),

        "Savings": st.column_config.TextColumn(
            "Annual Savings"
        ),

        "Affordability": st.column_config.ProgressColumn(
            "Affordability",
            min_value=0,
            max_value=100,
            format="%d/100"
        ),

        "Feasibility": st.column_config.ProgressColumn(
            "Feasibility",
            min_value=0,
            max_value=100,
            format="%d/100"
        ),
    }
)


# ============================================================
# SCENARIO SCORE CHART
# ============================================================

scenario_names = [
    item["name"]
    for item in scenario_ranked
]

scenario_scores = [
    item["score"]
    for item in scenario_ranked
]

scenario_fig = go.Figure()

scenario_fig.add_trace(
    go.Bar(
        x=scenario_scores,
        y=scenario_names,
        orientation="h",
        marker_color="#1D8F62",
        text=[
            f"{score}/100"
            for score in scenario_scores
        ],
        textposition="outside",
        hovertemplate=(
            "%{y}<br>"
            "Opportunity Score: %{x}/100"
            "<extra></extra>"
        ),
    )
)

scenario_fig.update_layout(
    height=320,
    margin={
        "l": 15,
        "r": 70,
        "t": 15,
        "b": 15,
    },
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    font={
        "color": "#60726A"
    },
    xaxis={
        "range": [0, 105],
        "title": "Opportunity Score",
        "gridcolor": "#E8EEE9",
    },
    yaxis={
        "title": None,
        "categoryorder": "total ascending",
    },
    showlegend=False,
)

st.plotly_chart(
    scenario_fig,
    width="stretch",
)


# ============================================================
# LOCATION MAP
# ============================================================

st.caption(
    "LOCATION CONTEXT"
)

st.header(
    "Assessment Location"
)

map_df = pd.DataFrame(
    {
        "latitude": [
            profile["latitude"]
        ],
        "longitude": [
            profile["longitude"]
        ],
        "location": [
            city
        ],
    }
)

map_fig = go.Figure()

map_fig.add_trace(
    go.Scattergeo(
        lat=map_df["latitude"],
        lon=map_df["longitude"],
        text=map_df["location"],
        mode="markers",
        marker={
            "size": 14,
            "color": "#1D8F62",
        },
        hovertemplate=(
            "%{text}"
            "<extra></extra>"
        ),
    )
)

map_fig.update_geos(
    scope="usa",
    showcountries=True,
    showland=True,
    landcolor="#EEF2EC",
    countrycolor="#C9D5CC",
    showsubunits=True,
    subunitcolor="#DCE4DC",
)

map_fig.update_layout(
    height=320,
    margin={
        "l": 0,
        "r": 0,
        "t": 10,
        "b": 0,
    },
    paper_bgcolor="#FFFFFF",
)

st.plotly_chart(
    map_fig,
    width="stretch",
)


# ============================================================
# EVIDENCE
# ============================================================

st.caption(
    "EVIDENCE"
)

st.header(
    "What is measured vs. estimated?"
)

evidence_df = pd.DataFrame(
    {
        "Input": [
            "Temperature",
            "Humidity",
            "Air Quality",
            "PM2.5",
            "Precipitation",
            "Available Budget",
            "Estimated Cost",
            "Estimated Savings",
        ],
        "Value": [
            f"{temperature:.1f} °C",
            f"{humidity:.0f}%",
            f"{aqi:.0f}",
            f"{pm25:.1f}",
            f"{total_rain:.1f} mm",
            f"${budget:,}",
            f"${recommendation['estimated_cost']:,}",
            f"${recommendation['annual_savings']:,}",
        ],
        "Classification": [
            "Measured",
            "Measured",
            "Measured",
            "Measured",
            "Measured",
            "User input",
            "Model estimate",
            "Model estimate",
        ],
    }
)

st.dataframe(
    evidence_df,
    width="stretch",
    hide_index=True,
)


# ============================================================
# EXPLAINABLE AI
# ============================================================

st.divider()

st.caption(
    "EXPLAINABLE AI"
)

st.header(
    "Decision Rationale"
)

st.write(
    "The AI explanation layer interprets the evidence "
    "produced by the deterministic decision engine."
)

with st.spinner(
    "Preparing decision rationale..."
):

    explanation = generate_explanation(
        temperature=temperature,
        humidity=humidity,
        aqi=aqi,
        pm25=pm25,
        precipitation=total_rain,
        budget=budget,
        recommendation=(
            recommendation[
                "recommendation"
            ]
        ),
        recommendation_cost=(
            recommendation[
                "estimated_cost"
            ]
        ),
        decision_score=(
            recommendation[
                "decision_score"
            ]
        ),
        heat_score=(
            recommendation[
                "heat_score"
            ]
        ),
        solar_score=(
            recommendation[
                "solar_score"
            ]
        ),
        ranked_interventions=(
            recommendation[
                "ranked_interventions"
            ]
        ),
    )


with st.container(
    border=True
):

    st.write(
        explanation
    )


# ============================================================
# METHODOLOGY
# ============================================================

with st.expander(
    "Methodology and limitations"
):

    st.subheader(
        "Environmental data"
    )

    st.write(
        "EcoLens retrieves current environmental "
        "conditions and short-term forecast information."
    )

    st.subheader(
        "Decision engine"
    )

    st.write(
        "A deterministic scoring system evaluates "
        "environmental opportunity, environmental "
        "impact, affordability, and implementation "
        "feasibility."
    )

    st.subheader(
        "Scenario engine"
    )

    st.write(
        "The scenario engine recalculates the intervention "
        "ranking as available resources change."
    )

    st.subheader(
        "Explainable AI"
    )

    st.write(
        "AI interprets the decision engine's output. "
        "It does not generate the underlying environmental "
        "measurements or financial estimates."
    )

    st.subheader(
        "Uncertainty"
    )

    st.write(
        "Cost, savings, and environmental impact values "
        "are simplified demonstration estimates. Actual "
        "project outcomes require site-specific engineering, "
        "financial, and environmental validation."
    )


# ============================================================
# NEW ASSESSMENT
# ============================================================

st.divider()

if st.button(
    "Start New Assessment",
    width="stretch",
):

    st.session_state.assessment_started = False

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "EcoLens · Environmental Decision Intelligence"
)

st.caption(
    "Data sources: Open-Meteo environmental services. "
    "Financial and intervention estimates are simplified "
    "demonstration assumptions."
)