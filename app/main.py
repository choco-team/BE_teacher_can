from django.conf import settings

from fastapi import FastAPI, Request
from fastapi.exceptions import ResponseValidationError, RequestValidationError
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import auth, user, school, student_list
from .common.consts import DJANGO_SECRET_KEY, ALLOWED_HOSTS
from .errors import exceptions as ex

# django auth 사용을 위한 config
settings.configure(
    SECRET_KEY=DJANGO_SECRET_KEY,
    USE_I18N=False,
    AUTH_PASSWORD_VALIDATORS=[
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ],
)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/api")


# middleware
## CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
## TrustedHost 미들웨어
app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)

# router
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(school.router)
app.include_router(student_list.router)


# 예외 처리
@app.exception_handler(ex.APIException)
async def exception_handelr(request, exc):
    return await ex.api_exception_handelr(request, exc)


@app.exception_handler(RequestValidationError)
async def exception_handelr(request, exc):
    return await ex.request_exception_handelr(request, exc)


@app.exception_handler(ResponseValidationError)
async def exception_handelr(request, exc):
    return await ex.response_exception_handelr(request, exc)


@app.exception_handler(Exception)
async def exception_handelr(request, exc):
    return await ex.response_exception_handelr(request, exc)


@app.get("/")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}
