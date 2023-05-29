from fastapi import FastAPI
from tasks_api.sub_task import views as sub_task_views
from tasks_api.task import views as task_views
from tasks_api.task_list import views as task_list_views
from tasks_api.users import views as user_views


def create_app() -> FastAPI:
    """
    Construct the core application.

    The whole function can be divided into 3 steps:
    1. Create a FastAPI app object, which derives configuration values
       (either from a Python class, a config file, or environment variables).
    2. Import the logic that makes up our app (such as routes).
    3. Register routers.

    :return: FastAPI application instance
    """
    # Create FastAPI app
    app = FastAPI(title="Google_tasks", version="0.79.0")

    # Register routers
    app.include_router(user_views.router)
    app.include_router(task_list_views.router)
    app.include_router(task_views.router)
    app.include_router(sub_task_views.router)

    return app
