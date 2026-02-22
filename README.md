<p align="center">
  <a href="https://dankistudio.com">
    <img src="report/assets/logo.png" width="140">
  </a>
</p>

<h1 align="center">Citrus Water Supply Optimization</h1>
<p align="center">
  A data-driven framework for estimating citrus irrigation requirements<br/>
  based on environmental and agronomic variables.
</p>

<p align="center">
  <a href="https://adeline-hub.github.io/citrus-water-supply/">
    <img src="https://img.shields.io/badge/Report-Live-blue?logo=quarto" alt="Report Live"/>
  </a>
  <a href="https://adeline-hub.github.io/citrus-water-supply/app.html">
    <img src="https://img.shields.io/badge/Calculator-Live-orange?logo=leaflet" alt="Calculator Live"/>
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT"/>
  </a>
</p>

---

## Overview

This project develops a supervised machine learning model to estimate daily water requirements (liters per tree per day) for citrus crops, and deploys the results as an **interactive irrigation decision support tool**.

The model integrates the following variables:

| Environmental | Agronomic |
|---------------|-----------|
| Temperature (°C) | Tree age (years) |
| Relative humidity (%) | Growth stage (vegetative / flowering / fruiting) |
| Wind speed (km/h) | Soil type (sandy / loam / clay) |
| Rainfall (mm/day) | Canopy area (age-scaled, m²) |

---

## Deliverables

| Deliverable | Technology | Location |
|-------------|------------|----------|
| Exploratory Data Analysis | Marimo + Python | `notebooks/eda_marimo.py` |
| Technical Whitepaper (HTML/PDF) | Quarto | `report/index.qmd` |
| **Irrigation Calculator App** | **Quarto + JS** | `report/app.qmd` |
| Live Whitepaper | GitHub Pages | [View Report](https://adeline-hub.github.io/citrus-water-supply/) |
| **Live Calculator** | **GitHub Pages** | [Open Calculator](https://adeline-hub.github.io/citrus-water-supply/app.html) |

---

## Irrigation Decision Support Tool

The calculator (`app.qmd`) transforms the XGBoost model into an operational planning tool. Users input orchard and weather parameters and receive:

- **ML estimate** — predicted water need per tree (L/tree/day), scaled by age-calibrated canopy area
- **FAO-56 baseline** — classical Penman-Monteith ET₀ × Kc × Ks reference
- **Total volumes** — in litres and m³, for daily / weekly / monthly periods
- **Efficiency metrics** — water savings %, cost saved (€), CO₂ avoided (kg)
- **Agronomic validation** — automatic pass/fail check against peer-reviewed reference ranges (FAO, University of Arizona, Wikifarmer)
- **PDF report download** — branded simulation report with all inputs, results and validation note

The app runs entirely as a static page — no server, no Python at runtime — and is fully offline-capable after the first load.

---

## Strategic Impact

In commercial citrus orchards (~400 trees/hectare), even a 10% reduction in excess irrigation translates to:

- **500–800 m³** of water saved per hectare per year
- **€50–€200** in direct cost reduction per hectare (water + pumping energy)
- Reduced nutrient leaching and lower disease pressure from over-irrigation

At 100 hectares: **50,000–80,000 m³** saved annually, **€5,000–€20,000** in operational cost reduction.

---

## Why Machine Learning?

Classical irrigation scheduling (FAO-56) relies on fixed crop coefficients and rule-based adjustments. While agronomically sound, it assumes simplified linear relationships between environmental variables.

XGBoost learns nonlinear interactions directly from data — capturing effects like:

- Exponential evapotranspiration increase above 35°C
- Wind amplification thresholds (>15 km/h)
- Stage × soil conditional multipliers
- Age-scaled canopy water demand

This produces irrigation forecasts that adapt dynamically to daily variability rather than static scheduling rules, with quantifiable accuracy (R² > 0.9, cross-validated).

---

## Project Structure

```
citrus-water-supply/
├── data/
│   └── processed/
│       └── citrus_water.parquet
├── docs/                        ← GitHub Pages output
│   └── assets/
│       ├── logo.png
│       └── partner_logo.png
├── notebooks/
│   └── eda_marimo.py
├── report/
│   ├── index.qmd                ← Technical whitepaper
│   ├── app.qmd                  ← Interactive calculator
│   └── assets/
│       ├── logo.png
│       └── partner_logo.png
├── src/
│   ├── generate_data.py
│   └── viz.py
├── requirements.txt
└── _quarto.yml
```

---

## Local Development (Windows PowerShell)

### 1. Clone Repository

```powershell
git clone https://github.com/adeline-hub/citrus-water-supply.git
cd citrus-water-supply
```

### 2. Create and Activate Virtual Environment

```powershell
# Windows
python -m venv .venv
.\.venv\Scripts\Activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

If generating PDF for the first time:

```powershell
quarto install tinytex
```

### 4. Generate Dataset

```powershell
python src/generate_data.py
```

Output: `data/processed/citrus_water.parquet`

### 5. Render HTML Report + Calculator

```powershell
cd report
quarto render index.qmd --to html --output-dir ../docs
quarto render app.qmd --to html --output-dir ../docs
cd ..
```

Open locally: `docs/index.html` and `docs/app.html`

### 6. Render PDF Report

```powershell
cd report
quarto render index.qmd --to pdf
cd ..
```

Output: `report/index.pdf`

### 7. Publish to GitHub Pages

```powershell
git add .
git commit -m "Update report and calculator"
git push origin main
```

Or use Quarto's built-in publish command:

```powershell
quarto publish gh-pages
```

---

## References

1. Allen, R.G. et al. (1998). *Crop Evapotranspiration — FAO Irrigation and Drainage Paper 56.*
2. Chen, T. & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System.*
3. University of Arizona Cooperative Extension — Citrus Water Requirements.
4. Wikifarmer — Citrus Tree Irrigation Guide.

---

<p align="center">
  Built by <a href="https://dankistudio.com"><strong>Danki Studio</strong></a> · Nambona Adeline YANGUERE
</p>
