# Generated by Django 4.2.4 on 2023-11-28 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_student_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=20)),
                ('value', models.TextField(blank=True, null=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.student')),
                ('student_list', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.studentlist')),
            ],
        ),
    ]
