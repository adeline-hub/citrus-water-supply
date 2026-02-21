\# Citrus Water Supply Optimization



> \*\*How much water does a citrus tree really need?\*\*

> A data-driven approach to irrigation planning based on temperature,

> soil type, tree age, and growth stage.



\[!\[Quarto Report](https://img.shields.io/badge/Report-Live-blue?logo=quarto)](https://adeline-hub.github.io/citrus-water-supply/)

\[!\[License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



\## Project Goal



Provide \*\*actionable irrigation recommendations\*\* for citrus growers

by modeling daily water requirements (liters/tree/day) as a function

of environmental and agronomic variables.



\## Key Deliverables



| Deliverable | Tool | Location |

|---|---|---|

| Interactive EDA | Marimo | `notebooks/eda\_marimo.py` |

| Static Report (PDF/HTML) | Quarto | `report/index.qmd` |

| Live Dashboard | GitHub Pages | \[Link](https://adeline-hub.github.io/citrus-water-supply/) |



\## Quick Start



```bash

\# 1. Clone

git clone https://github.com/adeline-hub/citrus-water-supply.git

cd citrus-water-supply



\# 2. Environment

python -m venv .venv \&\& source .venv/bin/activate

pip install -r requirements.txt



\# 3. Generate data + render report

make all



\# 4. Launch interactive EDA

marimo edit notebooks/eda\_marimo.py

