def convert_group_name(name: str) -> str:
    convert_groups = {
        "自民": "自由民主党",
        "自民党": "自由民主党"
    }

    if name in convert_groups.keys():
        return convert_groups[name]
    return name
