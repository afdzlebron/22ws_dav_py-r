# -*- coding: utf-8 -*-
"""Interaktives Dash-Dashboard für Einzelhandelsumsätze."""

from pathlib import Path

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

try:
    from dash import Dash, Input, Output, dcc, html
except ImportError:
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output

    Dash = dash.Dash


BASE_DIR = Path(__file__).resolve().parent
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


def load_dataframe(file_name: str) -> pd.DataFrame:
    """Lädt ein CSV aus dem Projektordner und entfernt index-basierte Exportspalten."""
    data_path = BASE_DIR / file_name
    df = pd.read_csv(data_path)
    unnamed_columns = [column for column in df.columns if str(column).startswith("Unnamed")]
    if unnamed_columns:
        df = df.drop(columns=unnamed_columns)
    return df


def ensure_columns(df: pd.DataFrame, dataset_name: str, required_columns: list[str]) -> None:
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Datensatz '{dataset_name}' fehlt erforderliche Spalten: {', '.join(missing_columns)}"
        )


monthly_sales_df = load_dataframe("monthly_sales_df.csv")
weekly_sale = load_dataframe("weekly_sale.csv")
store_df = load_dataframe("store_df.csv")
holiday_sales = load_dataframe("holiday_sales.csv")
dept_df = load_dataframe("dept_df.csv")

ensure_columns(monthly_sales_df, "monthly_sales_df.csv", ["month", "Month", "Weekly_Sales", "Holiday_Sales"])
ensure_columns(weekly_sale, "weekly_sale.csv", ["Month", "week_no", "Weekly_Sales"])
ensure_columns(store_df, "store_df.csv", ["Month", "Store", "Weekly_Sales"])
ensure_columns(holiday_sales, "holiday_sales.csv", ["month", "Holiday_Sales"])
ensure_columns(dept_df, "dept_df.csv", ["Month", "Dept", "Weekly_Sales"])

monthly_sales_df["month"] = pd.to_numeric(monthly_sales_df["month"], errors="coerce")
weekly_sale["week_no"] = pd.to_numeric(weekly_sale["week_no"], errors="coerce")

month_table = (
    monthly_sales_df[["month", "Month"]]
    .dropna()
    .drop_duplicates()
    .sort_values("month")
)
MONTH_OPTIONS = month_table["Month"].tolist()

if not MONTH_OPTIONS:
    raise ValueError("Keine Monatsdaten verfügbar. Bitte die Datensätze prüfen.")

DEFAULT_BASE = "Feb" if "Feb" in MONTH_OPTIONS else MONTH_OPTIONS[0]
DEFAULT_COMPARISON = "Jan" if "Jan" in MONTH_OPTIONS else MONTH_OPTIONS[min(1, len(MONTH_OPTIONS) - 1)]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Einzelhandelsumsätze Dashboard"
server = app.server

navbar = dbc.Navbar(
    id="navbar",
    children=[
        dbc.Row(
            [
                dbc.Col(html.Img(src=PLOTLY_LOGO, height="70px")),
                dbc.Col(
                    dbc.NavbarBrand(
                        "Einzelhandelsumsätze",
                        style={"color": "white", "fontSize": "25px", "fontFamily": "Times New Roman"},
                    )
                ),
            ],
            align="center",
        ),
    ],
    color="#090059",
)

card_content_dropdwn = [
    dbc.CardBody(
        [
            html.H6("Monate auswählen", style={"textAlign": "center"}),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H6("Aktueller Monat"),
                            dcc.Dropdown(
                                id="dropdown_base",
                                options=[{"label": month, "value": month} for month in MONTH_OPTIONS],
                                value=DEFAULT_BASE,
                                clearable=False,
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.H6("Referenzmonat"),
                            dcc.Dropdown(
                                id="dropdown_comp",
                                options=[{"label": month, "value": month} for month in MONTH_OPTIONS],
                                value=DEFAULT_COMPARISON,
                                clearable=False,
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )
]

body_app = dbc.Container(
    [
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([dbc.Card(card_content_dropdwn, style={"height": "150px"})], width=4),
                dbc.Col([dbc.Card(id="card_num1", style={"height": "150px"})]),
                dbc.Col([dbc.Card(id="card_num2", style={"height": "150px"})]),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([dbc.Card(id="card_num3", style={"height": "350px"})]),
                dbc.Col([dbc.Card(id="card_num4", style={"height": "350px"})]),
            ]
        ),
        html.Br(),
        html.Br(),
    ],
    style={"backgroundColor": "#f7f7f7"},
    fluid=True,
)

app.layout = html.Div(id="parent", children=[navbar, body_app])


def safe_month(month_name: str, fallback: str) -> str:
    return month_name if month_name in MONTH_OPTIONS else fallback


def month_metric(month_name: str, column_name: str) -> float:
    filtered_series = monthly_sales_df.loc[monthly_sales_df["Month"] == month_name, column_name]
    if filtered_series.empty:
        return 0.0
    return float(filtered_series.iloc[0])


def build_weekly_figure(base_month: str, comparison_month: str) -> go.Figure:
    weekly_base = weekly_sale.loc[weekly_sale["Month"] == base_month, ["week_no", "Weekly_Sales"]].dropna()
    weekly_comp = weekly_sale.loc[weekly_sale["Month"] == comparison_month, ["week_no", "Weekly_Sales"]].dropna()

    fig = go.Figure()

    if not weekly_base.empty:
        fig.add_trace(
            go.Scatter(
                x=weekly_base["week_no"],
                y=weekly_base["Weekly_Sales"],
                line={"color": "firebrick", "width": 4},
                name=base_month,
            )
        )

    if not weekly_comp.empty:
        fig.add_trace(
            go.Scatter(
                x=weekly_comp["week_no"],
                y=weekly_comp["Weekly_Sales"],
                line={"color": "#090059", "width": 4},
                name=comparison_month,
            )
        )

    fig.update_layout(
        plot_bgcolor="white",
        margin={"l": 40, "r": 5, "t": 60, "b": 40},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )
    fig.update_xaxes(title_text="Woche im Monat", dtick=1)
    fig.update_yaxes(title_text="Umsatz", tickprefix="$", ticksuffix="M")
    return fig


def build_store_figure(month_name: str, color: str) -> go.Figure:
    month_data = (
        store_df.loc[store_df["Month"] == month_name, ["Store", "Weekly_Sales"]]
        .dropna()
        .sort_values("Weekly_Sales", ascending=False)
        .head(10)
        .sort_values("Weekly_Sales", ascending=True)
    )

    if month_data.empty:
        return go.Figure()

    max_sales = float(month_data["Weekly_Sales"].max())

    fig = go.Figure(
        [
            go.Bar(
                x=month_data["Weekly_Sales"],
                y=month_data["Store"],
                marker_color=color,
                name=month_name,
                text=month_data["Weekly_Sales"].round(1),
                orientation="h",
                textposition="outside",
            )
        ]
    )

    fig.update_layout(
        plot_bgcolor="white",
        margin={"l": 40, "r": 5, "t": 60, "b": 40},
        title=month_name,
        title_x=0.5,
    )
    fig.update_xaxes(range=[0, max_sales + 3], tickprefix="$", ticksuffix="M")
    fig.update_yaxes(title_text="")
    return fig


def metric_card(title: str, value: float) -> list[dbc.CardBody]:
    return [
        dbc.CardBody(
            [
                html.H6(title, style={"fontWeight": "lighter", "textAlign": "center"}),
                html.H3(f"${value:.1f}M", style={"color": "#090059", "textAlign": "center"}),
            ]
        )
    ]


@app.callback(
    [
        Output("card_num1", "children"),
        Output("card_num2", "children"),
        Output("card_num3", "children"),
        Output("card_num4", "children"),
    ],
    [Input("dropdown_base", "value"), Input("dropdown_comp", "value")],
)
def update_cards(base: str, comparison: str):
    base = safe_month(base, DEFAULT_BASE)
    comparison = safe_month(comparison, DEFAULT_COMPARISON)

    sales_base = month_metric(base, "Weekly_Sales")
    holiday_base = month_metric(base, "Holiday_Sales")

    weekly_figure = build_weekly_figure(base, comparison)
    base_store_figure = build_store_figure(base, "indianred")
    comparison_store_figure = build_store_figure(comparison, "#4863A0")

    card_content2 = [
        dbc.CardBody(
            [
                html.H6("Wöchentlicher Umsatzvergleich", style={"fontWeight": "bold", "textAlign": "center"}),
                dcc.Graph(figure=weekly_figure, style={"height": "250px"}),
            ]
        )
    ]

    card_content3 = [
        dbc.CardBody(
            [
                html.H6("Geschäfte mit dem höchsten Umsatz", style={"fontWeight": "bold", "textAlign": "center"}),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(figure=base_store_figure, style={"height": "300px"})]),
                        dbc.Col([dcc.Graph(figure=comparison_store_figure, style={"height": "300px"})]),
                    ]
                ),
            ]
        )
    ]

    return (
        metric_card("Gesamtumsatz", sales_base),
        metric_card("Ferienumsatz", holiday_base),
        card_content2,
        card_content3,
    )


if __name__ == "__main__":
    run_app = getattr(app, "run", app.run_server)
    run_app(debug=False)
