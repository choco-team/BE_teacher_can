# Generated by Django 5.0.2 on 2024-03-25 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('columns', '0001_initial'),
        ('student_lists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'allergy',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('number', models.IntegerField()),
                ('gender', models.CharField(choices=[('남', '남'), ('여', '여')], default='남', max_length=2)),
                ('student_list', models.ForeignKey(db_column='list_id', on_delete=django.db.models.deletion.CASCADE, related_name='students', to='student_lists.studentlist')),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='columns.column')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='students.student')),
            ],
            options={
                'db_table': 'student_list_row',
            },
        ),
        migrations.CreateModel(
            name='StudentAllergyRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.allergy')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
            options={
                'db_table': 'student_allergy_set',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='allergy',
            field=models.ManyToManyField(through='students.StudentAllergyRelation', to='students.allergy'),
        ),
    ]
