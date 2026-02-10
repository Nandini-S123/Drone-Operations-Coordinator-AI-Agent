from datetime import datetime

def parse_list(val):
    return [v.strip().lower() for v in val.split(",")]

def detect_drone_conflicts(drone, mission):
    conflicts = []
    warnings = []

    # 1. Status conflict
    if drone["status"].lower() == "maintenance":
        conflicts.append("Drone is under maintenance")

    if drone["status"].lower() == "deployed":
        conflicts.append("Drone already deployed to another project")

    # 2. Capability mismatch
    drone_caps = parse_list(drone["capabilities"])
    mission_skills = parse_list(mission["required_skills"])

    missing_caps = [
        s for s in mission_skills if s not in drone_caps
    ]

    if missing_caps:
        conflicts.append(
            f"Drone lacks required capabilities: {', '.join(missing_caps)}"
        )

    # 3. Location mismatch (soft conflict)
    if drone["location"].lower() != mission["location"].lower():
        warnings.append("Drone is in a different location")

    # 4. Maintenance due soon (soft warning)
    if drone.get("maintenance_due"):
        due = datetime.strptime(drone["maintenance_due"], "%Y-%m-%d")
        if (due - datetime.today()).days <= 7:
            warnings.append("Drone maintenance due within 7 days")

    return conflicts, warnings
