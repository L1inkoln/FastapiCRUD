from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.user import UserLoginShema
from authx import AuthX, RequestToken
from core.config import authx_config
from services.user_service import UserService


router = APIRouter(tags=["auth"])


auth: AuthX = AuthX(config=authx_config)


@router.post("/login")
async def login(creds: UserLoginShema, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.authenticate_user(creds.username, creds.password)
    if user:
        token = auth.create_access_token(uid=str(user.id))
        return {"access_token": token}
    raise HTTPException(status_code=401, detail={"message": "Invalid credentials"})


@router.get("/tokentest", dependencies=[Depends(auth.get_token_from_request)])
async def get_protected(token: RequestToken = Depends()):
    try:
        auth.verify_token(token=token)
        return {"message": "Authentication is successful"}
    except Exception as e:
        raise HTTPException(status_code=401, detail={"message": str(e)}) from e
