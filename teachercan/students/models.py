from django.db import models
from django.core.exceptions import ObjectDoesNotExist

import config.exceptions as ex

from teachercan.columns.models import Column


class CustomStudentManager(models.Manager):
    use_for_related_fields = True

    def get_student(self, id, student_list, **kwargs):
        try:
            student = Student.objects.get(id=id, student_list=student_list)
        except ObjectDoesNotExist:
            raise ex.not_found_student
        return student

    def create_student(self, payload, student_list, **kwargs):
        new_student = Student(
            number=payload.number, name=payload.name, gender=payload.gender, student_list=student_list
        )
        new_student.save()
        return new_student

    def update_student(self, payload, student_list, **kwargs):
        student = self.get_student(id=payload.id, student_list=student_list)
        student.number = payload.number
        student.name = payload.name
        student.gender = payload.gender
        if student_list.has_allergy and student.allergy:
            student.allergy.set([Allergy.objects.get(pk=a)
                                for a in student.allergy])
        for rowWithColumnId in payload.columns:
            Row.objects.update_row(payload=rowWithColumnId, student=student)
        student.save()


class CustomRowManager(models.Manager):
    use_for_related_fields = True

    def get_row(self, column, student, **kwargs):
        try:
            row = Row.objects.get(
                column=column, student=student)
        except ObjectDoesNotExist:
            raise ex.not_found_row
        return row
    
    def update_row(self, payload, student):
        column = Column.objects.get(id=payload.id)
        row = self.get_row(column=column, student=student)
        row.value = payload.value
        row.save()



class Allergy(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "allergy"


class StudentAllergyRelation(models.Model):
    student = models.ForeignKey(to="Student", on_delete=models.CASCADE)
    allergy = models.ForeignKey(to="Allergy", on_delete=models.CASCADE)

    class Meta:
        db_table = "student_allergy_set"

    
class Student(models.Model):
    objects = CustomStudentManager()

    name = models.CharField(max_length=10)
    number = models.IntegerField()
    gender = models.CharField(
        max_length=2, choices=[("남", "남"), ("여", "여")], default="남"
    )

    student_list = models.ForeignKey(
        to="student_lists.StudentList",
        on_delete=models.CASCADE,
        db_column="list_id",
        related_name="students",
    )
    allergy = models.ManyToManyField(to="Allergy", through="StudentAllergyRelation")

    class Meta:
        db_table = "student"


class Row(models.Model):
    objects = CustomRowManager()
    value = models.CharField(max_length=100)
    column = models.ForeignKey(
        to="columns.Column", on_delete=models.CASCADE, related_name="rows"
    )
    student = models.ForeignKey(
        to="Student", on_delete=models.CASCADE, related_name="rows"
    )

    class Meta:
        db_table = "student_list_row"
