from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["auth"])


# 추후 구현 예정
@router.post("/login")
async def login():
    """로그인 (추후 구현)"""
    return {"message": "로그인 기능은 추후 구현 예정입니다."}


@router.post("/signup")
async def signup():
    """회원가입 (추후 구현)"""
    return {"message": "회원가입 기능은 추후 구현 예정입니다."}


@router.post("/logout")
async def logout():
    """로그아웃 (추후 구현)"""
    return {"message": "로그아웃 기능은 추후 구현 예정입니다."}
