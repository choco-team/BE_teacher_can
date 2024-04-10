from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import config.exceptions as ex

class CustomColumnManager(models.Manager):
    use_for_related_fields = True

    def get_column(self, id, student_list, **kwargs):
        try:
            column = self.get(id=id, student_list=student_list)
        except ObjectDoesNotExist:
            raise ex.not_found_column
        return column
    
    def update_column(self, payload, student_list, **kwargs):
        column = self.get_column(id=payload.id, student_list=student_list)
        column.field = payload.field
        column.save()


class Column(models.Model):
    objects = CustomColumnManager()


    field = models.CharField(max_length=20)
    student_list = models.ForeignKey(
        to="student_lists.StudentList", on_delete=models.CASCADE, null=True, related_name='columns'
    )

    class Meta:
        db_table = "student_list_column"