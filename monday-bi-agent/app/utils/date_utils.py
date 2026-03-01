# app/utils/date_utils.py

from datetime import datetime


def get_current_quarter(date: datetime) -> str:
    month = date.month

    if month <= 3:
        return "Q1"
    elif month <= 6:
        return "Q2"
    elif month <= 9:
        return "Q3"
    else:
        return "Q4"


def is_same_quarter(date: datetime, reference: datetime) -> bool:
    if not date:
        return False

    return (
        get_current_quarter(date) == get_current_quarter(reference)
        and date.year == reference.year
    )