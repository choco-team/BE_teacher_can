def error_response(request, exc, api):
    data = {
        "path": request.path,
        "method": request.method,
        "path_params": (
            request.resolver_match.kwargs if request.resolver_match.kwargs else None
        ),
        "query_params": (
            request.environ["QUERY_STRING"] if request.environ["QUERY_STRING"] else None
        ),
        "body": request.body.decode() if request.body.decode() else None,
        "detail": None,
    }
    try:
        data["detail"] = exc.errors[0]
    except:
        data["detail"] = f"{exc.__str__()} {str(exc.__context__)}"

    return api.create_response(
        request,
        {
            "success": False,
            "code": exc.code if hasattr(exc, "code") else 1000,
            "message": (
                exc.message
                if hasattr(exc, "message")
                else "서버에서 에러가 발생했어요."
            ),
            "data": data,
        },
        status=exc.status_code if hasattr(exc, "status_code") else 500,
    )


class APIException(Exception):
    def __init__(
        self, code: int = 1000, message: str = "서버 에러", status_code: int = 500
    ):
        self.code = code
        self.message = message
        self.status_code = status_code


# Auth
invalid_token = APIException(1002, "유효하지 않은 토큰이에요.", 401)
email_already_exist = APIException(1102, "이메일이 이미 존재해요.", 409)

# 공통
server_error = APIException()
not_authenticated = APIException(1001, "로그인이 필요한 서비스예요.", 403)
invalid_token = APIException(1002, "유효하지 않은 토큰이에요.", 403)
not_access_permission = APIException(1003, "접근 권한이 없는 id에요.", 403)

# Auth
email_already_exist = APIException(1102, "이메일이 이미 존재해요.", 409)
password_invalid = APIException(
    1103, "비밀번호는 8자 보다 적거나, 너무 일반적인 단어는 안 돼요.", 422
)
not_found_user = APIException(1104, "이메일을 다시 확인해주세요.", 404)
password_not_match = APIException(1105, "비밀번호를 다시 확인해주세요.", 401)

# School
nice_api_error = APIException(
    1301, "관련된 정보를 불러오는 중에 에러가 발생했어요.", 503
)
not_found_school = APIException(1302, "해당하는 학교 정보가 존재하지 않아요.", 404)
too_large_entity = APIException(
    1303, "데이터 요청은 한번에 1,000건을 넘을 수 없어요.", 400
)
not_regist_school = APIException(
    1304, "등록된 학교 정보가 없어요. 먼저 학교를 등록해주세요.", 404
)

# Student
not_found_student = APIException(1403, "해당하는 학생이 존재하지 않아요.", 404)

# StudentList
not_found_student_list = APIException(1401, "요청하신 명렬표가 존재하지 않아요.", 404)

# Column
not_found_column = APIException(1501, "요청하신 column이 존재하지 않아요.", 404)

# Row
not_found_row = APIException(1601, "요청하신 row가 존재하지 않아요.", 404)

# 유효성 검사
request_default_error = APIException(1003, "유효성 검사에서 문제가 발생했어요.", 400)
