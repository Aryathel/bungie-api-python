from datetime import datetime


class DateTimeUtils:
    @staticmethod
    def encode_datetime(dt: datetime) -> str:
        return dt.isoformat() + '.00Z'
