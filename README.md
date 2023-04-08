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

Is used to register and get access token (or refresh access token) for authorizing the requests.

  **Endpoints:**
<ul>
<li><h4>POST /api/auth/</h4> -  user registration</li>
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
<li><h4>POST /api/auth/token/</h4> -  getting access and refresh tokens for registrated user</li>
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
<li><h4>POST /api/auth/token/refresh/</h4> -  getting access and refresh tokens for registrated user</li>
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
   
   
    
