import re

def convert_yahoo_date(yahoo_date: str) -> str | None:
    """
    Yahoo!オークションの日付をISO 8601形式に変換します

    Args:
        yahoo_date (str): Yahoo!オークションの日付（例: "2025.02.18（月）10:00"）

    Returns:
        str | None: ISO 8601形式の日付（例: "2025-02-18T10:00:00"）
    """
    if not yahoo_date:
        return None

    # 正規表現で日付部分を抽出
    match = re.match(r'(\d{4})\.(\d{2})\.(\d{2})（[^)]+）(\d{2}:\d{2})', yahoo_date)
    if not match:
        return None

    # 抽出した部分をISO 8601形式に変換
    year, month, day, time = match.groups()
    return f"{year}-{month}-{day}T{time}:00"
