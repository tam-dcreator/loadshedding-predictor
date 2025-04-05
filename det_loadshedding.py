"""
Module for determining load shedding based on power demand and supply data.

This module contains functions to set the power requirement threshold for
load shedding based on the time of day and to estimate load shedding stages
based on various power demand and supply parameters.
"""


def tune_threshold(hour):
    """Set the power requirement threshold that activates loadshedding based
    on peak and off-peak period usage.

    Args:
        hour (int): Time of the day (0-23).

    Returns:
        int: The threshold based on the time of the day.
    """
    # gives a higher accuracy with a lower recall score
    # if 0 <= hour <=23:
    #   return 2500

    # gives a lower accuracy with a higher recall score
    if hour == 19:  # Max power demand happens around 7pm
        return 2100
    elif hour == 1:  # Min power demand happens around 1am
        return 1500
    elif 17 <= hour <= 21:  # Evening peak adjustments
        return 1950
    elif 0 <= hour <= 3:  # Early morning off-peak adjustments
        return 1650
    else:  # Default threshold gotten from the median deficits on days of
        # confirmed loadshedding
        return 1789


def estimate_loadshedding(row):
    """Estimate load shedding stage based on power demand and supply data.

    Args:
        row (pd.Series): A row of data containing the following columns:
            - residual_demand: The residual power demand.
            - dispatchable_generation: The available dispatchable generation.
            - eskom_ocgt_generation: The backup supply from Eskom OCGT.
            - hydro_water_generation: The backup supply from hydro water.
            - total_uclf+oclf: The total unplanned and planned outages.
            - manual_load_reduction(mlr): The manual load reduction.
            - international_imports: The power imports.
            - international_exports: The power exports.
            - load_shedding_threshold: The threshold for load shedding.

    Returns:
        int: 1 if load shedding is required, 0 otherwise.
    """
    demand = row["residual_demand"]
    supply = row["dispatchable_generation"]
    backup_supply1 = row["eskom_ocgt_generation"]
    backup_supply2 = row["hydro_water_generation"]
    manual_reduction = row["manual_load_reduction(mlr)"]
    imports = row["international_imports"]
    exports = row["international_exports"]
    threshold = row["load_shedding_threshold"]

    # Compute the power deficit (demand + exports - supply - imports)
    deficit = (demand + exports) - (supply + imports)

    # Determine load shedding based on deficit and outages
    if (deficit - backup_supply1 - backup_supply2) >= threshold:
        return 1
    elif manual_reduction >= deficit:
        return 1  # If Eskom implements MLR close to the deficit, it strongly
        # suggests load shedding.
    else:
        return 0
