library(dplyr)
library(shiny)
library(ggplot2)
library(readr)
library(scales)

resolve_data_path <- function(file_name) {
  local_path <- file.path(getwd(), file_name)
  if (file.exists(local_path)) {
    return(local_path)
  }

  args <- commandArgs(trailingOnly = FALSE)
  file_flag <- "--file="
  script_arg <- args[grepl(file_flag, args)]

  if (length(script_arg) > 0) {
    script_dir <- dirname(normalizePath(sub(file_flag, "", script_arg[1])))
    fallback_path <- file.path(script_dir, file_name)
    if (file.exists(fallback_path)) {
      return(fallback_path)
    }
  }

  stop(paste("Datendatei nicht gefunden:", file_name))
}

flights <- read_csv(resolve_data_path("fluege.csv"), show_col_types = FALSE) %>%
  mutate(
    Date = as.Date(Date, format = "%Y-%m-%dT%H:%M:%SZ"),
    Total = as.numeric(Total)
  ) %>%
  filter(!is.na(Date), !is.na(Total)) %>%
  arrange(Date)

countries <- sort(unique(flights$Land))

ui <- fluidPage(
  titlePanel("Europäischer Flugverkehr während der COVID-Pandemie"),
  p(
    "Mit dem Ausbruch der COVID-19-Pandemie im März 2020 ist die Zahl der Flüge,",
    "die an europäischen Flughäfen ankommen oder von dort abfliegen, drastisch zurückgegangen."
  ),
  fluidRow(
    column(
      width = 9,
      plotOutput(outputId = "barplot", height = "640px")
    ),
    column(
      width = 3,
      h4("Einstellungen"),
      p("Wählen Sie eine oder mehrere Länder für den Vergleich aus."),
      checkboxGroupInput(
        inputId = "land",
        label = "Land",
        choices = countries,
        selected = countries
      )
    )
  )
)

server <- function(input, output) {
  plot_df <- reactive({
    req(input$land)
    flights %>% filter(Land %in% input$land)
  })

  output$barplot <- renderPlot({
    plot_data <- plot_df()
    validate(need(nrow(plot_data) > 0, "Bitte mindestens ein Land auswählen."))

    ggplot(plot_data, aes(x = Date, y = Total, fill = Land)) +
      geom_col() +
      labs(
        x = "Datum",
        y = "Gesamtzahl der Flüge pro Woche",
        title = "Gesamtzahl der Flüge pro Woche"
      ) +
      scale_fill_brewer(palette = "Dark2") +
      scale_y_continuous(labels = label_number(big.mark = ".", decimal.mark = ",")) +
      scale_x_date(date_breaks = "6 months", date_labels = "%Y-%m") +
      theme_minimal(base_size = 12) +
      theme(
        panel.grid.minor.x = element_blank(),
        axis.text.x = element_text(angle = 45, hjust = 1),
        legend.position = "bottom"
      )
  })
}

shinyApp(ui, server)
