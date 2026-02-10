
from sheets import read_sheet, update_pilot_status

records, sheet = read_sheet("pilot_roster")
print("BEFORE:", records[:2])

success = update_pilot_status(sheet, "P001", "On Leave")
print("Update success:", success)

records, _ = read_sheet("pilot_roster")
print("AFTER:", records[:2])
