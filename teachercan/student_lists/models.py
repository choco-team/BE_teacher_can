from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import config.exceptions as ex


class CustomStudentListManager(models.Manager):
    use_for_related_fields = True

    def get_student_list(self, id, user, **kwargs):
        try:
            student_list = self.get(id=id, user=user)
        except ObjectDoesNotExist:
            raise ex.not_found_student_list
        return student_list

    def create_student_list(self, payload, user, **kwarg):
        new_student_list = StudentList(
            name=payload.name,
            description=payload.description,
            has_allergy=False,
            is_main=not user.studentLists.count(),
            user=user,
            total_student_num=len(payload.students),
        )
        new_student_list.save()

        return new_student_list

    def make_recent_student_list_main(self, user, **kwargs):
        try:
            recent_student_list = self.filter(user=user, is_main=False).order_by(
                "-updated_at"
            )[0]
        except ObjectDoesNotExist:
            raise ex.not_found_student_list
        recent_student_list.is_main = True
        recent_student_list.save()

    def update_main_student_list(self, student_list, payload, user, **kwargs):
        # is_main == false 를 true로 바꿀 때
        if not student_list.is_main and payload.is_main:
            try:
                main_student_list = self.get(user=user, is_main=True)
            except ObjectDoesNotExist:
                raise ex.not_found_student_list
            main_student_list.is_main = False
            main_student_list.save()
        # is_main == true 를 false로 바꿀 때
        elif student_list.is_main and not payload.is_main:
            self.make_recent_student_list_main(user=user)
        student_list.is_main = payload.is_main
        student_list.save()

    def update_student_list(self, student_list, payload, user, **kwargs):
        student_list.name = payload.name
        student_list.description = payload.description
        self.update_main_student_list(
            student_list=student_list, payload=payload, user=user
        )
        student_list.has_allergy = student_list.has_allergy
        student_list.save()


class StudentList(models.Model):
    objects = CustomStudentListManager()
    name = models.CharField(max_length=15)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    has_allergy = models.BooleanField(default=False)
    description = models.CharField(null=True, max_length=200)
    total_student_num = models.IntegerField()

    user = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, related_name="studentLists"
    )

    class Meta:
        db_table = "student_list"
