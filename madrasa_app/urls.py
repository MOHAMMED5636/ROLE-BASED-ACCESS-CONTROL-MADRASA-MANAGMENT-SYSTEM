from django.urls import path
from . import views
urlpatterns = [
    path('home', views.index, name='index'),

    path('Logout', views.Logout, name='Logout'),

    path('', views.home, name='home'),
    
    path('charity', views.charity, name='charity'),
    path('payment', views.payment, name='payment'),

    ####################admin panel 
    path('admin_home', views.admin_home, name='admin_home'),

    path('admin_register', views.admin_register, name='admin_register'),
    path('admin_login', views.admin_login, name='admin_login'),
    
    path('view_adm_profile/<int:pk>/', views.view_adm_profile, name='view_adm_profile'),
    path('update_adm_profile/<int:pk>/', views.update_adm_profile, name='update_adm_profile'),
    
    path('add_subject', views.add_subject, name='add_subject'),
    path('view_subject', views.view_subject, name='view_subject'),
    path('update_subject/<int:pk>/', views.update_subject, name='update_subject'),
    path('delete_subject/<int:pk>/', views.delete_subject, name='delete_subject'),

    path('teacher_register', views.teacher_register, name='teacher_register'),
    path('view_adm_teacher', views.view_adm_teacher, name='view_adm_teacher'),
    path('update_adm_teacher/<int:pk>/', views.update_adm_teacher, name='update_adm_teacher'),
    path('delete_adm_teacher/<int:pk>/', views.delete_adm_teacher, name='delete_adm_teacher'),
    
    path('add_assign_teacher', views.add_assign_teacher, name='add_assign_teacher'),
    path('view_assign_teacher', views.view_assign_teacher, name='view_assign_teacher'),
    path('update_assign_teacher/<int:pk>/', views.update_assign_teacher, name='update_assign_teacher'),
    path('delete_assign_teacher/<int:pk>/', views.delete_assign_teacher, name='delete_assign_teacher'),
    
    path('student_register', views.student_register, name='student_register'),
    path('view_adm_student', views.view_adm_student, name='view_adm_student'),
    path('update_adm_student/<int:pk>/', views.update_adm_student, name='update_adm_student'),
    path('delete_adm_student/<int:pk>/', views.delete_adm_student, name='delete_adm_student'),

    path('add_class', views.add_class, name='add_class'),
    path('view_class', views.view_class, name='view_class'),
    path('delete_class/<int:pk>/', views.delete_class, name='delete_class'),
    
    path('parent_register', views.parent_register, name='parent_register'),
    path('view_adm_parents', views.view_adm_parents, name='view_adm_parents'),
    path('update_adm_parents/<int:pk>/', views.update_adm_parents, name='update_adm_parents'),
    path('delete_adm_parent/<int:pk>/', views.delete_adm_parent, name='delete_adm_parent'),
    
    path('add_assign_parent', views.add_assign_parent, name='add_assign_parent'),
    path('view_assign_parent', views.view_assign_parent, name='view_assign_parent'),

    path('send_adm_notification', views.send_adm_notification, name='send_adm_notification'),
    path('view_adm_replay_notif', views.view_adm_replay_notif, name='view_adm_replay_notif'),

    path('view_adm_leave', views.view_adm_leave, name='view_adm_leave'),
    path('approve_leave_request', views.approve_leave_request, name='approve_leave_request'),
    path('approve_leave_request/<int:pk>/', views.approve_leave_request, name='approve_leave_request'),
    
    path('view_std_feedback', views.view_std_feedback, name='view_std_feedback'),
    path('feedback_with_student/<int:pk>/', views.feedback_with_student, name='feedback_with_student'),

    ####################teacher panel 
    path('teacher_home', views.teacher_home, name='teacher_home'),

    path('teacher_login', views.teacher_login, name='teacher_login'),
    path('view_teacher_profile/<int:pk>/', views.view_teacher_profile, name='view_teacher_profile'),
    path('update_teacher_profile/<int:pk>/', views.update_teacher_profile, name='update_teacher_profile'),

    path('view_admin', views.view_admin, name='view_admin'),

    path('add_teacher_leave/<int:pk>/', views.add_teacher_leave, name='add_teacher_leave'),
    path('view_teacher_leave', views.view_teacher_leave, name='view_teacher_leave'),

    path('view_teach_student', views.view_teach_student, name='view_teach_student'),
    
    path('add_result/<int:pk>/', views.add_result, name='add_result'),
    path('view_result', views.view_result, name='view_result'),
    path('update_result/<int:pk>/', views.update_result, name='update_result'),
    
    path('take_attendance', views.take_attendance, name='take_attendance'),
    path('view_attendance', views.view_attendance, name='view_attendance'),
    path('search_attendance', views.search_attendance, name='search_attendance'),
    path('update_attendance/<int:pk>/', views.update_attendance, name='update_attendance'),
    
    path('view_teach_notifications', views.view_teach_notifications, name='view_teach_notifications'),
    path('replay_teach_notifications/<int:pk>/', views.replay_teach_notifications, name='replay_teach_notifications'),
    
    path('view_std_leave_request', views.view_std_leave_request, name='view_std_leave_request'),
    path('approve_std_leave_request/<int:pk>/', views.approve_std_leave_request, name='approve_std_leave_request'),
    
    path('view_parents', views.view_parents, name='view_parents'),
    path('notification_with_parent/<int:pk>/', views.notification_with_parent, name='notification_with_parent'),
    
    path('view_teach_student_detials', views.view_teach_student_detials, name='view_teach_student_detials'),

    ####################student panel 

    path('student_home', views.student_home, name='student_home'),

    path('student_login', views.student_login, name='student_login'),
    path('view_std_profile/<int:pk>/', views.view_std_profile, name='view_std_profile'),
    path('update_std_profile/<int:pk>/', views.update_std_profile, name='update_std_profile'),

    path('view_std_attendance', views.view_std_attendance, name='view_std_attendance'),
    path('view_std_result', views.view_std_result, name='view_std_result'),

    path('view_teacher', views.view_teacher, name='view_teacher'),
    path('add_std_leave/<int:pk>/', views.add_std_leave, name='add_std_leave'),
    path('view_std_leave', views.view_std_leave, name='view_std_leave'),

    path('view_std_admin', views.view_std_admin, name='view_std_admin'),
    path('feedback_with_admin/<int:pk>/', views.feedback_with_admin, name='feedback_with_admin'),
    
    path('view_std_notifications', views.view_std_notifications, name='view_std_notifications'),
    
    ####################parent panel  
    path('parent_home', views.parent_home, name='parent_home'),

    path('parent_login', views.parent_login, name='parent_login'),
    path('view_parent_profile/<int:pk>/', views.view_parent_profile, name='view_parent_profile'),
    path('update_parent_profile/<int:pk>/', views.update_parent_profile, name='update_parent_profile'),
    
    path('view_pat_std_profile/<int:pk>/', views.view_pat_std_profile, name='view_pat_std_profile'),

    path('view_std_prt_attendance', views.view_std_prt_attendance, name='view_std_prt_attendance'),
    
    path('view_std_prt_result', views.view_std_prt_result, name='view_std_prt_result'),
    
    path('parent_view_student_teacher', views.parent_view_student_teacher, name='parent_view_student_teacher'),
    path('notification_with_teacher/<int:pk>/', views.notification_with_teacher, name='notification_with_teacher'),

    
]