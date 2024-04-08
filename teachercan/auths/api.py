from datetime import datetime, timedelta

from ninja import Router
from ninja.security import HttpBearer
from django.contrib.auth import authenticate, login
from jwt import encode, decode


from config.settings import JWT_ALGORITHM, JWT_SECRET
from teachercan.users.models import User
from .schemas import EmailIn, SignUpIn, SignInIn
import config.exceptions as ex


class AuthBearer(HttpBearer):
    def authenticate(self, request, token=""):
        try:
            payload = decode(token, JWT_SECRET, JWT_ALGORITHM)
            user = User.objects.get(email=payload["email"])
            login(request, user)
        except:
            raise ex.invalid_token
        return user


router = Router(tags=["Auth"])


# 1.이메일 중복검사
@router.post("/signup/validation", response={201: str})
def is_email_usable(request, payload: EmailIn):
    """
    `이메일 중복검사`
    """
    if User.objects.has_user(payload.email):
        raise ex.email_already_exist
    return 201, "이 이메일은 사용할 수 있어요."


# 2.회원가입
@router.post("/signup", response={201: str})
def signup(request, user: SignUpIn):
    """
    `회원가입`
    """
    User.objects.create_user(
        email=user.email, password=user.password, nickname=user.nickname
    )
    return 201, "회원가입이 완료되었어요."


# 3.로그인
@router.post("/signin", response={200: dict})
def signin(request, user: SignInIn):
    """
    `로그인`
    """
    db_user: User = authenticate(email=user.email, password=user.password)
    if db_user:
        login(request, db_user)

        # Create jwt
        token = encode(
            {"email": db_user.email, "exp": datetime.utcnow() + timedelta(hours=24)},
            JWT_SECRET,
            JWT_ALGORITHM,
        )
        return 200, {"token": token}

    if User.objects.has_user(user.email):
        raise ex.password_not_match
    raise ex.not_found_user
