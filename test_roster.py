from sheets import read_sheet
import pandas as pd
from roster import (
    filter_available_pilots,
    filter_by_skill,
    filter_by_location,
    filter_by_date
)

records, _ = read_sheet("pilot_roster")
pilots_df = pd.DataFrame(records)

print("\nAvailable pilots:")
print(filter_available_pilots(pilots_df)[["pilot_id", "name", "status"]])

print("\nPilots with Mapping skill:")
print(filter_by_skill(pilots_df, "Mapping")[["pilot_id", "name", "skills"]])

print("\nPilots in Bangalore:")
print(filter_by_location(pilots_df, "Bangalore")[["pilot_id", "name", "location"]])

print("\nPilots available by 2026-02-10:")
print(filter_by_date(pilots_df, "2026-02-10")[["pilot_id", "name", "available_from"]])
