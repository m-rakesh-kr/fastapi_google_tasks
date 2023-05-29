import os
from dotenv import load_dotenv

load_dotenv()

# JWT and Authentication Constants
ALGORITHM = os.getenv('ALGORITHM')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')
JWT_FORGOT_PASSWORD_SECRET_KEY = os.getenv('JWT_FORGOT_PASSWORD_SECRET_KEY')

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
FORGOT_PASSWORD_EXPIRE_MINUTES = 10
RESET_PASSWORD_LINK = os.getenv('RESET_PASSWORD_LINK')

# Regular Expressions
EMAIL_REGEX = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,12}$"

# Error Messages
INVALID_EXPIRED_TOKEN_MSG = "Invalid/Expired Token"
USER_NOT_FOUND_OF_TOKEN_MSG = "There is no user associated with this token!"

PASSWORD_RESET_SUBJECT = "Password Reset"
PASSWORD_RESET_MAIL_LINK_MSG = "Click on the link below to reset your password."
PASSWORD_RESET_MAIL_MSG = "An email has been sent to your email address. Please check your inbox."

ERR_USERNAME_WRONG = "Please enter a valid username!"
ERR_PASSWORD_WRONG = "Please enter a valid password!"
PASSWORD_PATTERN_HINT = "The password must be between 8 and 12 characters long, contain at least one lowercase letter, " \
                       "one uppercase letter, one digit, and one special character from @$!%*#?&."
ERR_EMAIL_WRONG = "Please enter a valid email!"
ERR_PASSWORD_INCORRECT = "The current password does not match the user's password"
ERR_PASSWORD_NOT_MATCH = "The confirm password does not match"
ERR_SQL_ALCHEMY_ERROR = "An error occurred while storing data in the database."
ERR_EMAIL_ALREADY_TAKEN = "The email {} is already registered. Please use another email."

MSG_REGISTER_USER_SUCCESSFULLY = "Hey {}, you have successfully registered."
MSG_PASSWORD_RESET = "Your password has been successfully reset."
MSG_USER_NOT_AVAILABLE = "User with the ID {} is not available."
MSG_INVALID_CREDENTIALS = "Username (email ID) not found! Invalid credentials."
MSG_INVALID_PASSWORD = "Incorrect password."
MSG_UPDATE_PASSWORD = "Password has been changed successfully!"
MSG_USER_CREATED = "User created successfully!"

MSG_TASK_LIST_NOT_FOUND = "There is no task list with the ID {}."
MSG_TASK_LIST_UPDATED = "Task list updated successfully."
MSG_TASK_LIST_DELETED = "Task list deleted successfully."
EMAIL_NOT_EXIST = "Email {} does not exist!"

MSG_TASK_LIST_NOT_FOUND2 = "You do not have any task list with the ID {}."
MSG_TASK_NOT_FOUND = "There is no task with the ID {}."
MSG_TASK_UPDATED = "Task updated successfully."
MSG_TASK_DELETED = "Task deleted successfully."

MSG_TASK_NOT_FOUND2 = "There are no subtasks for the task with the ID {}."
MSG_SUB_TASK_NOT_FOUND = "There is no any subtask created with the ID {}."
MSG_SUB_TASK_UPDATE_FORBIDDEN = "You have not authorization to update this task"
MSG_SUB_TASK_UPDATED = "Subtask updated successfully."
MSG_SUB_TASK_DELETE_FORBIDDEN = "You have not authorization to delete this task"
MSG_SUB_TASK_DELETED = "Subtask deleted successfully."

# Task Alert Messages
TASK_ALERT_SUBJECT = "Task Alert for Your Google Task"
TASK_ALERT_MSG_BEFORE = "This is a notification for your task created on a given date. It has 15 minutes remaining."
TASK_ALERT_MSG_CURRENT = "This is a notification for your task created on a given date. It is now overdue."
TASK_ALERT_DEADLINE_MSG = "Sorry, the deadline for your task created on a given date has passed."

# Subtask Alert Messages
SUB_TASK_ALERT_SUBJECT = "Subtask Alert for Your Google Task"
SUB_TASK_ALERT_MSG_BEFORE = "This is a notification for your subtask created on a given date. It has 15 minutes remaining."
SUB_TASK_ALERT_MSG_CURRENT = "This is a notification for your subtask created on a given date. It is now overdue."
SUB_TASK_ALERT_DEADLINE_MSG = "Sorry, the deadline for your subtask created on a given date has passed."

USER_CREATION_EMAIL_ALERT_TITLE = "User Registration"
USER_CREATION_EMAIL_ALERT_MSG = "Welcome to our application!", "Your account has been created successfully."
FORGET_USER_PASSWORD_ALERT_TITLE= "Reset Password Link"
FORGET_USER_PASSWORD_ALERT_MSG = "Using this below link you can reset you password."
