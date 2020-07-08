library(httr)
library(jsonlite)
library(dplyr)

GET("http://localhost:5000/auth/token",
     httr::content_type_json(),
    authenticate("Peter", "Yoo"))
