library(httr)
library(rvest)
library(purrr)
library(dplyr)
library(tidyr)
library(readr)
library(stringr)
library(jsonlite)

available <- read_html("https://github.com/peyo/dtc-and-vin-data/tree/master/dtc/p") %>%
  html_nodes(".Box-row") %>%
  html_node(".js-navigation-open") %>%
  html_text() %>%
  str_subset("json$")

get_dtc <- function(file, location="https://raw.githubusercontent.com/peyo/dtc-and-vin-data/master/dtc/p/"){
  source_url <- paste0(location, file)
  GET(source_url) %>%
    content(as="text") %>%
    fromJSON()
}

dtc_raw <- tibble(file = available) %>%
  mutate(manufacturer = str_replace(file, "\\.json$", ""),
         dtc_fetch = map(file, get_dtc)) %>%
  select(-file) %>%
  unnest(dtc_fetch) %>%
  distinct() %>%
  add_count(tmp_id=paste0(manufacturer, dtc), name = "nb_man_dtc") %>%
  select(-tmp_id) %>%
  filter(description != "escription")

# dtc_raw %>%
#   filter(nb_man_dtc > 1) %>%
#   arrange(manufacturer, dtc, description) %>%
#   select(-nb_man_dtc) %>%
#   readr::write_csv("~/Desktop/duplicate_dtc.csv")

dtc_raw %>%
  filter(nb_man_dtc == 1) %>%
  select(-nb_man_dtc) %>%
  arrange(manufacturer, dtc) %>%
  mutate(id = row_number()) %>%
  select(id, everything()) %>%
  write_csv("../app/data/dtc_p.csv")
