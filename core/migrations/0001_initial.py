# Generated by Django 5.0.1 on 2024-01-17 21:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=300, null=True, verbose_name='Descripción')),
                ('class_quantity', models.PositiveIntegerField(default=0, verbose_name='Cantidad de clases')),
                ('status', models.CharField(choices=[('i', 'En inscripción'), ('p', 'En progreso'), ('f', 'Finalizado')], default='i', max_length=1, verbose_name='Estado')),
                ('teacher', models.ForeignKey(limit_choices_to={'groups__name': 'profesores'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Profesor')),
            ],
            options={
                'verbose_name': 'curso',
                'verbose_name_plural': 'cursos',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present', models.BooleanField(blank=True, default=False, null=True, verbose_name='Presente')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Fecha')),
                ('student', models.ForeignKey(limit_choices_to={'groups__name': 'estudiantes'}, on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to=settings.AUTH_USER_MODEL, verbose_name='Estudiante')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course', verbose_name='Curso')),
            ],
            options={
                'verbose_name': 'Asistencia',
                'verbose_name_plural': 'Asistencias',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark_1', models.PositiveIntegerField(blank=True, null=True, verbose_name='Nota 1')),
                ('mark_2', models.PositiveIntegerField(blank=True, null=True, verbose_name='Nota 2')),
                ('mark_3', models.PositiveIntegerField(blank=True, null=True, verbose_name='Nota 3')),
                ('averange', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='Promedio')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course', verbose_name='Curso')),
                ('student', models.ForeignKey(limit_choices_to={'groups__name': 'estudiantes'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Estudiante')),
            ],
            options={
                'verbose_name': 'Nota',
                'verbose_name_plural': 'Notas',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True, verbose_name='Alumno Regular')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course', verbose_name='Curso')),
                ('student', models.ForeignKey(limit_choices_to={'groups__name': 'estudiantes'}, on_delete=django.db.models.deletion.CASCADE, related_name='students_registration', to=settings.AUTH_USER_MODEL, verbose_name='Estudiante')),
            ],
            options={
                'verbose_name': 'Inscripcion',
                'verbose_name_plural': 'Inscripciones',
            },
        ),
    ]