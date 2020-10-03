# Generated by Django 3.1.1 on 2020-09-27 14:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ituscheduler.apps.api.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('lecture_count', models.PositiveSmallIntegerField(default=1)),
                ('crn', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('catalogue', models.URLField(blank=True, null=True)),
                ('code', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=250)),
                ('instructor', models.CharField(max_length=500)),
                ('capacity', models.PositiveSmallIntegerField()),
                ('enrolled', models.PositiveSmallIntegerField(default=0)),
                ('reservation', models.CharField(max_length=100)),
                ('class_restriction', models.CharField(max_length=110)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['code'],
                'get_latest_by': 'code',
            },
        ),
        migrations.CreateModel(
            name='MajorCode',
            fields=[
                ('refreshed', models.DateTimeField(default=django.utils.timezone.now)),
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'ordering': ['code'],
                'get_latest_by': 'code',
            },
        ),
        migrations.CreateModel(
            name='MajorRestriction',
            fields=[
                ('major', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prerequisite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=30, null=True)),
                ('min_grade', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'get_latest_by': 'code',
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('name', models.CharField(choices=[('SU21', '2020-2021 Summer'), ('S21', '2020-2021 Spring'), ('F20', '2020-2021 Fall'), ('SU20', '2019-2020 Summer'), ('S20', '2019-2020 Spring'), ('F19', '2019-2020 Fall'), ('SU19', '2018-2019 Summer'), ('S19', '2018-2019 Spring'), ('F18', '2018-2019 Fall'), ('SU18', '2017-2018 Summer'), ('S18', '2017-2018 Spring'), ('F17', '2017-2018 Fall'), ('S17', '2016-2017 Spring')], default='F20', max_length=4, primary_key=True, serialize=False, unique=True)),
            ],
            managers=[
                ('objects', ituscheduler.apps.api.models.SemesterManager()),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(max_length=65)),
                ('day', models.CharField(max_length=60)),
                ('time_start', models.IntegerField()),
                ('time_finish', models.IntegerField()),
                ('room', models.CharField(max_length=55)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.course')),
            ],
            options={
                'ordering': ['course'],
                'get_latest_by': 'course',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='major_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.majorcode'),
        ),
        migrations.AddField(
            model_name='course',
            name='major_restriction',
            field=models.ManyToManyField(to='api.MajorRestriction'),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.ManyToManyField(to='api.Prerequisite'),
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(default='F20', on_delete=django.db.models.deletion.CASCADE, to='api.semester'),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('semester', 'crn')},
        ),
    ]
