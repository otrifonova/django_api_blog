<h1>Launching:</h1>
<ol>
<li>Clone the repository</li>
<li>Create and activate virtual environment:

    $ python -m venv venv
    $ source venv/bin/activate
</li>
<li>Install dependencies:

    $ pip install -r requirements.txt
</li>  
<li>Create .env file and set global variables in it (SECRET_KEY and database (PostgreSQL) data: DB_NAME, DB_USER, DB_PASSWORD)</li> 
<li>Run a database migration:

    $ python manage.py makemigrations
    $ python manage.py migrate
</li> 
<li>Create a superuser:

    $ python manage.py createsuperuser
</li> 
<li>To run unit tests execute:

    $ python manage.py tests
</li>
<li>To run a local server (at http://127.0.0.1:8000/) execute:

    $ python manage.py runserver

The Django admin interface is available on <b>/admin/</b>
</li>
</ol>

<h1>API methods</h1>

Registrate and authenticate the user:
<ul>
    <li>POST /api/auth/ - register a new user</li>
    <li>POST /api/auth/token/ - get an access and a refresh tokens for a registered user</li>
    <li>POST /api/auth/token/refresh/ - get a new access token</li>
</ul>

Create and get a list of posts:
<ul>
    <li>POST /api/post/ - create a post (authorized)</li>
    <li>GET /api/post/{user_id}/ - get all posts (optionally by a user with id = user_id}</li>
</ul>

Get a list of users:
<ul>
    <li>GET /api/user/ - get a list of users (with a query parameter "sorting=posts_desc|posts_asc" for sorting by number of posts)</li>
</ul>

Follow or unfollow a user:
<ul>
    <li>PUT /api/user/{user_id}/follow - follow a user with id=user_id (authorized)</li>
    <li>PUT /api/user/{user_id}/unfollow - stop following a user with id=user_id (authorized)</li>
</ul>


<h3>Registrate and authenticate the user</h3>

 Allow to register and get an access token (or a refresh access token) for authorizing the requests. The access token is valid for 1 day, the refresh token is valid for 7 days.

<ul>
<li><h4>POST /api/auth/</h4> - register a new user</li>
</ul>

<br>

  <h6>Header params</h6>
  
*Content-Type: application/json*

<br>

  <h6>Body params:</h6> 

*username* (required) - This value may contain only letters, numbers, and @/./+/-/_ characters. Must be unique (does not exist in the database).

*password* (required) - Must be a valid password (at least 8 characters, not too common, not too similar to the username).

*email* (optional)- Must be a valid email address.

*first_name* (optional)

*last_name* (optional)

<br>

  <h6>Response examples:</h6>
  
    HTTP 201 Created
    {
        "email": "johndoe@example.com",
        "username": "johndoe1",
        "id": 9
    }


    HTTP 400 Bad Request
    {
        "email": [
            "Enter a valid email address."
        ],
        "username": [
            "A user with that username already exists."
        ],
        "password": [
            "The password is too similar to the username.",
            "This password is too short. It must contain at least 8 characters."
        ]  
    }
    
<br>

<ul>
<li><h4>POST /api/auth/token/</h4> - get an access and a refresh tokens for a registered user</li>
</ul>

<br>

  <h6>Header params</h6>
  
*Content-Type: application/json*

<br>

  <h6>Body params: </h6>

*username* (required)

*password* (required)

<br>

  <h6>Response examples:</h6>
  
  
    HTTP 200 OK
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    }


    HTTP 401 Unauthorized
    {
         "detail": "No active account found with the given credentials"
    }
    
    
    HTTP_400_BAD_REQUEST
    {
        "email": [
            "Enter a valid email address."
        ],
        "username": [
            "A user with that username already exists."
        ],
        "password": [
            "The password is too similar to the username.",
            "This password is too short. It must contain at least 8 characters."
        ]  
    }
    
<br>

<ul>
<li><h4>POST /api/auth/token/refresh/</h4> - get a new access token</li>
</ul>

<br>

  <h6>Header params</h6>
  
*Content-Type: application/json*

<br>

  <h6>Body params: </h6>

*refresh* (required) - Contains a refresh token

<br>

  <h6>Response examples:</h6>
  
    HTTP 200 OK
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    }


    HTTP 401 Unauthorized
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }

<br>

<h3>Create and get a list of posts</h3>

Allow to create posts (for the authorized users, an access token required) and get a list of all the certain user's posts sorted by a publication date in order from newest to oldest. The post contains fields: title, text, publication date, author. The field "author" gets a current authorized user, the field "publication date" gets a current UTC date and time value.

<br>

<ul>
<li><h4>POST /api/post/</h4> - create a post</li>
</ul>

<br>    

  <h6>Header params</h6>
  
*Content-Type: application/json*

*Authorization: Bearer {access_token}*

<br>

  <h6>Body params: </h6>

*title* (required) - Max length 80 characters.

*text* (required)

<br>

  <h6>Response examples:</h6>
  
    HTTP 201 Created
    {
        "id": 9,
        "title": "title",
        "text": "text text text",
        "author_id": 1,
        "pub_date": "2023-04-08T12:24:51.185666Z"
    }

    HTTP 401 Unauthorized
    {
        "detail": "Authentication credentials were not provided."
    }
    
    HTTP 400 Bad Request
    {
        "title": [
            "This field is required."
        ],
        "text": [
            "This field is required."
        ]
    }

<br>

<ul>
<li><h4>GET /api/post/{user_id}/</h4> - get all posts (optionally by a user with id = user_id)</li>
</ul>

<br>    

 <h6>Path params:</h6>
 
 *user_id* (optional) - integer

<br>

 <h6>Response examples:</h6>
 
    HTTP 200 OK
    [
       {
            "id": 3,
            "title": "TextTitle3",
            "text": "TestText3",
            "author_id": 1,
            "pub_date": "2023-04-07T17:39:37.172921Z"
        },
        {
            "id": 1,
            "title": "TextTitle1",
            "text": "TestText1",
            "author_id": 1,
            "pub_date": "2023-04-07T17:36:07.213059Z"
        }
    ]

<br>

<h3>Get a list of users</h3>

Allow to get a list of users optionally sorted by number of posts.

<ul>
<li><h4>GET /api/user/</h4> - get a list of users</li>
</ul>

<br>

  <h6>Query params</h6>

*sorting* (optional) - "posts_desc" to sort in descending order, "posts_asc" to sort in ascending order

<br>

  <h6>Response examples:</h6>
  
    HTTP 200 OK
    [
    {
        "id": 1,
        "username": "admin",
        "number_of_posts": 9
    },
    {
        "id": 2,
        "username": "johndoe",
        "number_of_posts": 3
    },
    {
        "id": 3,
        "username": "janedoe",
        "number_of_posts": 5
    }
    ]

<br>

<h3>Follow or unfollow a user</h3>

Allows authorized users to start and stop following the posts of another user.

<ul>
<li><h4>PUT /api/user/{user_id}/follow</h4> - start following a user with id=user_id.</li>
</ul>

<br>

  <h6>Path params</h6>
*user_id* (required)

<br>

  <h6>Header params</h6>
*Authorization: Bearer {access_token}*

<br>

   <h6>Response examples:</h6>

    HTTP 200 OK
    {
    "message": "User with id 3 was successfully followed."
    }

    HTTP 200 OK
    {
    "message": "User with id 2 is already followed."
    }

    HTTP 400 Bad Request
    {
    "message": "Cannot follow yourself."
    }

<br>

<ul>
<li><h4>PUT /api/user/{user_id}/unfollow</h4> - stop following a user with id=user_id.</li>
</ul>

<br>

  <h6>Path params</h6>
*user_id* (required)

<br>

  <h6>Header params</h6>
*Authorization: Bearer {access_token}*

<br>

  <h6>Response examples:</h6>

    HTTP 200 OK
    {
    "message": "User with id 3 was successfully unfollowed."
    }

    HTTP 200 OK
    {
    "message": "User with id 2 is already not followed."
    }

    HTTP 400 Bad Request
    {
    "message": "Cannot unfollow yourself."
    }
