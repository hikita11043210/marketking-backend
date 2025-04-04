import re

def convert_yahoo_date(yahoo_date: str) -> str | None:
    """
    Yahoo!オークションの日付をISO 8601形式に変換します

    Args:
        yahoo_date (str): Yahoo!オークションの日付
            - 新フォーマット: "2025-04-04T21:33:45+09:00"
            - 旧フォーマット: "2025.02.18（月）10:00"

    Returns:
        str | None: ISO 8601形式の日付（例: "2025-02-18T10:00:00"）
    """
    if not yahoo_date:
        return None

    # 既にISO 8601形式の場合はそのまま返す
    if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}', yahoo_date):
        return yahoo_date

    # 旧フォーマットの場合
    match = re.match(r'(\d{4})\.(\d{2})\.(\d{2})（[^)]+）(\d{2}:\d{2})', yahoo_date)
    if match:
        year, month, day, time = match.groups()
        return f"{year}-{month}-{day}T{time}:00"

    return None