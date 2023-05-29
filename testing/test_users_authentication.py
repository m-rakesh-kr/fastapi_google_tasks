import os
import json


def test_read_server(client):
    response = client.get("api/v1/auth/test_server")
    assert response.status_code == 200
    assert response.json() == 'Server is working'


"""------------------------------------------------------------------"""
"""
Below are Registration Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 4 Nos

test_registration_success_200: Successful User Registration      : 200
test_registration_email_exists_409: Email-ID Already Exists      : 409
test_registration_invalid_email_401: Invalid Email-ID Format     : 401 
test_registration_password_mismatch_401: Password Mismatch Error : 401
test_registration_password_format_401: Incorrect Password Format : 401
"""
"""-------------------------------------------------------------------"""


def test_registration_success_200(client):
    data = {
        "name": os.getenv("name"),
        "email": os.getenv("email"),
        "password": os.getenv("password"),
        "confirm_password": os.getenv("confirm_password")
    }
    response = client.post('/api/v1/auth/register', json.dumps(data))
    # print(f"RETURN{response.json()}")
    assert response.status_code == 201
    assert response.json()["name"] == data['name']
    assert response.json()["email"] == data['email']


def test_registration_email_exists_409(client):
    data = {
        "name": os.getenv('name'),
        "email": os.getenv('email'),
        "password": os.getenv('password'),
        "confirm_password": os.getenv('confirm_password')
    }
    response = client.post('/api/v1/auth/register', json.dumps(data))
    assert response.status_code == 409
    assert f"The Email {data['email']} is already registered plz use another email."


def test_registration_invalid_email_401(client):
    data = {
        "name": os.getenv('name'),
        "email": os.getenv('invalid_email'),
        "password": os.getenv('password'),
        "confirm_password": os.getenv('confirm_password')
    }
    response = client.post('/api/v1/auth/register', json.dumps(data))
    assert response.status_code == 401
    assert "Please enter valid email!"


def test_registration_password_mismatch_401(client):
    data = {
        "name": os.getenv('name'),
        "email": os.getenv('mismatch_email'),
        "password": os.getenv('password'),
        "confirm_password": os.getenv('mismatch_confirm_password')
    }
    response = client.post('/api/v1/auth/register', json.dumps(data))
    assert response.status_code == 401
    assert "Confirm Password not matching"


def test_registration_password_format_401(client):
    data = {
        "name": os.getenv('name'),
        "email": os.getenv('email'),
        "password": os.getenv('invalid_format_password'),
        "confirm_password": os.getenv('confirm_password')
    }
    response = client.post('/api/v1/auth/register', json.dumps(data))
    assert response.status_code == 401
    assert "Please enter valid password!"


"""------------------------------------------------------------------"""
"""
Below are Login Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_login_success_200: Successful User Login                    : 200
test_login_incorrect_credentials_404: Incorrect Credentials      : 404
test_login_incorrect_password_404: Incorrect Password            : 404
"""
"""-------------------------------------------------------------------"""


def test_login_success_200(client):
    data = {
        "username": os.getenv('email'),
        "password": os.getenv('password'),
    }
    response = client.post('/api/v1/auth/login', data)
    assert response.status_code == 200
    assert "access_token: {}, refresh_token: {}, token_type: bearer"


def test_login_incorrect_credentials_404(client):
    data = {
        "username": "unknown@user.in",
        "password": "UnknownUser@1234"
    }
    response = client.post('/api/v1/auth/login', data)
    assert response.status_code == 404
    assert "User Not Found"


def test_login_incorrect_password_404(client):
    data = {
        "username": os.environ.get('email'),
        "password": "User@12345"
    }
    response = client.post('/api/v1/auth/login', data)
    assert response.status_code == 404
    assert "Username(Email id) not found! Invalid Credentials"


"""--------------------------------------------------------------------"""
"""
Below are Forgot Password Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_forgot_password_200: Email-IS Exists & Token Sent Success   : 200
test_forgot_password_user_not_found_404: User Not Found          : 404
test_forgot_password_token_sent_404: Token Already Sent          : 404
"""
"""--------------------------------------------------------------------"""


def test_forgot_password_200(client):
    data = {
        "email": os.environ.get('email'),
    }
    response = client.post('/api/v1/auth/forgot_password', json.dumps(data))
    # print(f"RESPONSE {response.json()}")
    assert response.status_code == 200
    assert response.json()["Reset Password Link"]


def test_forgot_password_user_not_found_404(client):
    data = {
        "email": "inexture@gmail.com"
    }
    response = client.post('/api/v1/auth/forgot_password', json.dumps(data))
    assert response.status_code == 404
    assert f"Email {data['email']} does not exist!"


"""------------------------------------------------------------------"""
"""
Below are Reset Password Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_reset_password_200: Token is Correct & password has Reset   : 200
test_reset_password_incorrect_token_404: Incorrect Token Entered : 404
test_reset_password_password_mismatch_404: New Password Mismatch : 404
"""
"""-----------------------------------------------------------------"""


def test_reset_password_200(client, reset_password_access_token):
    data = {
        "password": os.getenv('password'),
        "confirm_password": os.getenv('confirm_password')
    }
    response = client.post(f'/api/v1/auth/reset_password/{reset_password_access_token}', json.dumps(data))
    # print(f"RESPONSE {response.json()}")
    assert response.status_code == 200
    assert response.json()["message"]


def test_reset_password_incorrect_token_404(client):
    data = {
        "password": os.environ.get('password'),
        "confirm_password": os.environ.get('confirm_password')
    }
    response = client.post('/api/v1/auth/reset_password/incorrect_token', json.dumps(data))
    # print(f"RESPONSE {response.json()}")
    assert response.status_code == 404
    assert "Incorrect Token"


def test_reset_password_mismatch_404(client, reset_password_access_token):
    data = {
        "password": os.getenv('password'),
        "confirm_password": os.getenv('mismatch_confirm_password')
    }
    response = client.post(f'/api/v1/auth/reset_password/{reset_password_access_token}', json.dumps(data))
    print(f"RESPONSE {response.json()}")
    assert response.status_code == 401
    assert "Confirm Password not matching"


def test_get_user_200(client):
    response = client.get('/api/v1/auth/user/1')
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200


def test_get_user_404(client):
    response = client.get('/api/v1/auth/user/5')
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
