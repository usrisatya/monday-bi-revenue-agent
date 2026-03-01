# app/utils/sector_normalizer.py


SECTOR_MAPPING = {
    "energy": "Energy",
    "renewable energy": "Energy",
    "health": "Healthcare",
    "healthcare": "Healthcare",
    "tech": "Technology",
    "technology": "Technology",
}


def normalize_sector_advanced(sector: str) -> str:
    if not sector:
        return "Unknown"

    cleaned = sector.strip().lower()
    return SECTOR_MAPPING.get(cleaned, cleaned.title())