library(dplyr)
library(shiny)
library(ggplot2)
library(markdown)

flights <- readr::read_csv("fluege.csv")


ui <- fluidPage(
  
  
  titlePanel("Europäischer Flugverkehr während der COVID-Pandemie"),
  
  markdown("
           Mit dem Ausbruch der Covid-19-Pandemie im März 2020 ist die Zahl der Flüge die an europäischen Flughäfen ankommen oder von dort abfliegen drastisch zurückgegangen. 
           "),
  
  
  fluidRow(
    
    column(10, 
           plotOutput(outputId = "barplot")
    ),
    
    column(2,
           markdown("### **Einstellungen**
              
               Verwenden Sie die unten stehenden Selektoren, um eine Reihe von Ländern auszuwählen, die Sie erkunden möchten.
               "),
           checkboxGroupInput(
             inputId = "land",
             label = "Land",
             choices = c("Belgium", "Frankreich", "Ireland", "Luxemburg", "Niederlande", "UK"),
             selected = c("Belgium", "Frankreich", "Ireland", "Luxemburg", "Niederlande", "UK")
           )
    )
  )
)



server <- function(input, output) {
  
  
  plot_df <- reactive({
    req(input$land)
    plot_df <- flights %>% 
      filter(Land %in% input$land) 
    plot_df
  })
  
  
  output$barplot <- renderPlot({
    plot_df <- plot_df()
    ggplot(data = plot_df, 
           mapping = aes(x = Date,
                         y = Total,
                         fill = Land)) +
      geom_col() +
      labs(x = "Jahr",
           y = "Gesamtzahl der Flüge pro Woche", 
           title = "Gesamtzahl der Flüge pro Woche") +
      scale_fill_brewer(palette = "Dark2") +
      theme_minimal() +
      theme(panel.grid.major.x = element_blank(),
            panel.grid.minor.x = element_blank())
  })
  
}

shinyApp(ui, server)
