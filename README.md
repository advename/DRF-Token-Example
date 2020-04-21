# DRF-Token-Example
An example of how to send the Token in HttpOnly cookies and the CSRF token inside the body for cross domain usage. 


## Installation
1. Create a new project directory with a virtual environment
2. Install dependencies in the activated venv using `pip install -r requirements.txt`
3. Create a new user with `python manage.py createsuperuser`
4. Add a token to your new user `python manage.py drf_create_token USERNAME`
4. Run the server using `python manage.py runserver`

## How to use
You can send POST requests to `example.com/api/v1/login` (example.com should be your localhost or 127.0.0.1:8000 or whereever you run your Django projects),
with login credentials in JSON format like:
```
{
    "username": "admin",
    "password": "hello"
}
```
and you receive the auth token in an HttpOnly cookie. The csrf_token is send inside the response body and should be stored in local storage.

Now, you can view protected endpoints like `example.com/api/v1/posts/`


## Project structure
This project is a simple demonstration of a "blog website" that also has a REST API endpoint that can be consumed by mobile devices, 
but also from other websites having a different domain (cross domain).

This project, you need to imagine if the blog website already existed with all apps and frontend pages using Django templating system.

All posts are inside the `posts_app` directory. The posts should be accessed using the API, therefore, `posts_app` has a subdirectory, the `api/`
directory handling API views and urls.

The `posts_app/api/` directory is included inside the `api_app/` application, because we want to have one unified `example.com/api/v1` API endpoint and not
an API endpoint for each application (like this: `example.com/post/api` ).

## Authentication and Authorization
#### By default, DRF's `TokenAuthorization` and `IsAuthentication` system flow is like this:
1. The client send credentials inside the body to the API login endpoint `api/login/`
2. Our API endpoint verifies the credentials, and if valid, a token should be returned in the body
3. The client takes the token and stores it locally (Session storage, local storage or cookie)
4. On subsequent requests, the client uses the stored token and adds it in the header like `Authorize: Token <token>` to get authorized

This setup has one big flaw when the API is consumed in web applications. The stored token in the frontend is vulnerable to XSS attacks.

#### A better approach would be:
1. The client send credentials inside the body to the API login endpoint `api/login/`
2. Our API endpoint verifies the credentials, and if valid, sends the token in an HttpOnly cookie back to the client (not accessible by JavaScirpt
, so no XSS attack possible). Moreover, the CSRF token is passed in the body. Now only the CSRF token should be stored inside local storage.
3. On subsequent requests, the client browser automatically passes along the token. Now the only thing the client manually has to do is
to take the stored csrf token and sends it in the header like `X-CSRFToken: <csrf_token>`.

Thanks to HttpOnly Cookies, the token is not prone to XSS requests. But now it is vulnerable to CSRF attacks. That's why the
CSRF-token should be stored in local storage and required to perform data modification requests.

To implement this, have i done the following:
1. Create a custom permission class to first check for the csrf token and second check if the passed token is valid -> `blogs_project/permissions.py`
2. Include the custom permission class and use it as the default class. Now all `example.com/api/v1/posts` endpoints are protected.
3. Created a custom Login view inside `api_app/views.py` that sends the auth token in an HttpOnly cookie and the csrf_token in the body, if the provided credentials are correct.
4. Thanks to our custom permission class, the user authenticated user can now access the protected posts endpoint.

### Example of cross domain website
An example, of how such a cross domain website that would like to access our API endpoint could look like is this simple HTML file:
```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fake Frontend Website</title>
</head>

<body>
    <h1>Awesome Million dollar Application</h1>

    <button>Try me</button>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.0/jquery.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/js-cookie@rc/dist/js.cookie.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script>
        let csrf = "";
        const credentials = {
            username: "admin",
            password: "hello"
        }

        //Initial login request
        fetch("http://127.0.0.1:8000/api/v1/auth/login/", {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            method: "POST",
            credentials: 'include',
            body: JSON.stringify(credentials)
        }).then(res => {
            return res.json()
        }).then(json => {
            console.log(json)
            csrf = json.csrf;
            console.log("Cookies are: ", Cookies.get())
        });

        // New POST request, using the credentials from the initial login
        document.querySelector("button").addEventListener("click", function () {
            fetch("http://127.0.0.1:8000/api/v1/posts/",
                {
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf
                    },
                    method: "POST",
                    credentials: 'include',
                }

            ).then(res => {
                return res.json()
            }).then(json => {
                console.log(json)
            });
        })
    </script>
</body>

</html>
```



