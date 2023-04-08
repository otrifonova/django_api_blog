Django REST API application for blog.

<h1>Launching:</h1>
<ol>
<li>Clone repository</li>
<li>Create and activate virtual environment:

    $ python -m venv venv
    $ source venv/bin/activate
</li>
<li>Install dependencies:

    $ pip install -r requirements.txt
</li>  
<li>Create .env file and set global variables in it (SECRET_KEY and database (PostgreSQL) data: DB_NAME, DB_USER, DB_PASSWORD</li> 
<li>Run database migration:

    $ python manage.py makemigrations
    $ python manage.py migrate
</li> 
<li>To run local server (at http://127.0.0.1:8000/) execute:

    $ python manage.py runserver
</li> 
<li>To run unit tests execute:

    $ python manage.py tests
</li> 

<h1>API methods</h1>

<h3>Registration and authorization</h3>

 Allows to register and get access token (or refresh access token) for authorizing the requests. Access token is valid for 1 day, refresh token is valid for 7 days.

  **Endpoints:**
<ul>
<li><h4>POST /api/auth/</h4> - register a new user</li>
</ul>
<br>

  Header params
  
*Content-Type: application/json*

<br>

  Body params: 

*username* (required) - This value may contain only letters, numbers, and @/./+/-/_ characters. Must be unique (does not exist in the database).

*password* (required) - Must be a valid password (at least 8 characters, not too common, not too similar to username).

*email* - Must be a valid email address.

*first_name*

*last_name*

<br>

  Response examples:
  
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
    
<ul>
<li><h4>POST /api/auth/token/</h4> - get access and refresh tokens for registrated user</li>
</ul>
<br>

  Header params
  
*Content-Type: application/json*

<br>

  Body params: 

*username* (required)

*password* (required)

<br>

  Response examples:
  
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
    
<ul>
<li><h4>POST /api/auth/token/refresh/</h4> - get new access token</li>
</ul>
<br>

  Header params
  
*Content-Type: application/json*

<br>

  Body params: 

*refresh* (required) - Contains a refresh token

<br>

  Response examples:
  
    HTTP 200 OK
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    }


    HTTP 401 Unauthorized
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }
   
   
<h3>Creating and getting posts</h3>

Allows to create posts (for authorized users, acces token required) and get list of all posts or certain user's posts sorted by publication date in order from newest to olders. Post contains of fields: title, text, publication date, author. Field author gets a current authorized user, publication date gets a current UTS date and time value.

  **Endpoints:**
<ul>
<li><h4>POST /api/post/</h4> - create post</li>
</ul>
<br>    

  Header params
  
*Content-Type: application/json*

*Authorization: Bearer {acces_token}*

<br>

  Body params: 

*title* (required) - Max length 80 characters.
*text* (required)

<br>


  Response examples:
  
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

   
<ul>
<li><h4>GET /api/post/</h4> - get all posts</li>
</ul>
<br>    

  Response examples:   
  
  
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
            "id": 2,
            "title": "TextTitle2",
            "text": "TestText2",
            "author_id": 2,
            "pub_date": "2023-04-07T17:37:16.608617Z"
        },
        {
            "id": 1,
            "title": "TextTitle1",
            "text": "TestText1",
            "author_id": 1,
            "pub_date": "2023-04-07T17:36:07.213059Z"
    ]
<ul>
<li><h4>GET /api/post/{user_id}/</h4> - get all posts by user with id = user_id</li>
</ul>
<br>    

 Path params:
 
 *user_id* - integer
 
<br>

 Response examples:
 
 
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
