import calendar

def get_nth_week(day):
    # 7 + 1
    return (day - 1)

def get_nth_dow(year, month, day):
    return get_nth_week(day), calendar.weekday(year, month, day)

def get_weekday(year, month, day):
    return calendar.weekday(year, month, day)

def convert_group_name(name: str) -> str:
    convert_groups = {
        "自民": "自由民主党",
        "自民党": "自由民主党"
    }

    if name in convert_groups.keys():
        return convert_groups[name]
    return name

def filter_word(word: str) -> bool:
    """
    フィルタリングするワードがあったらFalseを返す.

    Args:
        word (str): _description_

    Returns:
        bool: _description_
    """
    words = ["日本", "委員長"]
    words = ["日本", "委員長", "委員会"]

    if word in words:
        return False
    return True
