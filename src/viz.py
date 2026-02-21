"""
Reusable visualization functions — consistent branding across
Marimo notebooks and Quarto report.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

# ── Brand palette ──────────────────────────────────────────────
PALETTE = {
    "primary": "#2E86AB",
    "secondary": "#A23B72",
    "accent": "#F18F01",
    "success": "#2CA58D",
    "dark": "#1B1B1E",
    "light": "#F5F5F5",
}
COLORS = list(PALETTE.values())

sns.set_theme(
    style="whitegrid",
    palette=[PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"]],
    font_scale=1.05,
    rc={
        "figure.figsize": (9, 5),
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "figure.dpi": 150,
    },
)


def save(fig, name: str, directory: str = "report/images"):
    """Save figure as PNG + SVG for Quarto."""
    p = Path(directory)
    p.mkdir(parents=True, exist_ok=True)
    fig.savefig(p / f"{name}.png", bbox_inches="tight", dpi=200)
    fig.savefig(p / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


# ── Page 1: Overview Heatmap ──────────────────────────────────
def plot_correlation_heatmap(df: pd.DataFrame):
    numeric = df.select_dtypes("number")
    corr = numeric.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
        center=0, linewidths=0.5, ax=ax, vmin=-1, vmax=1,
        cbar_kws={"label": "Pearson r"},
    )
    ax.set_title("Variable Correlation Matrix")
    return fig


# ── Page 2: Temperature vs Water Need ────────────────────────
def plot_temp_vs_water(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(9, 5))
    scatter = ax.scatter(
        df["temperature_c"],
        df["water_need_liters"],
        c=df["humidity_pct"],
        cmap="RdYlBu_r",
        alpha=0.5,
        s=15,
        edgecolors="none",
    )
    cbar = fig.colorbar(scatter, ax=ax, label="Humidity (%)")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Water Need (L/tree/day)")
    ax.set_title("Water Demand Increases with Temperature\n(color = humidity)")

    # Trend line
    z = np.polyfit(df["temperature_c"], df["water_need_liters"], 2)
    x_line = np.linspace(df["temperature_c"].min(), df["temperature_c"].max(), 200)
    ax.plot(x_line, np.polyval(z, x_line), color=PALETTE["secondary"],
            linewidth=2.5, label="Quadratic trend")
    ax.legend()
    return fig


# ── Page 3: Growth Stage Boxplot ──────────────────────────────
def plot_growth_stage_box(df: pd.DataFrame):
    order = ["Vegetative", "Flowering", "Fruiting"]
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(
        data=df, x="growth_stage", y="water_need_liters",
        hue="soil_type", order=order, ax=ax,
        palette=[PALETTE["primary"], PALETTE["success"], PALETTE["accent"]],
        fliersize=2,
    )
    ax.set_xlabel("Growth Stage")
    ax.set_ylabel("Water Need (L/tree/day)")
    ax.set_title("Fruiting Trees Demand 35–50% More Water")
    ax.legend(title="Soil Type", loc="upper left")
    return fig


# ── Page 4: Feature Importance / SHAP-style bar ──────────────
def plot_feature_importance(importances: dict):
    sorted_imp = dict(sorted(importances.items(), key=lambda x: x[1]))
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(
        list(sorted_imp.keys()),
        list(sorted_imp.values()),
        color=PALETTE["primary"],
        edgecolor="white",
    )
    ax.set_xlabel("Importance (gain)")
    ax.set_title("What Drives Water Demand?\nXGBoost Feature Importance")
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(1.0))
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.005, bar.get_y() + bar.get_height() / 2,
                f"{width:.1%}", va="center", fontsize=9)
    return fig