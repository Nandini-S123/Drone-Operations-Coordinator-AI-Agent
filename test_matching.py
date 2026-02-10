from sheets import read_sheet
import pandas as pd
from matching import score_pilot

pilots, _ = read_sheet("pilot_roster")
missions = pd.read_csv("missions.csv")

pilots_df = pd.DataFrame(pilots)
mission = missions.iloc[0]

print(f"\nMatching pilots for mission {mission['project_id']}:\n")

for _, pilot in pilots_df.iterrows():
    score, reasons = score_pilot(pilot, mission)
    if score > 0:
        print(f"{pilot['name']} → Score: {score}")
        for r in reasons:
            print(" -", r)
        print()
