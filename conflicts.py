from datetime import datetime

def parse_list(val):
    return [v.strip().lower() for v in val.split(",")]

def detect_pilot_conflicts(pilot, mission):
    conflicts = []
    warnings = []

    # 1. Assignment conflict
    if pilot["status"].lower() == "assigned":
        conflicts.append("Pilot already assigned to another project")

    # 2. Availability date conflict
    pilot_available = datetime.strptime(pilot["available_from"], "%Y-%m-%d")
    mission_start = datetime.strptime(mission["start_date"], "%Y-%m-%d")

    if pilot_available > mission_start:
        conflicts.append("Pilot not available before mission start date")

    # 3. Skill mismatch
    pilot_skills = parse_list(pilot["skills"])
    mission_skills = parse_list(mission["required_skills"])

    missing_skills = [
        s for s in mission_skills if s not in pilot_skills
    ]

    if missing_skills:
        conflicts.append(f"Missing required skills: {', '.join(missing_skills)}")

    # 4. Certification mismatch
    pilot_certs = parse_list(pilot["certifications"])
    mission_certs = parse_list(mission["required_certs"])

    missing_certs = [
        c for c in mission_certs if c not in pilot_certs
    ]

    if missing_certs:
        conflicts.append(f"Missing certifications: {', '.join(missing_certs)}")

    # 5. Location mismatch (soft conflict)
    if pilot["location"].lower() != mission["location"].lower():
        warnings.append("Pilot is in a different location")

    return conflicts, warnings
