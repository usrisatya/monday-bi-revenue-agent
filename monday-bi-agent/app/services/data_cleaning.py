# app/services/data_cleaning.py

from datetime import datetime
from typing import Optional


def clean_number(value: Optional[str]) -> float:
    """
    Converts messy numeric string to float.
    Handles currency symbols, commas, nulls.
    """

    if not value:
        return 0.0

    try:
        cleaned = (
            str(value)
            .replace(",", "")
            .replace("$", "")
            .replace("₹", "")
            .strip()
        )
        return float(cleaned)
    except Exception:
        return 0.0


def normalize_sector(sector: Optional[str]) -> str:
    """
    Standardizes sector values.
    """

    if not sector:
        return "Unknown"

    sector = sector.strip().lower()

    mapping = {
        "energy": "Energy",
        "energy ": "Energy",
        "renewable energy": "Energy",
        "health": "Healthcare",
        "healthcare": "Healthcare",
        "tech": "Technology",
        "technology": "Technology",
    }

    return mapping.get(sector, sector.title())


def parse_date(value: Optional[str]) -> Optional[datetime]:
    """
    Parses various date formats safely.
    """

    if not value:
        return None

    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%d/%m/%Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    return None


def clean_text(value: Optional[str]) -> str:
    """
    Handles empty text fields.
    """

    if not value:
        return ""

    return value.strip()