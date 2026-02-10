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
The system follows a modular, layered architecture that separates data access, business logic, and user interaction. Core coordination logic such as roster filtering, assignment matching, conflict detection, and urgent reassignment is implemented as independent Python modules. This separation improves readability, testability, and reduces the risk of unintended side effects during changes.

A Streamlit-based interface was chosen to provide a lightweight conversational interaction layer without introducing unnecessary frontend complexity. This allowed development effort to remain focused on the agent’s reasoning and coordination logic rather than UI engineering.

Python was selected as the primary language due to its strong ecosystem for data processing, rapid prototyping, and integration with external services such as Google Sheets. Pandas is used for structured data handling, while gspread and Google OAuth libraries are used for secure, authenticated access to Google Sheets.

This architecture prioritizes clarity, explainability, and operational safety over optimization or scale, which aligns with the problem’s focus on coordination intelligence rather than high-throughput automation.


## 4. Google Sheets Integration Decisions
Google Sheets was used as the system of record to align with existing operational workflows and to satisfy the requirement for two-way data synchronization. The pilot roster and drone fleet datasets are read dynamically from Google Sheets to ensure the agent always reasons over the latest operational state.

Pilot status updates are the only write operation supported by the agent. This decision was intentional to minimize the risk of accidental data corruption. All write operations require explicit user confirmation through the interface, ensuring controlled and auditable changes.

Due to organization-level security policies that disabled service account key creation, OAuth-based user authentication was used instead of service accounts. This approach follows Google’s recommended security practices, avoids long-lived credentials, and fully satisfies the integration requirements. OAuth credentials are managed securely and not committed to version control.

The missions dataset is treated as read-only reference data and is loaded locally to prevent unintended modification of project definitions.


## 5. Conflict Detection & Resolution Strategy
Conflict detection is a core responsibility of the agent and is implemented as an explicit reasoning layer rather than implicit filtering. The system distinguishes between blocking conflicts and advisory warnings to reflect real operational decision-making.

Blocking conflicts include pilot double-booking, missing required skills or certifications, pilot unavailability based on mission dates, drones under maintenance, and drones lacking required capabilities. These conflicts prevent direct assignment and are clearly communicated to the user.

Advisory warnings include location mismatches and upcoming maintenance deadlines. These do not block assignments but are surfaced to inform risk-aware decision-making.

By separating hard constraints from soft warnings, the agent supports informed human judgment rather than enforcing rigid automation, which is critical in real-world operations.


## 6. Urgent Reassignment Interpretation
Urgent reassignment is interpreted as a scenario where a high-priority mission cannot be fulfilled using standard constraints due to pilot unavailability, skill mismatches, or equipment limitations.

When an urgent mission is detected, the agent does not attempt automatic reassignment. Instead, it relaxes non-critical constraints in a controlled manner and presents multiple alternative strategies. These include allowing pilot or drone location mismatches, reassigning pilots from lower-priority missions, or using drones with partial capability matches.

Each suggestion is accompanied by an explicit explanation and risk disclosure, such as potential travel delays, downstream conflicts, or reduced mission quality. Final approval is always left to the human operator.

This approach ensures mission continuity while maintaining transparency, accountability, and operational safety.


## 7. Trade-offs & Limitations
Several trade-offs were made to balance realism, safety, and development time. Rule-based matching and conflict detection were chosen over machine learning models to ensure explainability and predictable behavior within the limited timeline.

Geographic reasoning is handled through logical location matching rather than distance-based calculations. Skill and capability matching relies on exact string comparisons, which simplifies implementation but may require stricter data hygiene.

The system does not perform automatic schedule optimization or autonomous reassignment. These decisions were intentionally excluded to avoid over-automation in scenarios that require human judgment and accountability.


## 8. What I Would Improve with More Time
With additional time, the system could be extended to include distance-based location matching, calendar-based scheduling integration, and role-based access control for different operational users.

Additional improvements could include assignment history tracking, audit logs for all changes, ranking of urgent reassignment suggestions based on impact, and support for multiple concurrent mission evaluations.

The conversational interface could also be enhanced with more natural language understanding and guided prompts, while maintaining the same emphasis on explainability and safety.



