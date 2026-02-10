from datetime import datetime

def parse_list(val):
    return [v.strip().lower() for v in val.split(",")]

def date_overlap(pilot_date, mission_start):
    return pilot_date <= mission_start

def score_pilot(pilot, mission):
    score = 0
    reasons = []

    pilot_skills = parse_list(pilot["skills"])
    mission_skills = parse_list(mission["required_skills"])

    for skill in mission_skills:
        if skill in pilot_skills:
            score += 2
            reasons.append(f"Skill match: {skill}")

    pilot_certs = parse_list(pilot["certifications"])
    mission_certs = parse_list(mission["required_certs"])

    for cert in mission_certs:
        if cert in pilot_certs:
            score += 2
            reasons.append(f"Certification match: {cert}")

    if pilot["location"].lower() == mission["location"].lower():
        score += 1
        reasons.append("Location match")

    pilot_available = datetime.strptime(pilot["available_from"], "%Y-%m-%d")
    mission_start = datetime.strptime(mission["start_date"], "%Y-%m-%d")

    if date_overlap(pilot_available, mission_start):
        score += 1
        reasons.append("Available before mission start")

    return score, reasons
