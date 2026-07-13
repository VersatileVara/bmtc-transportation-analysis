import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="BMTC Public Transport Analysis",
    page_icon="🚌",
    layout="wide"
)

# ── Title ─────────────────────────────────────────────────────
st.title("🚌 BMTC Public Transport Analysis")
st.markdown("**Bengaluru Metropolitan Transport Corporation — Route & Stop Insights**")
st.markdown("---")

# ── Load Data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    routes = pd.read_csv("busiest_routes.csv")
    stops  = pd.read_csv("busiest_stops.csv")
    hours  = pd.read_csv("peak_hours.csv")
    return routes, stops, hours

routes_df, stops_df, hours_df = load_data()

# Detect trip-count column in routes
count_col = "count" if "count" in routes_df.columns else \
            routes_df.select_dtypes(include="number").columns[0]

# ── KPI Cards ─────────────────────────────────────────────────
st.subheader("📊 Key Highlights")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🚌 Busiest Route",    str(routes_df.iloc[0]["route_id"]))
k2.metric("🔢 Trips (Top Route)", str(int(routes_df.iloc[0][count_col])))
k3.metric("🚏 Busiest Stop",     stops_df.iloc[0]["stop_name"])
k4.metric("👥 Stop Visits",      str(int(stops_df.iloc[0]["count"])))
k5.metric("⏰ Peak Hour",        f"{int(hours_df.iloc[0]['hour']):02d}:00")

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────
col1, col2 = st.columns(2)

# Chart 1 — Busiest Routes
with col1:
    st.subheader("🛣️ Top 10 Busiest Routes")
    fig1 = px.bar(
        routes_df.sort_values(count_col, ascending=True),
        x=count_col, y="route_id",
        orientation="h",
        color=count_col,
        color_continuous_scale="Purples",
        labels={count_col: "Number of Trips", "route_id": "Route"},
        title="Top 10 Busiest BMTC Routes"
    )
    fig1.update_layout(coloraxis_showscale=False, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2 — Busiest Stops
with col2:
    st.subheader("🚏 Top 10 Busiest Stops")
    fig2 = px.bar(
        stops_df.sort_values("count", ascending=True),
        x="count", y="stop_name",
        orientation="h",
        color="count",
        color_continuous_scale="Purples",
        labels={"count": "Number of Visits", "stop_name": "Stop"},
        title="Top 10 Busiest BMTC Stops"
    )
    fig2.update_layout(coloraxis_showscale=False, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# Chart 3 — Peak Hours
st.subheader("⏰ Peak Hour Traffic Pattern")
hours_sorted = hours_df.sort_values("hour").copy()
hours_sorted["hour_label"] = hours_sorted["hour"].astype(str).str.zfill(2) + ":00"
fig3 = px.bar(
    hours_sorted,
    x="hour_label", y="count",
    color="count",
    color_continuous_scale="Blues",
    labels={"count": "Number of Trips", "hour_label": "Hour of Day"},
    title="BMTC Trip Frequency by Hour — Double Peak Pattern (8 AM & 5 PM)"
)
fig3.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── Raw Data Explorer ──────────────────────────────────────────
st.subheader("🔍 Explore Raw Data")
tab1, tab2, tab3 = st.tabs(["Busiest Routes", "Busiest Stops", "Peak Hours"])
with tab1:
    st.dataframe(routes_df, use_container_width=True)
with tab2:
    st.dataframe(stops_df, use_container_width=True)
with tab3:
    st.dataframe(hours_df, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "**Data Source:** BMTC GTFS Open Data &nbsp;|&nbsp; "
    "**Built with:** Python · Pandas · Plotly · Streamlit &nbsp;|&nbsp; "
    "**Author:** Varalakshmi"
)