# Drone Operations Coordinator AI Agent

## Overview
This project implements an AI-powered Drone Operations Coordinator for managing pilots, drones, and missions across multiple client projects. The agent supports pilot assignment, conflict detection, drone inventory validation, and urgent reassignment handling through a conversational interface.

## Architecture
- **Frontend:** Streamlit conversational UI
- **Backend Logic:** Python modules for roster management, matching, conflict detection, and urgent reassignment
- **Data Source:** Google Sheets (pilot roster, drone fleet) and CSV (missions)
- **Authentication:** Google OAuth with credentials managed via Streamlit Secrets

## Key Features
- Query pilot availability by skill, location, and date
- Match pilots to missions with explainable scoring
- Detect pilot and drone conflicts (hard vs soft constraints)
- Track drone availability, maintenance, and capability mismatches
- Handle urgent missions with risk-aware reassignment suggestions
- Two-way Google Sheets sync for pilot status updates

## How to Use (Example Queries)
- `available pilots`
- `match pilots for PRJ001`
- `why mission PRJ001`
- `urgent PRJ001`
- `update pilot P001 Available`

## Tech Stack
- Python
- Streamlit
- Pandas
- Google Sheets API
- Google Drive API

## Security & Secrets Handling
OAuth credentials are managed using Streamlit Secrets. No sensitive credentials or tokens are committed to version control.
