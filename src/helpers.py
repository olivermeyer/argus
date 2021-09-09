def abbreviate_condition(condition: str) -> str:
    if "Generic" in condition:
        short_condition = "Gen"
    else:
        short_condition = condition[
            condition.find("(") + 1:condition.find(")")
        ]
    return short_condition
