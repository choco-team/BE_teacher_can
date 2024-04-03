from django.template import TemplateSyntaxError
from ninja import NinjaAPI
from ninja.errors import AuthenticationError, ValidationError, HttpError

from config import exceptions as ex
from config.renderers import DefaultRenderer
from teachercan.auths.api import router as auth_router
from teachercan.users.api import router as user_router
from teachercan.students.api import router as student_router
from teachercan.schools.api import router as school_router
from teachercan.student_lists.api import router as student_list_router
from teachercan.columns.api import router as column_router


api = NinjaAPI(
    renderer=DefaultRenderer(),
    title="Teachercan API",
)


# token인증 예외처리
@api.exception_handler(AuthenticationError)
def auth_unavailable(request, exc):
    exc.code = 1001
    exc.message = "로그인이 필요한 서비스에요."
    exc.status_code = 401
    return ex.error_response(request, exc, api)


# 유효성검사 예외처리
@api.exception_handler(ValidationError)
def exception_handelr(request, exc):
    exc.code = 1003
    exc.message = "유효성 검사에서 문제가 발생했어요."
    exc.status_code = 422
    return ex.error_response(request, exc, api)


# 기타 예외처리
@api.exception_handler(Exception)
def exception_handelr(request, exc):
    return ex.error_response(request, exc, api)


api.add_router("/auth", auth_router)
api.add_router("/user", user_router)
api.add_router("/student/list", student_list_router)
# api.add_router("/student", student_router)
api.add_router("/school", school_router)
api.add_router("/column", column_router)
