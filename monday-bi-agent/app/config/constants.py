# app/config/constants.py

from datetime import datetime


# Deal stages considered closed-won
CLOSED_WON_STAGES = [
    "Closed Won",
    "Won"
]

# Deal stages considered closed-lost
CLOSED_LOST_STAGES = [
    "Closed Lost",
    "Lost"
]

# Early stage risk categories
EARLY_STAGE_STAGES = [
    "Lead",
    "Prospect",
    "Qualification",
    "Discovery"
]

# Default currency
DEFAULT_CURRENCY = "₹"

# Current reference date (can be mocked in tests)
REFERENCE_DATE = datetime.now()

# Executive response thresholds
HIGH_RISK_EARLY_STAGE_PERCENT = 0.6  # 60%
LOW_CONVERSION_THRESHOLD = 0.2       # 20%