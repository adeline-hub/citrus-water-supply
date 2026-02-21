# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "pandas>=2.1",
#     "numpy>=1.26",
#     "seaborn>=0.13",
#     "matplotlib>=3.8",
#     "xgboost>=2.0",
#     "scikit-learn>=1.4",
#     "shap>=0.45",
# ]
# ///

import marimo

__generated_with = "0.6.0"
app = marimo.App(width="medium")


# ── Cell 1: Imports & Config ─────────────────────────────────
@app.cell
def imports():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import sys, os

    # Allow importing from project root
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from src.viz import (
        plot_correlation_heatmap,
        plot_temp_vs_water,
        plot_growth_stage_box,
        plot_feature_importance,
        save,
    )
    from src.generate_data import generate_citrus_data

    mo.md("# 🍊 Citrus Water Supply — Exploratory Data Analysis")
    return (
        mo,
        pd,
        np,
        plt,
        sns,
        save,
        generate_citrus_data,
        plot_correlation_heatmap,
        plot_temp_vs_water,
        plot_growth_stage_box,
        plot_feature_importance,
    )


# ── Cell 2: Load / Generate Data ─────────────────────────────
@app.cell
def load_data(mo, pd, generate_citrus_data):
    from pathlib import Path

    parquet_path = Path("../data/processed/citrus_water.parquet")
    if parquet_path.exists():
        df = pd.read_parquet(parquet_path)
        mo.md(f"✅ Loaded **{len(df):,}** records from `{parquet_path}`")
    else:
        df = generate_citrus_data()
        mo.md(f"⚠️ No cached data — generated **{len(df):,}** synthetic records")

    mo.ui.table(df.describe().round(2).reset_index())
    return df,


# ── Cell 3: Interactive Filters ──────────────────────────────
@app.cell
def filters(mo):
    temp_slider = mo.ui.slider(
        start=5, stop=48, value=48, label="Max Temperature (°C)"
    )
    soil_dropdown = mo.ui.dropdown(
        options=["All", "Sandy", "Loam", "Clay"],
        value="All",
        label="Soil Type",
    )
    stage_dropdown = mo.ui.dropdown(
        options=["All", "Vegetative", "Flowering", "Fruiting"],
        value="All",
        label="Growth Stage",
    )
    mo.hstack([temp_slider, soil_dropdown, stage_dropdown])
    return temp_slider, soil_dropdown, stage_dropdown


# ── Cell 4: Filtered View ────────────────────────────────────
@app.cell
def filtered(mo, df, temp_slider, soil_dropdown, stage_dropdown):
    mask = df["temperature_c"] <= temp_slider.value
    if soil_dropdown.value != "All":
        mask &= df["soil_type"] == soil_dropdown.value
    if stage_dropdown.value != "All":
        mask &= df["growth_stage"] == stage_dropdown.value

    dff = df[mask].copy()
    mo.md(f"**Filtered dataset:** {len(dff):,} / {len(df):,} records")
    return dff, mask


# ── Cell 5: Correlation Heatmap ──────────────────────────────
@app.cell
def viz_corr(dff, plot_correlation_heatmap, save, mo):
    # Renamed variable to 'fig_corr' to avoid conflict
    fig_corr = plot_correlation_heatmap(dff)
    save(fig_corr, "correlation_heatmap")
    mo.vstack([mo.md("### Correlation Matrix"), fig_corr])
    return fig_corr,


# ── Cell 6: Temperature vs Water ─────────────────────────────
@app.cell
def viz_temp(dff, plot_temp_vs_water, save, mo):
    # Renamed variable to 'fig_temp'
    fig_temp = plot_temp_vs_water(dff)
    save(fig_temp, "temp_vs_water")
    mo.vstack([mo.md("### Temperature Effect on Irrigation Demand"), fig_temp])
    return fig_temp,


# ── Cell 7: Growth Stage Boxplot ─────────────────────────────
@app.cell
def viz_stage(dff, plot_growth_stage_box, save, mo):
    # Renamed variable to 'fig_stage'
    fig_stage = plot_growth_stage_box(dff)
    save(fig_stage, "growth_stage_box")
    mo.vstack([mo.md("### Water Needs by Growth Stage & Soil"), fig_stage])
    return fig_stage,


# ── Cell 8: Model Training + Feature Importance ──────────────
@app.cell
def model(df, plot_feature_importance, save, mo):
    from sklearn.model_selection import cross_val_score
    from sklearn.preprocessing import LabelEncoder
    from xgboost import XGBRegressor

    dfc = df.copy()
    le_soil = LabelEncoder().fit(dfc["soil_type"])
    le_stage = LabelEncoder().fit(dfc["growth_stage"])
    dfc["soil_type_enc"] = le_soil.transform(dfc["soil_type"])
    dfc["growth_stage_enc"] = le_stage.transform(dfc["growth_stage"])

    features = [
        "temperature_c", "humidity_pct", "wind_speed_kmh",
        "rainfall_mm", "tree_age_years", "soil_type_enc", "growth_stage_enc",
    ]
    X = dfc[features]
    y = dfc["water_need_liters"]

    model_xgb = XGBRegressor(
        n_estimators=300, max_depth=5, learning_rate=0.08,
        random_state=42, n_jobs=-1
    )
    scores = cross_val_score(model_xgb, X, y, cv=5, scoring="r2")
    
    model_xgb.fit(X, y)
    
    imp = dict(zip(
        [f.replace("_enc", "").replace("_", " ").title() for f in features],
        model_xgb.feature_importances_ / model_xgb.feature_importances_.sum(),
    ))
    
    # Renamed variable to 'fig_imp'
    fig_imp = plot_feature_importance(imp)
    save(fig_imp, "feature_importance")

    mo.vstack([
        mo.md(f"### Model Performance\n**5-Fold CV R²:** {scores.mean():.3f} ± {scores.std():.3f}"),
        fig_imp
    ])
    return model_xgb, scores, imp, fig_imp, dfc, le_soil, le_stage


# ── Cell 9: Summary KPIs ─────────────────────────────────────
@app.cell
def kpis(mo, df, scores):
    avg_water = df["water_need_liters"].mean()
    max_water = df["water_need_liters"].quantile(0.95)

    mo.md(f"""
    ## 📋 Key Findings

    | Metric | Value |
    |---|---|
    | Average water need | **{avg_water:.1f} L/tree/day** |
    | 95th percentile (peak demand) | **{max_water:.1f} L/tree/day** |
    | Model accuracy (R²) | **{scores.mean():.1%}** |
    | #1 driver | **Temperature** |
    | Most water-hungry stage | **Fruiting** |
    """)
    return avg_water, max_water


if __name__ == "__main__":
    app.run()