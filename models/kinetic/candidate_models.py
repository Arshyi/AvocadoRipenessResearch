"""Candidate avocado-ripening dynamics.

These functions are an implementation scaffold, not a fitted biological model.
No parameter values in this module are claimed for avocado. Callers must supply
units-consistent parameters and measured environmental forcing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Sequence

import numpy as np


GAS_CONSTANT_J_MOL_K = 8.31446261815324
STATE_NAMES = (
    "water_mass",
    "firmness",
    "chlorophyll",
    "anthocyanin",
    "ethylene_state",
    "starch_mass",
    "soluble_solid_mass",
    "lipid_mass",
)


@dataclass(frozen=True)
class CandidateParameters:
    """Units-consistent parameters for the proposed lumped ODE system."""

    reference_temperature_k: float
    water_rate_ref: float
    water_activation_energy_j_mol: float
    surface_area: float
    water_activity_offset: float
    water_activity_mass_scale: float
    airflow_multiplier: float
    firmness_rate_ref: float
    firmness_activation_energy_j_mol: float
    firmness_floor: float
    ethylene_firmness_half_saturation: float
    ethylene_firmness_hill: float
    chlorophyll_rate_ref: float
    chlorophyll_activation_energy_j_mol: float
    anthocyanin_rate_ref: float
    anthocyanin_activation_energy_j_mol: float
    anthocyanin_capacity: float
    anthocyanin_loss_rate: float
    anthocyanin_ripeness_half_saturation: float
    anthocyanin_ripeness_hill: float
    ethylene_basal_rate: float
    ethylene_autocatalytic_rate: float
    ethylene_half_saturation: float
    ethylene_hill: float
    ethylene_loss_rate: float
    starch_rate_ref: float
    starch_activation_energy_j_mol: float
    starch_to_soluble_yield: float
    soluble_consumption_rate: float
    lipid_consumption_rate: float


def relative_arrhenius_rate(
    rate_at_reference: float,
    activation_energy_j_mol: float,
    temperature_k: float,
    reference_temperature_k: float,
) -> float:
    """Return an Arrhenius rate normalized to a reference temperature."""
    if temperature_k <= 0 or reference_temperature_k <= 0:
        raise ValueError("Absolute temperatures must be positive")
    if rate_at_reference < 0 or activation_energy_j_mol < 0:
        raise ValueError("Rate and apparent activation energy must be nonnegative")
    exponent = -(activation_energy_j_mol / GAS_CONSTANT_J_MOL_K) * (
        1.0 / temperature_k - 1.0 / reference_temperature_k
    )
    return float(rate_at_reference * np.exp(exponent))


def hill_activation(value: float, half_saturation: float, hill: float) -> float:
    """Bounded Hill activation for nonnegative states."""
    if half_saturation <= 0 or hill <= 0:
        raise ValueError("Hill parameters must be positive")
    value = max(float(value), 0.0)
    numerator = value**hill
    return float(numerator / (half_saturation**hill + numerator))


def logistic_progression(time: float, rate: float, midpoint: float) -> float:
    """Dimensionless latent progression in [0, 1]."""
    if rate < 0:
        raise ValueError("Progression rate must be nonnegative")
    return float(1.0 / (1.0 + np.exp(-rate * (time - midpoint))))


def coupled_candidate_rhs(
    time: float,
    state: Sequence[float],
    parameters: CandidateParameters,
    forcing: Callable[[float], Mapping[str, float]],
) -> np.ndarray:
    """Evaluate the proposed lumped ripening ODE right-hand side.

    Required forcing keys:
      - ``temperature_k``: absolute temperature
      - ``relative_humidity``: fraction in [0, 1]
      - ``airflow_factor``: nonnegative dimensionless multiplier
      - ``latent_ripeness``: independently supplied/estimated state in [0, 1]

    The state ordering is given by ``STATE_NAMES``.
    """
    y = np.asarray(state, dtype=float)
    if y.shape != (len(STATE_NAMES),):
        raise ValueError(f"Expected {len(STATE_NAMES)} states: {STATE_NAMES}")
    if np.any(~np.isfinite(y)):
        raise ValueError("State contains a non-finite value")
    if np.any(y < 0):
        raise ValueError("Candidate model states must be nonnegative")

    inputs = forcing(float(time))
    temperature_k = float(inputs["temperature_k"])
    relative_humidity = float(inputs["relative_humidity"])
    airflow_factor = float(inputs["airflow_factor"])
    latent_ripeness = float(inputs["latent_ripeness"])
    if not 0 <= relative_humidity <= 1:
        raise ValueError("relative_humidity must be a fraction in [0, 1]")
    if airflow_factor < 0 or not 0 <= latent_ripeness <= 1:
        raise ValueError("Invalid airflow factor or latent ripeness")

    (
        water_mass,
        firmness,
        chlorophyll,
        anthocyanin,
        ethylene,
        starch,
        soluble,
        lipid,
    ) = y
    p = parameters

    water_rate = relative_arrhenius_rate(
        p.water_rate_ref,
        p.water_activation_energy_j_mol,
        temperature_k,
        p.reference_temperature_k,
    )
    if p.water_activity_mass_scale <= 0:
        raise ValueError("water_activity_mass_scale must be positive")
    water_activity = float(
        np.clip(
            p.water_activity_offset + water_mass / p.water_activity_mass_scale,
            0.0,
            1.0,
        )
    )
    d_water = (
        -water_rate
        * p.surface_area
        * p.airflow_multiplier
        * airflow_factor
        * max(water_activity - relative_humidity, 0.0)
    )

    firmness_rate = relative_arrhenius_rate(
        p.firmness_rate_ref,
        p.firmness_activation_energy_j_mol,
        temperature_k,
        p.reference_temperature_k,
    )
    ethylene_softening = hill_activation(
        ethylene,
        p.ethylene_firmness_half_saturation,
        p.ethylene_firmness_hill,
    )
    d_firmness = (
        -firmness_rate
        * ethylene_softening
        * max(firmness - p.firmness_floor, 0.0)
    )

    chlorophyll_rate = relative_arrhenius_rate(
        p.chlorophyll_rate_ref,
        p.chlorophyll_activation_energy_j_mol,
        temperature_k,
        p.reference_temperature_k,
    )
    d_chlorophyll = -chlorophyll_rate * chlorophyll

    anthocyanin_rate = relative_arrhenius_rate(
        p.anthocyanin_rate_ref,
        p.anthocyanin_activation_energy_j_mol,
        temperature_k,
        p.reference_temperature_k,
    )
    pigment_activation = hill_activation(
        latent_ripeness,
        p.anthocyanin_ripeness_half_saturation,
        p.anthocyanin_ripeness_hill,
    )
    d_anthocyanin = (
        anthocyanin_rate
        * pigment_activation
        * max(p.anthocyanin_capacity - anthocyanin, 0.0)
        - p.anthocyanin_loss_rate * anthocyanin
    )

    ethylene_activation = hill_activation(
        ethylene, p.ethylene_half_saturation, p.ethylene_hill
    )
    d_ethylene = (
        p.ethylene_basal_rate
        + p.ethylene_autocatalytic_rate * ethylene_activation
        - p.ethylene_loss_rate * ethylene
    )

    starch_rate = relative_arrhenius_rate(
        p.starch_rate_ref,
        p.starch_activation_energy_j_mol,
        temperature_k,
        p.reference_temperature_k,
    )
    starch_conversion = starch_rate * starch
    d_starch = -starch_conversion
    d_soluble = (
        p.starch_to_soluble_yield * starch_conversion
        - p.soluble_consumption_rate * soluble
    )
    d_lipid = -p.lipid_consumption_rate * lipid

    return np.asarray(
        [
            d_water,
            d_firmness,
            d_chlorophyll,
            d_anthocyanin,
            d_ethylene,
            d_starch,
            d_soluble,
            d_lipid,
        ],
        dtype=float,
    )


def validate_state_names(names: Sequence[str]) -> None:
    """Guard serialized model artifacts against state-order drift."""
    if tuple(names) != STATE_NAMES:
        raise ValueError(f"State order mismatch: expected {STATE_NAMES}, got {tuple(names)}")
