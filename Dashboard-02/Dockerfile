FROM rocker/r-ver:4.3.3

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

RUN R -e "install.packages(c('shiny','dplyr','ggplot2','readr','scales'), repos='https://cloud.r-project.org')"

WORKDIR /app
COPY . /app

EXPOSE 3838

CMD ["R", "-e", "app <- source('/app/db.R', local = TRUE)$value; shiny::runApp(app, host='0.0.0.0', port=as.integer(Sys.getenv('PORT', '3838')))"]
