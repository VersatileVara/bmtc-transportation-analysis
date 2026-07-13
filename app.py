import streamlit as st
import pandas as pd
import altair as alt

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="BMTC Public Transport Analysis",
    page_icon="🚌",
    layout="wide"
)

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

# Detect count column in routes
count_col = "count" if "count" in routes_df.columns else \
            routes_df.select_dtypes(include="number").columns[0]

# ── KPI Cards ─────────────────────────────────────────────────
st.subheader("📊 Key Highlights")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🚌 Busiest Route",     str(routes_df.iloc[0]["route_id"]))
k2.metric("🔢 Trips (Top Route)", str(int(routes_df.iloc[0][count_col])))
stop_name = stops_df.iloc[0]["stop_name"]
short_name = " ".join(stop_name.split()[:2])  # First 2 words only e.g. "Kempegowda Bus"
k3.metric("🚏 Busiest Stop", short_name + " Stn")
k4.metric("👥 Stop Visits",       str(int(stops_df.iloc[0]["count"])))
k5.metric("⏰ Peak Hour",         f"{int(hours_df.iloc[0]['hour']):02d}:00")

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛣️ Top 10 Busiest Routes")
    fig1 = alt.Chart(routes_df).mark_bar().encode(
        x=alt.X(f"{count_col}:Q", title="Number of Trips"),
        y=alt.Y("route_id:N", sort="-x", title="Route"),
        color=alt.Color(f"{count_col}:Q", scale=alt.Scale(scheme="purples"), legend=None),
        tooltip=["route_id", count_col]
    ).properties(height=350)
    st.altair_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🚏 Top 10 Busiest Stops")
    fig2 = alt.Chart(stops_df).mark_bar().encode(
        x=alt.X("count:Q", title="Number of Visits"),
        y=alt.Y("stop_name:N", sort="-x", title="Stop"),
        color=alt.Color("count:Q", scale=alt.Scale(scheme="purples"), legend=None),
        tooltip=["stop_name", "count"]
    ).properties(height=350)
    st.altair_chart(fig2, use_container_width=True)

st.subheader("⏰ Peak Hour Traffic Pattern")
hours_sorted = hours_df.sort_values("hour").copy()
hours_sorted["hour_label"] = hours_sorted["hour"].astype(str).str.zfill(2) + ":00"
fig3 = alt.Chart(hours_sorted).mark_bar().encode(
    x=alt.X("hour_label:N", title="Hour of Day", sort=None),
    y=alt.Y("count:Q", title="Number of Trips"),
    color=alt.Color("count:Q", scale=alt.Scale(scheme="blues"), legend=None),
    tooltip=["hour_label", "count"]
).properties(height=300, title="Double Peak Pattern — 8 AM & 5 PM Rush Hours")
st.altair_chart(fig3, use_container_width=True)

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

st.markdown("---")
st.markdown("**Data Source:** BMTC GTFS Open Data &nbsp;|&nbsp; **Built with:** Python · Pandas · Altair · Streamlit &nbsp;|&nbsp; **Author:** Varalakshmi")