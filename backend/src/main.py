from fastapi import FastAPI

from .api.routers import user_router
from tools.controller import visualize


if __name__ == '__main__':
    app = FastAPI()
    app.include_router(user_router)

    visualize.make_graph()
