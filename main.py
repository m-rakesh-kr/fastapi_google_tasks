import uvicorn
from tasks_api import create_app

# import logging
#
# # Disable all logging
# logging.disable(logging.CRITICAL)
#
# # Disable SQLAlchemy logging only
# logging.getLogger('sqlalchemy').disabled = True

# logging.getLogger('sqlalchemy').setLevel(logging.INFO)

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
