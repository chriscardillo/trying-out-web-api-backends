library(httr)
library(jsonlite)
library(dplyr)

endpoint <- "http://localhost:5000/api/graphql"

create_user <- function(username, email, password){
  sprintf('mutation {
  createUser(username: "%s", email: "%s", password: "%s"){
          token
    }
  }', username, email, password)
}

check <- POST(endpoint, body = list(query=create_user("mary", "mary@app.com", "pw"))) %>%
  content(as = "text") %>% 
  fromJSON()

my_token <- GET("http://localhost:5000/auth/token",
                httr::content_type_json(),
                authenticate("mary", "pw")) %>%
  content(as = "text") %>%
  fromJSON()

GET("http://localhost:5000/site/secure",
    authenticate(my_token$token, 'NoPwNeeded'))

# Updating the user
POST(endpoint, body = list(query='mutation{updateUser(username: "jim"){token}}'),
     authenticate(my_token$token, 'NoPwNeeded')) %>%
  content(as = "text") %>% 
  fromJSON()

GET("http://localhost:5000/site/secure",
    authenticate(my_token$token, 'NoPwNeeded'))

# app_users()

# Deleting the user
POST(endpoint, body = list(query='mutation{deleteUser{ok}}'),
     authenticate(check$data$createUser$token, 'NoPwNeeded')) %>%
  content(as = "text") %>% 
  fromJSON()

# app_users()