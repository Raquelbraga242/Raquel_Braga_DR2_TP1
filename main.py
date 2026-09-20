from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import events_router
from user_routes import users_router


app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)

    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"

    return response


@app.get("/")
async def welcome() -> dict:
    return {
        "message": "hello world"
    }


app.include_router(events_router)
app.include_router(users_router)
