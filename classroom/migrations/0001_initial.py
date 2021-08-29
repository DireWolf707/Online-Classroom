# Generated by Django 3.2.6 on 2021-08-28 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(blank=True)),
                ('due_date', models.DateTimeField()),
                ('attachment', models.FileField(blank=True, upload_to='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('code', models.CharField(blank=True, max_length=10)),
                ('students', models.ManyToManyField(blank=True, related_name='student_joined', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(blank=True)),
                ('max_marks', models.PositiveIntegerField()),
                ('due_date', models.DateTimeField()),
                ('attachment', models.FileField(blank=True, upload_to='')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classroom_test', to='classroom.classroom')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_test', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submit_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('L', 'Late'), ('D', 'Done')], max_length=1)),
                ('attachment', models.FileField(blank=True, upload_to='')),
                ('grade', models.PositiveIntegerField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_testsubmission', to=settings.AUTH_USER_MODEL)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_submissions', to='classroom.test')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='streams', to='classroom.classroom')),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ('announcement', 'test', 'assignment')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submit_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('L', 'Late'), ('D', 'Done')], max_length=1)),
                ('attachment', models.FileField(blank=True, upload_to='')),
                ('reviewed', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment_submissions', to='classroom.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_assignmentsubmission', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='assignment',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classroom_assignment', to='classroom.classroom'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_assignment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classroom_announcement', to='classroom.classroom')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_announcement', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
