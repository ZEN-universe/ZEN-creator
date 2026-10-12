def get_energy_unit_from_power_unit(power_unit: str) -> str:
    """Get the corresponding energy unit for a given power unit.

    Args:
        power_unit (str): The power unit (e.g., "MW", "GW").

    Returns:
        str: The corresponding energy unit (e.g., "MWh", "GWh").
    """
    if "/h" in power_unit or "/hour" in power_unit:
        energy_unit = power_unit.replace("/hour", "").replace("/h", "")
    else:
        energy_unit = f"({power_unit}*h)"
    return energy_unit
