import pandas as pd
from datetime import datetime

def parse_skills(skills_str):
    return [s.strip().lower() for s in skills_str.split(",")]

def filter_available_pilots(pilots_df):
    return pilots_df[pilots_df["status"] == "Available"]

def filter_by_skill(pilots_df, skill):
    skill = skill.lower()
    return pilots_df[
        pilots_df["skills"].apply(
            lambda x: skill in parse_skills(x)
        )
    ]

def filter_by_location(pilots_df, location):
    return pilots_df[pilots_df["location"].str.lower() == location.lower()]

def filter_by_date(pilots_df, date_str):
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    pilots_df["available_from"] = pd.to_datetime(pilots_df["available_from"])
    return pilots_df[pilots_df["available_from"] <= target_date]
