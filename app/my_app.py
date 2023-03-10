from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers.posts import router as post_router
from app.routers.users import router as user_router

app = FastAPI()


app.include_router(user_router)
app.include_router(post_router)
add_pagination(app)
