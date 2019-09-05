null = None

get_paginated_users_query = '''{
  users(first: 2) {
    pageInfo {
      endCursor
      startCursor
      hasNextPage
      hasPreviousPage
    }
    count
    edges {
      cursor
      node {
        username
        firstName
        lastName
        email
      }
    }
  }
}'''

get_paginated_users_response = {
  "data": {
    "users": {
      "pageInfo": {
        "endCursor": "YXJyYXljb25uZWN0aW9uOjA=",
        "startCursor": "YXJyYXljb25uZWN0aW9uOjA=",
        "hasNextPage": False,
        "hasPreviousPage": False
      },
      "count": 1,
      "edges": [
        {
          "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
          "node": {
            "username": "Tim",
            "firstName": "Timothy",
            "lastName": "Kamau",
            "email": "tim@app.com"
          }
        }
      ]
    }
  }
}


create_user_mutation = '''mutation{createUser (
  username:"Jimmy",
  email:"jimmy@app.com",
  password:"Teamore123",
	firstName:"Timothy",
	lastName:"Kamau"){
  user {
    username
    email
    firstName
    lastName
  }
}
}'''

create_user_response = {
  "data": {
    "createUser": {
      "user": {
        "username": "Jimmy",
        "email": "jimmy@app.com",
        "firstName": "Timothy",
        "lastName": "Kamau"
      }
    }
  }
}