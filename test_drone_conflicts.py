from sheets import read_sheet
import pandas as pd
from drone_inventory import detect_drone_conflicts

drones, _ = read_sheet("drone_fleet")
missions = pd.read_csv("missions.csv")

drones_df = pd.DataFrame(drones)
mission = missions.iloc[0]

print(f"\nDrone conflict analysis for mission {mission['project_id']}:\n")

for _, drone in drones_df.iterrows():
    conflicts, warnings = detect_drone_conflicts(drone, mission)

    print(f"Drone {drone['drone_id']} ({drone['model']}):")

    if not conflicts and not warnings:
        print(" ✅ No conflicts")

    for c in conflicts:
        print(" ❌", c)

    for w in warnings:
        print(" ⚠️", w)

    print()
