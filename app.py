import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Detect trip-count column in routes (could be 'count' or 'trip_count')
count_col = "count" if "count" in routes_df.columns else routes_df.select_dtypes(include="number").columns[0]

# ── KPI Cards ─────────────────────────────────────────────────
st.subheader("📊 Key Highlights")
k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("🚌 Busiest Route",  str(routes_df.iloc[0]["route_id"]))
k2.metric("🔢 Trips (Top Route)", str(int(routes_df.iloc[0][count_col])))
k3.metric("🚏 Busiest Stop",  stops_df.iloc[0]["stop_name"].split()[0] + " BS")
k4.metric("👥 Stop Visits",   str(int(stops_df.iloc[0]["count"])))
k5.metric("⏰ Peak Hour",     f"{int(hours_df.iloc[0]['hour']):02d}:00")

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────
col1, col2 = st.columns(2)

# Chart 1 — Busiest Routes
with col1:
    st.subheader("🛣️ Top 10 Busiest Routes")
    fig, ax = plt.subplots(figsize=(7, 5))
    sorted_routes = routes_df.sort_values(count_col, ascending=True)
    colors = plt.cm.Purples(np.linspace(0.4, 0.9, len(sorted_routes)))
    bars = ax.barh(sorted_routes["route_id"], sorted_routes[count_col], color=colors)
    for bar, val in zip(bars, sorted_routes[count_col]):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                str(int(val)), va="center", fontsize=9)
    ax.set_xlabel("Number of Trips")
    ax.set_title("Top 10 Busiest BMTC Routes")
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

# Chart 2 — Busiest Stops
with col2:
    st.subheader("🚏 Top 10 Busiest Stops")
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    sorted_stops = stops_df.sort_values("count", ascending=True)
    colors2 = plt.cm.Purples(np.linspace(0.4, 0.9, len(sorted_stops)))
    bars2 = ax2.barh(sorted_stops["stop_name"], sorted_stops["count"], color=colors2)
    for bar, val in zip(bars2, sorted_stops["count"]):
        ax2.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                 str(int(val)), va="center", fontsize=9)
    ax2.set_xlabel("Number of Stop Visits")
    ax2.set_title("Top 10 Busiest BMTC Stops")
    ax2.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig2)

# Chart 3 — Peak Hours (full width)
st.subheader("⏰ Peak Hour Traffic Pattern")
fig3, ax3 = plt.subplots(figsize=(12, 4))
sorted_hours = hours_df.sort_values("hour")
ax3.bar(sorted_hours["hour"].astype(str).str.zfill(2) + ":00",
        sorted_hours["count"], color="steelblue", edgecolor="white")
ax3.set_xlabel("Hour of Day")
ax3.set_ylabel("Number of Trips")
ax3.set_title("BMTC Trip Frequency by Hour — Double Peak Pattern (8 AM & 5 PM)")
ax3.spines[["top","right"]].set_visible(False)
plt.tight_layout()
st.pyplot(fig3)

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
    "**Built with:** Python · Pandas · Matplotlib · Streamlit &nbsp;|&nbsp; "
    "**Author:** Varalakshmi"
)