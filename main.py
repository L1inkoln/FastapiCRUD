from fastapi import FastAPI
from routers import users, login
import uvicorn
from authx import AuthX
from core.config import authx_config

app = FastAPI()

auth = AuthX(config=authx_config)

auth.handle_errors(app)
app.include_router(users.router)
app.include_router(login.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
