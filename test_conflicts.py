from sheets import read_sheet
import pandas as pd
from conflicts import detect_pilot_conflicts

pilots, _ = read_sheet("pilot_roster")
missions = pd.read_csv("missions.csv")

pilots_df = pd.DataFrame(pilots)
mission = missions.iloc[0]

print(f"\nConflict analysis for mission {mission['project_id']}:\n")

for _, pilot in pilots_df.iterrows():
    conflicts, warnings = detect_pilot_conflicts(pilot, mission)

    print(f"{pilot['name']}:")

    if not conflicts and not warnings:
        print(" ✅ No conflicts")

    for c in conflicts:
        print(" ❌", c)

    for w in warnings:
        print(" ⚠️", w)

    print()
