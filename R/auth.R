library(httr)
library(jsonlite)
library(dplyr)

my_token <- GET("http://localhost:5000/auth/token",
     httr::content_type_json(),
    authenticate("Chris", "Car")) %>%
  content(as = "text") %>%
  fromJSON()

GET("http://localhost:5000/auth/secure",
    authenticate(my_token$token, 'NoPwNeeded'))

# If you change your password, the token won't work anymore :)
# PUT("http://localhost:5000/api/restless/users/2",
#     httr::content_type_json(),
#     body = toJSON(list(password="PWChanged"), auto_unbox = T))
