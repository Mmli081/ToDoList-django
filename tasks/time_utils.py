from datetime import datetime

def create_date(date_str: str) -> datetime.date: #date YYYY-MM-DD
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

