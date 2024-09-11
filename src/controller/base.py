from datetime import datetime
class Base():

    ARCESIUM_FREEZE_DATE = datetime(2024, 6, 30)
    ARCESIUM_FREEZE_DATE_T1 = "20240701"

    def __init__(self) -> None:
        pass

    def to_date(self, str, mask):
        if mask == "yyyymmdd":
            mask = "%Y%m%d"
        dt = datetime.strptime(str, mask)
        return dt
