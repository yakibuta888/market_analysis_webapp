#src/main.py
from fastapi import FastAPI

from src.api.routers.user_router import user_router
# from tools.controller import visualize


app = FastAPI()
app.include_router(user_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # visualize.make_graph()
