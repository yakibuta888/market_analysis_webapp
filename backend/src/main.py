#src/main.py
from fastapi import FastAPI

from src.application.web.api.routers.asset_router import asset_router
from src.application.web.api.routers.futures_data_router import futures_data_router
from src.application.web.api.routers.user_router import user_router


app = FastAPI()
app.include_router(asset_router)
app.include_router(futures_data_router)
app.include_router(user_router)


# NOTE: This is for development purposes only
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
