from datetime import datetime
from ninja import Schema, Field
from enum import Enum


class Gender(str, Enum):
    남 = "남"
    여 = "여"


class ColumnBase(Schema):
    field: str = Field(...)


class Column(ColumnBase):
    id: int = Field(...)


class Row(Schema):
    id: int = Field(...)
    value: str | None = Field(None)


class BaseStudent(Schema):
    studentNumber: int = Field(..., alias="number")
    studentName: str = Field(..., alias="name")
    gender: Gender = Field(...)
    allergy: list[int] | None = Field(None)


class Student(BaseStudent):
    id: int = Field(...)
    rows: list[Row] = Field([])


class StudentCreate(Schema):
    number: int = Field(..., alias="studentNumber")
    name: str = Field(..., alias="studentName")
    gender: Gender = Field(...)


class StudentUpdate(Schema):
    id: int = Field(...)
    number: int = Field(..., alias="studentNumber")
    name: str = Field(..., alias="studentName")
    gender: Gender = Field(...)
    allergy: list[int] | None = Field(None)
    columns: list[Row] = Field([])


class BaseStudentList(Schema):
    id: int = Field(...)
    name: str = Field(...)
    isMain: bool = Field(..., alias="is_main")
    hasAllergy: bool = Field(False, alias="has_allergy")
    createdAt: datetime = Field(..., alias="created_at")
    updatedAt: datetime = Field(..., alias="updated_at")
    totalStudentNum: int | None = Field(..., alias="total_student_num")


class StudentList(BaseStudentList):
    columns: list[Column]
    students: list[Student]


class GetStudentList(Schema):
    studentList: list[BaseStudentList]


class PostStudentListReq(Schema):
    name: str
    description: str
    students: list[StudentCreate]


class PutMainReq(Schema):
    id: int
    is_main: bool = Field(..., alias="isMain")


class PutStudentListReq(Schema):
    id: int
    name: str
    description: str
    is_main: bool | None = Field(False, alias="isMain")
    has_allergy: bool = Field(False, alias="hasAllergy")
    columns: list[Column]
    students: list[StudentUpdate]
