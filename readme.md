# BMTC Transportation Analysis

Analysis of Bangalore Metropolitan Transport Corporation (BMTC) public transit data 
to uncover patterns in routes, stops, and trip schedules.

## Dataset
- Source: Kaggle (BMTC GTFS data, Oct 2024)
- Files: routes, stops, stop_times, trips, routes_with_coordinates

## Status: In Progress 🚧

## What I've done so far
- Profiled all 5 datasets (shape, columns, data types)
- Identified data quality issues:
  - `routes_with_coordinates.csv` has missing latitude/longitude for all rows
  - `routes.csv` had two fully empty columns (`route_desc`, `route_url`) — dropped
- Cleaned `routes.csv` down to 7 usable columns

## Next steps
- Clean remaining files (stops, stop_times, trips)
- Answer key questions: busiest routes, peak hours, route distribution
- Build visualizations
- Power BI dashboard

## Tools
Python, Pandas, Jupyter Notebook