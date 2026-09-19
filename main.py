from fastapi import FastAPI
from routes import events_router
from user_routes import users_router


app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {
        "message": "hello world"
    }


app.include_router(events_router)
app.include_router(users_router)
