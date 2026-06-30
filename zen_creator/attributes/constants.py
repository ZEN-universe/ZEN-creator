# Constants for validation
ATTRIBUTES_SUPPORTING_LISTS = {
    "conversion_factor",
    "reference_carrier",
    "input_carrier",
    "output_carrier",
    "retrofit_reference_carrier",
}

ATTRIBUTES_SUPPORTING_BASE_TECHNOLOGY = {"retrofit_flow_coupling_factor"}

ALLOWED_DF_INDEX_NAMES = {
    "time",
    "year",
    "node",
    "location",
    "edge",
    "carrier",
    "technology",
    "year_construction",
}

ALLOWED_YEARLY_VARIATIONS_INDEX_NAMES = {
    "year",
    "node",
    "location",
    "edge",
    "carrier",
    "technology",
}

UNIT_REPLACEMENTS = {
    "GW*h": "GWh",
    "MW*h": "MWh",
    "kW*h": "kWh",
    "/h*h": "",
}
