def suggest_urgent_reassignment(pilots_df, drones_df, mission):
    suggestions = []

    # Strategy 1: Allow pilot location mismatch
    for _, pilot in pilots_df.iterrows():
        if pilot["status"] == "Available":
            suggestions.append({
                "type": "Pilot reassignment",
                "name": pilot["name"],
                "reason": "Available pilot, location mismatch allowed",
                "risk": "Travel delay"
            })

    # Strategy 2: Reassign from low-priority mission
    for _, pilot in pilots_df.iterrows():
        if pilot["status"] == "Assigned":
            suggestions.append({
                "type": "Pilot reassignment",
                "name": pilot["name"],
                "reason": "Reassign from lower priority mission",
                "risk": "Downstream conflict"
            })

    # Strategy 3: Use drone with partial capability
    for _, drone in drones_df.iterrows():
        if drone["status"] == "Available":
            suggestions.append({
                "type": "Drone substitution",
                "name": drone["drone_id"],
                "reason": "Partial capability match",
                "risk": "Reduced mission quality"
            })

    return suggestions
