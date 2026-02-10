from sheets import read_sheet
import pandas as pd
from urgent_reassignment import suggest_urgent_reassignment

pilots, _ = read_sheet("pilot_roster")
drones, _ = read_sheet("drone_fleet")
missions = pd.read_csv("missions.csv")

pilots_df = pd.DataFrame(pilots)
drones_df = pd.DataFrame(drones)

mission = missions.iloc[0]

mission["priority"] = "Urgent"
if mission["priority"].lower() == "urgent":
    print("\n⚠️ Urgent mission detected. Reassignment suggestions:\n")
    suggestions = suggest_urgent_reassignment(pilots_df, drones_df, mission)

    for s in suggestions:
        print(f"- {s['type']}: {s['name']}")
        print(f"  Reason: {s['reason']}")
        print(f"  Risk: {s['risk']}\n")
else:
    print("Mission is not urgent")

