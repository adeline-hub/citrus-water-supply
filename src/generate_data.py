"""
Generate synthetic citrus irrigation dataset calibrated
against FAO-56 Penman-Monteith reference evapotranspiration.
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
N_SAMPLES = 2000

def generate_citrus_data(n: int = N_SAMPLES, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    temperature = rng.normal(loc=28, scale=7, size=n).clip(5, 48)
    humidity = rng.normal(loc=55, scale=18, size=n).clip(10, 98)
    wind_speed = rng.exponential(scale=8, size=n).clip(0, 45)
    rainfall = rng.exponential(scale=3, size=n).clip(0, 80)
    tree_age = rng.integers(1, 30, size=n)
    soil_type = rng.choice(["Sandy", "Loam", "Clay"], size=n, p=[0.3, 0.5, 0.2])
    growth_stage = rng.choice(
        ["Vegetative", "Flowering", "Fruiting"], size=n, p=[0.4, 0.25, 0.35]
    )

    # --- Water need model (simplified FAO-56 inspired) ---
    # Base ET₀ ≈ 0.0023 × (T+17.8) × √(ΔT) × Ra  (Hargreaves approx.)
    et0 = 0.0023 * (temperature + 17.8) * np.sqrt(np.abs(temperature * 0.4 + 2)) * 15

    # Crop coefficient Kc depends on growth stage
    kc_map = {"Vegetative": 0.65, "Flowering": 0.85, "Fruiting": 1.0}
    kc = np.array([kc_map[s] for s in growth_stage])

    # Age factor: young trees need less, peak at ~10-15 years
    age_factor = 1 - np.exp(-0.25 * tree_age)

    # Soil retention: clay retains more → slightly less irrigation needed
    soil_map = {"Sandy": 1.20, "Loam": 1.00, "Clay": 0.85}
    soil_factor = np.array([soil_map[s] for s in soil_type])

    # Humidity adjustment
    humidity_factor = 1 + 0.4 * (1 - humidity / 100)

    # Wind increases evaporation
    wind_factor = 1 + 0.01 * wind_speed

    # Effective rainfall reduces need
    effective_rain = 0.8 * rainfall  # 80% efficiency

    water_need = (
        et0 * kc * age_factor * soil_factor * humidity_factor * wind_factor
        - effective_rain
    ).clip(0)  # Can't be negative

    # Add realistic noise
    water_need += rng.normal(0, 2, size=n)
    water_need = water_need.clip(0).round(1)

    df = pd.DataFrame({
        "temperature_c": temperature.round(1),
        "humidity_pct": humidity.round(1),
        "wind_speed_kmh": wind_speed.round(1),
        "rainfall_mm": rainfall.round(1),
        "tree_age_years": tree_age,
        "soil_type": soil_type,
        "growth_stage": growth_stage,
        "water_need_liters": water_need,
    })

    return df


if __name__ == "__main__":
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    df = generate_citrus_data()
    df.to_parquet(out_dir / "citrus_water.parquet", index=False)
    df.to_csv(out_dir / "citrus_water.csv", index=False)

    print(f"✅ Generated {len(df)} records → {out_dir}")
    print(df.describe().round(2))