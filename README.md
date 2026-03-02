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
│   ├── requirements.txt
│   ├── monthly_sales_df.csv
│   ├── holiday_sales.csv
│   ├── weekly_sale.csv
│   ├── store_df.csv
│   ├── dept_df.csv
│   └── retail_sales.csv
├── Dashboard-02
│   ├── db.R
│   ├── Dockerfile
│   └── fluege.csv
├── render.yaml
├── Projektdokumentation.tex
└── README.md
```

## Hinweis zu Backups

Der frühere Ordner `improved_20260214_015308_backup` liegt jetzt im Branch `backup`. Die Hauptentwicklung befindet sich direkt im Repository-Root.

## Voraussetzungen

### Python-Dashboard (`Dashboard-01`)

- Python 3.9 oder neuer
- Pakete:
  - `dash`
  - `dash-bootstrap-components`
  - `pandas`
  - `plotly`
  - `gunicorn` (für Render-Deployment)

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
shiny::runApp("Dashboard-02")
```

## Deployment auf Render

Dieses Repository enthält ein Render-Blueprint unter `render.yaml`, das beide Dashboards als getrennte Web-Services bereitstellt:

- `dashboard-01`: Python/Dash-Service (`Dashboard-01`)
- `dashboard-02`: Docker-basierter R/Shiny-Service (`Dashboard-02`)

Vorgehen:

1. Repository zu GitHub pushen.
2. In Render: **New +** -> **Blueprint** auswählen.
3. Das Repository verbinden und `render.yaml` übernehmen.
4. Beide Services erstellen lassen und auf den ersten erfolgreichen Build warten.

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
