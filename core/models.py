from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
 
class Course (models.Model):
    STATUS_CHOICES = (
        ('i', 'En inscripción'),
        ('p', 'En progreso'),
        ('f', 'Finalizado')
    )
    
    name = models.CharField(max_length=90, verbose_name='Nombre')
    description = models.CharField(max_length=300, blank=True, null=True, verbose_name='Descripción')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'profesores'},verbose_name='Profesor')
    class_quantity = models.PositiveIntegerField(default=0, verbose_name='Cantidad de clases')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='i', verbose_name='Estado')
        
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'

class Registration (models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students_registration', limit_choices_to={'groups__name': 'estudiantes'},verbose_name='Estudiante')
    enabled = models.BooleanField(default=True, verbose_name='Alumno Regular')
    
    def __str__(self):
        return f'{self.student.username} - {self.course.name}'
    
    class Meta:
        verbose_name = 'Inscripcion'
        verbose_name_plural = 'Inscripciones'
        
class Attendance (models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances', limit_choices_to={'groups__name': 'estudiantes'}, verbose_name='Estudiante')
    date = models.DateField(null=True, blank=True, verbose_name='Fecha')
    present = models.BooleanField(default=False, blank=True, null=True, verbose_name='Presente')
          
    def __str__(self):
        return f'Asistencia {self.id}' 
    
    # Logica para generar el estado del alumno regular / irregular (enabled)
    # total de clases => class_quantity del modelo Course
    # total de inasistencias => attendance -> present = False
    # porcentaje de inasistencias => (total de inasistencias / total de clases) * 100
    
    def update_registration_enabled_status (self):
        course_instance = Course.objects.get(id=self.course.id)
        total_classes = course_instance.class_quantity
        total_absences = Attendance.objects.filter(student=self.student, course=self.course, present=False).count()
        absences_percent = (total_absences / total_classes) * 100
        
        registration = Registration.objects.get(course=self.course, student=self.student)
        
        if absences_percent > 20:
            registration.enabled = False
        else:
            registration.enabled = True
        
        registration.save()
    
    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        
class Mark (models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'estudiantes'}, verbose_name='Estudiante')
    mark_1 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 1')
    mark_2 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 2')
    mark_3 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nota 3')
    average = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='Promedio')
    
    def __str__(self):
        return str(self.course)
    
    # Calcular el promedio de las notas
    def calculate_average (self):
        marks = [self.mark_1, self.mark_2, self.mark_3]
        valid_marks = [mark for mark in marks if mark is not None]
        if valid_marks:
            return sum(valid_marks) / len (valid_marks)
        return None
    
    def save (self, *args, **kwargs):
        if self.mark_1 or self.mark_2 or self.mark_3:
            self.average = self.calculate_average()
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        
@receiver(post_save, sender=Attendance)
@receiver(post_delete, sender=Attendance)
def update_registration_enabled_status(sender, instance, **kwargs):
    instance.update_registration_enabled_status()