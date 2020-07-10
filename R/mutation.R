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

GET("http://localhost:5000/auth/secure",
    authenticate(check$data$createUser$token, 'NoPwNeeded'))

# Updating the user
POST(endpoint, body = list(query='mutation{updateUser(username: "mary"){token}}'),
     authenticate(check$data$createUser$token, 'NoPwNeeded')) %>%
  content(as = "text") %>% 
  fromJSON()


