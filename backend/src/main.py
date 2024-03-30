#src/main.py
from fastapi import FastAPI

from src.application.web.api.routers.user_router import user_router


app = FastAPI()
app.include_router(user_router)


# NOTE: This is for development purposes only
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
