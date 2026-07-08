import streamlit as st
import pandas as pd
import plotly.express as px

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BMTC Transportation Analysis",
    page_icon="🚌",
    layout="wide",
)

st.title("🚌 BMTC Transportation Analysis")
st.markdown(
    "Interactive dashboard exploring Bengaluru's public bus network using GTFS data — "
    "surfacing the busiest routes, stops, and hours across the system."
)

# ─────────────────────────────────────────────────────────────
# SIDEBAR — DATA SOURCE
# ─────────────────────────────────────────────────────────────
st.sidebar.header("Data Source")
mode = st.sidebar.radio(
    "Choose how to load data:",
    ["Quick View (processed summary CSVs)", "Full Pipeline (raw GTFS files)"],
    help="Quick View loads pre-computed results instantly. Full Pipeline reruns the "
         "cleaning + aggregation logic live on raw GTFS files.",
)

top_n = st.sidebar.slider("Number of items to show per chart", min_value=3, max_value=10, value=10)


@st.cache_data
def load_summary_csv(uploaded_file):
    return pd.read_csv(uploaded_file)


@st.cache_data
def run_full_pipeline(routes_file, stop_times_file, stops_file, trips_file):
    """Recreates the original cleaning + aggregation pipeline on raw GTFS files."""
    df2 = pd.read_csv(routes_file)
    drop_cols = [c for c in ["route_desc", "route_url", "agency_id",
                              "route_color", "route_text_color", "route_type"] if c in df2.columns]
    df2 = df2.drop(columns=drop_cols)

    df3 = pd.read_csv(stop_times_file)
    drop_cols = [c for c in ["shape_dist_traveled", "stop_headsign",
                              "drop_off_type", "pickup_type", "timepoint"] if c in df3.columns]
    df3 = df3.drop(columns=drop_cols)

    df4 = pd.read_csv(stops_file, index_col=False)
    drop_cols = [c for c in ["location_type", "parent_station", "stop_code", "stop_desc",
                              "stop_timezone", "stop_url", "wheelchair_boarding", "zone_id"] if c in df4.columns]
    df4 = df4.drop(columns=drop_cols)

    df5 = pd.read_csv(trips_file, index_col=False)
    drop_cols = [c for c in ["bikes_allowed", "block_id", "shape_id",
                              "trip_headsign", "trip_short_name", "wheelchair_accessible"] if c in df5.columns]
    df5 = df5.drop(columns=drop_cols)

    busiest_routes = df5["route_id"].value_counts().head(10).reset_index()
    busiest_routes = pd.merge(busiest_routes, df2, on="route_id")

    busiest_stops = df3["stop_id"].value_counts().head(10).reset_index()
    busiest_stops = pd.merge(busiest_stops, df4, on="stop_id")
    busiest_stops = busiest_stops.drop(columns=[c for c in ["stop_lat", "stop_lon"] if c in busiest_stops.columns])

    df3["hour"] = df3["arrival_time"].str.split(":").str[0]
    busiest_hours = df3["hour"].value_counts().head(10).reset_index()
    busiest_hours["hour"] = busiest_hours["hour"].astype(int)
    busiest_hours = busiest_hours.sort_values("hour")

    return busiest_routes, busiest_stops, busiest_hours


routes_df = stops_df = hours_df = None

if mode.startswith("Quick View"):
    st.sidebar.subheader("Upload summary files")
    routes_upload = st.sidebar.file_uploader("busiest_routes.csv", type="csv", key="r")
    stops_upload = st.sidebar.file_uploader("busiest_stops.csv", type="csv", key="s")
    hours_upload = st.sidebar.file_uploader("peak_hours.csv", type="csv", key="h")

    if routes_upload:
        routes_df = load_summary_csv(routes_upload)
    if stops_upload:
        stops_df = load_summary_csv(stops_upload)
    if hours_upload:
        hours_df = load_summary_csv(hours_upload)

else:
    st.sidebar.subheader("Upload raw GTFS files")
    routes_raw = st.sidebar.file_uploader("routes.csv", type="csv", key="rr")
    stop_times_raw = st.sidebar.file_uploader("stop_times.csv", type="csv", key="st")
    stops_raw = st.sidebar.file_uploader("stops.csv", type="csv", key="sr")
    trips_raw = st.sidebar.file_uploader("trips.csv", type="csv", key="tr")

    if routes_raw and stop_times_raw and stops_raw and trips_raw:
        with st.spinner("Running cleaning + aggregation pipeline..."):
            routes_df, stops_df, hours_df = run_full_pipeline(
                routes_raw, stop_times_raw, stops_raw, trips_raw
            )
        st.sidebar.success("Pipeline complete ✓")
    else:
        st.sidebar.info("Upload all four raw GTFS files to run the pipeline.")

# ─────────────────────────────────────────────────────────────
# EMPTY STATE
# ─────────────────────────────────────────────────────────────
if routes_df is None and stops_df is None and hours_df is None:
    st.info("👈 Upload your data files in the sidebar to get started.")
    st.markdown("""
    **Expected files depending on mode:**
    - *Quick View*: `busiest_routes.csv`, `busiest_stops.csv`, `peak_hours.csv`
    - *Full Pipeline*: `routes.csv`, `stop_times.csv`, `stops.csv`, `trips.csv`
    """)
    st.stop()

# ─────────────────────────────────────────────────────────────
# KEY METRICS ROW
# ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
if routes_df is not None:
    col1.metric("Top Route", str(routes_df.iloc[0]["route_id"]), f"{routes_df.iloc[0]['count']} trips")
if stops_df is not None:
    col2.metric("Top Stop", str(stops_df.iloc[0]["stop_name"]), f"{stops_df.iloc[0]['count']} trips")
if hours_df is not None:
    peak_row = hours_df.sort_values("count", ascending=False).iloc[0]
    col3.metric("Peak Hour", f"{int(peak_row['hour'])}:00", f"{peak_row['count']} trips")

st.divider()

# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🛣️ Busiest Routes", "📍 Busiest Stops", "⏰ Busiest Hours", "📝 Findings"])

with tab1:
    st.subheader("Top BMTC Routes by Trip Count")
    if routes_df is not None:
        d = routes_df.sort_values("count", ascending=True).tail(top_n)
        fig = px.bar(
            d, x="count", y="route_id", orientation="h",
            color="count", color_continuous_scale="Purples",
            labels={"count": "Number of Trips", "route_id": "Route ID"},
            text="count",
        )
        fig.update_layout(height=500, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("View raw data"):
            st.dataframe(routes_df, use_container_width=True)
        st.download_button("Download chart data (CSV)", routes_df.to_csv(index=False), "busiest_routes.csv")
    else:
        st.warning("Upload route data to view this chart.")

with tab2:
    st.subheader("Top BMTC Stops by Trip Count")
    if stops_df is not None:
        d = stops_df.sort_values("count", ascending=True).tail(top_n)
        fig = px.bar(
            d, x="count", y="stop_name", orientation="h",
            color="count", color_continuous_scale="Purples",
            labels={"count": "Number of Trips", "stop_name": "Stop Name"},
            text="count",
        )
        fig.update_layout(height=500, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("View raw data"):
            st.dataframe(stops_df, use_container_width=True)
        st.download_button("Download chart data (CSV)", stops_df.to_csv(index=False), "busiest_stops.csv")
    else:
        st.warning("Upload stop data to view this chart.")

with tab3:
    st.subheader("Trip Volume by Hour of Day")
    if hours_df is not None:
        d = hours_df.sort_values("hour")
        fig = px.bar(
            d, x="hour", y="count",
            labels={"hour": "Hour of Day", "count": "Number of Trips"},
            text="count",
        )
        fig.update_traces(marker_color="steelblue")
        fig.update_layout(height=500, xaxis=dict(dtick=1))
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("View raw data"):
            st.dataframe(hours_df, use_container_width=True)
        st.download_button("Download chart data (CSV)", hours_df.to_csv(index=False), "peak_hours.csv")
    else:
        st.warning("Upload hourly data to view this chart.")

with tab4:
    st.subheader("Key Findings")
    st.markdown("""
    Use this space to narrate the "so what" behind each chart — this is what interviewers
    will ask about, so keep it concrete and numbers-driven. For example:

    - **Route concentration**: identify whether trip volume is spread evenly or concentrated
      in a handful of high-frequency routes — this speaks to network design and where
      capacity investment matters most.
    - **Stop-level demand**: the busiest stops likely cluster around transit hubs, business
      districts, or interchange points — worth naming the actual areas once you cross-reference
      stop names with geography.
    - **Time-of-day patterns**: peak hours typically reflect commute windows — check whether
      the data shows a single sharp peak (implying rush-hour strain) or a flatter, more spread
      profile (implying more even fleet utilization through the day).

    *(Replace this section with your actual written findings from the project.)*
    """)

st.divider()
st.caption("Built with Streamlit · BMTC GTFS data · Bengaluru")