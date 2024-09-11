from datetime import datetime
class Base():
    def __init__(self) -> None:
        pass

    def to_date(self, str, mask):
        if mask == "yyyymmdd":
            mask = "%Y%m%d"
        dt = datetime.strptime(str, mask)
        return dt
