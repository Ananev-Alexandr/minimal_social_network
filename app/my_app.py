from fastapi import FastAPI
from routers.users import router as user_router
from routers.posts import router as post_router
from fastapi_pagination import add_pagination


app = FastAPI()


app.include_router(user_router)
app.include_router(post_router)
add_pagination(app)
