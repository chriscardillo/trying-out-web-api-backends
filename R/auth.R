# Gives back token
POST("http://localhost:5000/auth/login",
     httr::content_type_json(),
     body = toJSON(list(username=" Peter ",
                        password = "Yoo"), auto_unbox = T))

# Does not give back token
POST("http://localhost:5000/auth/login",
     httr::content_type_json(),
     body = toJSON(list(username=" Chris ",
                        password = "Yoo"), auto_unbox = T))


GET("http://localhost:5000/auth/test",
     httr::content_type_json(),
    authenticate("Peter", "Yoo"))
