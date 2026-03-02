# Datenvisualisierungsprojekt - Wintersemester 2022/2023

## Projektübersicht

Dieses Repository enthält zwei Dashboards aus dem Kurs *Datenvisualisierung mit R und Python*:

- `Dashboard-01`: Interaktives Python/Dash-Dashboard für Einzelhandelsumsätze.
- `Dashboard-02`: Interaktive R/Shiny-Anwendung zum europäischen Flugverkehr.

## Verbesserungen in dieser Version

- Stabilere Dateipfade (Ausführung unabhängig vom aktuellen Arbeitsverzeichnis).
- Robusteres Daten-Handling (Spaltenprüfung, Datumskonvertierung, sichere Filter).
- Modernisierte Dash-Imports und bereinigte Callback-Logik.
- Bessere Visualisierungsformatierung in beiden Dashboards.
- Ergänzte technische Dokumentation als LaTeX-Datei mit Erklärungen und Visualisierungen.

## Projektstruktur

```text
.
├── Dashboard-01
│   ├── app.py
│   ├── monthly_sales_df.csv
│   ├── holiday_sales.csv
│   ├── weekly_sale.csv
│   ├── store_df.csv
│   ├── dept_df.csv
│   └── retail_sales.csv
├── Dashboard-02
│   ├── db.R
│   └── fluege.csv
├── Projektdokumentation.tex
└── README.md
```

## Voraussetzungen

### Python-Dashboard (`Dashboard-01`)

- Python 3.9 oder neuer
- Pakete:
  - `dash`
  - `dash-bootstrap-components`
  - `pandas`
  - `plotly`

Start:

```bash
cd Dashboard-01
python3 app.py
```

### R-Dashboard (`Dashboard-02`)

- R (mit Shiny-Unterstützung)
- Pakete:
  - `shiny`
  - `dplyr`
  - `ggplot2`
  - `readr`
  - `scales`

Start (in R):

```r
setwd("Dashboard-02")
source("db.R")
```

## Dokumentation (LaTeX)

Die Datei `Projektdokumentation.tex` enthält:

- eine detaillierte Beschreibung beider Anwendungen,
- Architektur- und Datenflussdiagramme,
- Visualisierungen der verarbeiteten Daten,
- eine technische Zusammenfassung der Verbesserungen.

Kompilierung:

```bash
pdflatex Projektdokumentation.tex
```

## Disclaimer

Dieses Projekt dient ausschließlich der Lehre und Dokumentation und verfolgt keine kommerziellen Zwecke.

## Autor

AFL et al.
