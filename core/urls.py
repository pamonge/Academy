from django.urls import path
from .views import HomeView, PricingView, RegisterView, ProfileView, CoursesView, CourseCreateView, CourseEditView, CourseDeleteView, CourseEnrollmentView, StudentListMarkView, UpdateMarkView, AttendanceListView, AddAttendanceView, evolution, ProfilePasswordChangeView, AddUserView, CustomLoginView, UserDetailView, superuser_edit, ErrorView 
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Pagina de inicio
    path ('', HomeView.as_view(), name='home'), 
    # Pagina de precios
    path ('pricing/', PricingView.as_view(), name='pricing'),  
    # Pagina de Login y registro
    path ('register/', RegisterView.as_view(), name='register'),
    # Pagina de vista y edición de perfil
    path ('profile/', login_required(ProfileView.as_view()), name='profile'),  
    # Paginas que administran los cursos (CRUD) 
    path ('courses/', CoursesView.as_view(), name='courses'), 
    path ('courses/create/', login_required(CourseCreateView.as_view()), name='course_create'), 
    path ('courses/<int:pk>/edit/', login_required(CourseEditView.as_view()), name='course_edit'),
    path ('course/<int:pk>/delete/', login_required(CourseDeleteView.as_view()), name='course_delete'),
    # Pagina de inscripción de alumnos a cursos
    path ('enroll_course/<int:course_id>/', login_required(CourseEnrollmentView.as_view()), name='enroll_course'),
    path ('error/', login_required(ErrorView.as_view()), name='error'),
    # Pagina de administración de notas
    path ('courses/<int:course_id>/', StudentListMarkView.as_view(), name='student_list_mark'),
    path ('courses/update_mark/<int:mark_id>/', UpdateMarkView.as_view(), name='update_mark'),
    # Paginas de asistencias
    path ('course/<int:course_id>/list_attendance/', login_required(AttendanceListView.as_view()), name='list_attendance'),
    path ('course/<int:course_id>/add_attendance/', login_required(AddAttendanceView.as_view()), name='add_attendance'),
    # Pagina de evolución del esudiante
    path ('evolution/<int:course_id>/<int:student_id>/', login_required(evolution), name='evolution'),
    # Pagina de cambios de contraseña
    path('password_change/', login_required(ProfilePasswordChangeView.as_view()), name='profile_password_change'),
    # Agregar Nuevo Usuario por el Admin
    path('add_user/', login_required(AddUserView.as_view()), name='add_user'),
    # Login Personalizado
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    # perfil de un usuario
    path('user_details/<int:pk>/', UserDetailView.as_view(), name='user_details'),
    # Editar datos del usuario
    path('superuser_edit/<int:user_id>/', login_required(superuser_edit), name='superuser_edit')
]
