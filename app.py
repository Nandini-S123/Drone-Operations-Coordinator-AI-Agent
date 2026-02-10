import streamlit as st
import pandas as pd

from sheets import read_sheet, update_pilot_status
from roster import (
    filter_available_pilots,
    filter_by_skill,
    filter_by_location
)
from matching import score_pilot
from conflicts import detect_pilot_conflicts
from drone_inventory import detect_drone_conflicts
from urgent_reassignment import suggest_urgent_reassignment

st.set_page_config(page_title="Drone Ops Coordinator AI", layout="wide")
st.title("🚁 Drone Operations Coordinator AI Agent")

# Load data
pilots, pilot_sheet = read_sheet("pilot_roster")
drones, _ = read_sheet("drone_fleet")
missions = pd.read_csv("missions.csv")

pilots_df = pd.DataFrame(pilots)
drones_df = pd.DataFrame(drones)

# Chat input
user_query = st.text_input("Ask the agent")

st.divider()

# -------- QUERY HANDLERS --------

if user_query:
    q = user_query.lower()

    # 1. Available pilots
    if "available pilots" in q:
        result = filter_available_pilots(pilots_df)
        st.subheader("Available Pilots")
        st.dataframe(result)

    # 2. Pilot skill query
    elif "pilots with" in q and "skill" in q:
        skill = q.split("with")[-1].replace("skill", "").strip()
        result = filter_by_skill(pilots_df, skill)
        st.subheader(f"Pilots with skill: {skill}")
        st.dataframe(result)

    # 3. Match pilots to mission
    elif "match pilots for" in q:
        project_id = q.split("for")[-1].strip().upper()
        mission = missions[missions["project_id"] == project_id].iloc[0]

        st.subheader(f"Pilot matches for {project_id}")

        for _, pilot in pilots_df.iterrows():
            score, reasons = score_pilot(pilot, mission)
            if score > 0:
                st.markdown(f"**{pilot['name']} — Score {score}**")
                for r in reasons:
                    st.write("•", r)

    # 4. Why mission cannot be assigned
    elif "why" in q and "mission" in q:
        project_id = q.split()[-1].upper()
        mission = missions[missions["project_id"] == project_id].iloc[0]

        st.subheader(f"Conflicts for mission {project_id}")

        for _, pilot in pilots_df.iterrows():
            conflicts, warnings = detect_pilot_conflicts(pilot, mission)
            if conflicts or warnings:
                st.markdown(f"**{pilot['name']}**")
                for c in conflicts:
                    st.error(c)
                for w in warnings:
                    st.warning(w)

        for _, drone in drones_df.iterrows():
            conflicts, warnings = detect_drone_conflicts(drone, mission)
            if conflicts or warnings:
                st.markdown(f"**Drone {drone['drone_id']}**")
                for c in conflicts:
                    st.error(c)
                for w in warnings:
                    st.warning(w)

    # 5. Urgent reassignment
    elif "urgent" in q:
        project_id = q.split()[-1].upper()
        mission = missions[missions["project_id"] == project_id].iloc[0]

        st.subheader("⚠️ Urgent Reassignment Suggestions")

        suggestions = suggest_urgent_reassignment(
            pilots_df, drones_df, mission
        )

        for s in suggestions:
            st.markdown(f"**{s['type']} — {s['name']}**")
            st.write("Reason:", s["reason"])
            st.warning("Risk: " + s["risk"])

    # 6. Update pilot status
    elif "update pilot" in q:
        parts = q.split()
        pilot_id = parts[2].upper()
        new_status = parts[-1].capitalize()

        if st.button("Confirm status update"):
            success = update_pilot_status(
                pilot_sheet, pilot_id, new_status
            )
            if success:
                st.success("Pilot status updated successfully")
            else:
                st.error("Pilot ID not found")

    else:
        st.info("I can help with pilot availability, matching, conflicts, and urgent reassignments.")
