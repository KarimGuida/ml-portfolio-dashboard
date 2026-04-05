import pandas as pd


def validate_required_fields(input_data: dict, required_fields: list[str]) -> None:
    missing = [field for field in required_fields if field not in input_data]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")


def validate_allowed_values(input_data: dict, allowed_values: dict) -> None:
    for field, allowed in allowed_values.items():
        if field in input_data and input_data[field] not in allowed:
            raise ValueError(
                f"Invalid value for '{field}': {input_data[field]}. Allowed values: {allowed}"
            )


def validate_numeric_ranges(input_data: dict, numeric_ranges: dict) -> None:
    for field, (min_val, max_val) in numeric_ranges.items():
        if field in input_data:
            value = input_data[field]
            if value < min_val or value > max_val:
                raise ValueError(
                    f"Value for '{field}' must be between {min_val} and {max_val}. Got: {value}"
                )


def convert_input_to_dataframe(input_data: dict, column_order: list[str]) -> pd.DataFrame:
    df = pd.DataFrame([input_data])
    return df[column_order]
