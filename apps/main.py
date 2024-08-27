from fastapi import FastAPI
from user.routers import router as router_user

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(router_user)
