from teachercan.students.models import Allergy, Row, Student
from teachercan.columns.models import Column
from . import schemas
from .models import StudentList
from ..auths.api import AuthBearer
from ninja import Router
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import config.exceptions as ex

router = Router(auth=AuthBearer(), tags=["StudentList"])

@router.put("/main")
def put_student_list_main(request, payload: schemas.PutMainReq):
    user = request.auth
    student_list = StudentList.objects.get_student_list(id=payload.id, user=user)
    StudentList.objects.update_main_student_list(
        student_list=student_list, 
        payload=payload, 
        user=user
    )
    return {"message": "성공적으로 변경 되었습니다."}

@router.get("", response=schemas.GetStudentList)
def get_student_list(request):
    """
    모든 명렬표 보기(학생은 안보임)\n
    로그인만 하면 별도의 파라미터 없음
    """
    return {"studentList": StudentList.objects.filter(user=request.auth)}


@router.get("/{list_id}", response=schemas.StudentList)
def get_student_list_by_id(request, list_id: int):
    """
    특정 명렬표 보기(학생까지 보임)\n
    파라미터 값은 명렬표 id
    """
    return StudentList.objects.get_student_list(id=list_id, user=request.auth)


@router.post("", response=schemas.StudentList)
def post_student_list(
    request,
    payload: schemas.PostStudentListReq,
):
    """
    {\n
        "name": "3-2반 명렬표",
        "description": "우리반 명렬표",
        "students": [
            {
                "StudentNumber": 1,
                "StudentName": "김철수",
                "gender": "남"
            },
            {
                "StudentNumber": 2,
                "StudentName": "김영희",
                "gender": "여"
            }
        ]
    }
    """
    with transaction.atomic():
        new_student_list = StudentList.objects.create_student_list(payload=payload, user = request.auth)
        for student in payload.students:
            Student.objects.create_student(payload=student, student_list=new_student_list)
    return new_student_list

@router.delete("/{list_id}")
def delete_student_list(request, list_id: int):
    """
    명렬표 지우기(학생까지 다 지워짐)\n
    파라미터 값은 명렬표 id
    """
    user = request.auth
    student_list = StudentList.objects.get_student_list(id=list_id, user=user)
    if student_list.is_main:
        StudentList.objects.make_recent_student_list_main(user=user)
    student_list.delete()
    return "성공적으로 삭제 되었어요."


@router.put("", response=schemas.StudentList)
def put_student_list(request, payload: schemas.PutStudentListReq):
    user = request.auth
    student_list = StudentList.objects.get_student_list(id=payload.id, user=user)
    with transaction.atomic():
        # StudentList update
        StudentList.objects.update_student_list(student_list=student_list, payload=payload, user=user)        
        # Column update
        for column in payload.columns:
            Column.objects.update_column(payload=column, student_list=student_list)
        # Student update
        for student in payload.students:
            Student.objects.update_student(payload=student, student_list=student_list)
    return student_list
