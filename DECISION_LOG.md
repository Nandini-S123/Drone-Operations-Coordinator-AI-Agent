# Decision Log – Drone Operations Coordinator AI Agent


## 1. Problem Understanding & Scope
The problem involves coordinating drone pilots and drone assets across multiple concurrent client missions. This is a high-context operational task that requires tracking pilot availability, skills, certifications, drone readiness, maintenance status, and mission requirements simultaneously.

The goal of the agent is not to automate final decisions, but to act as a decision-support system for a drone operations coordinator. The agent is responsible for aggregating information from multiple datasets, detecting conflicts, and presenting explainable recommendations that help a human operator make informed coordination decisions.

The scope of the agent includes roster management, assignment matching, drone inventory validation, conflict detection, and support for urgent reassignment scenarios. Final approval and accountability remain with the human user, especially in cases where constraints must be relaxed to handle urgent missions.

Out of scope items include automated scheduling optimization, autonomous mission execution, and real-time flight control. These were intentionally excluded to keep the system focused on coordination intelligence rather than operational execution.


## 2. Data & Assumptions
The system operates on three primary datasets: a pilot roster, a drone fleet inventory, and a missions dataset. These datasets are treated as the system of record and are read dynamically at runtime to reflect the latest operational state.

The pilot roster contains information about pilot skills, certifications, location, current assignment status, and availability dates. The drone fleet dataset includes drone models, capabilities, current status, location, and maintenance schedules. The missions dataset defines project locations, required skills and certifications, time windows, and priority levels.

Several assumptions were made to handle ambiguity in the data. Skills, certifications, and drone capabilities are represented as comma-separated values and matched using exact string comparisons. Pilot availability is determined by comparing the mission start date with the pilot’s available_from date. Location matching is treated as a logical match rather than a geographic distance calculation.

The missions dataset is treated as read-only reference data, while the pilot roster allows controlled status updates with explicit user confirmation. Drone fleet data is also treated as read-only to prevent accidental equipment state changes.


## 3. Architecture & Technology Choices

## 4. Google Sheets Integration Decisions

## 5. Conflict Detection & Resolution Strategy

## 6. Urgent Reassignment Interpretation

## 7. Trade-offs & Limitations

## 8. What I Would Improve with More Time

