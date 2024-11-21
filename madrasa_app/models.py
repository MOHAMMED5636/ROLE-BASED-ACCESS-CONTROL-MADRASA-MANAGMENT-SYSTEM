from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Claass_no(models.Model):   
    class_no= models.CharField(max_length=100,null=True, blank=True)

class User(AbstractUser):
    is_admin = models.BooleanField(default=False, verbose_name="Is admin")
    is_student = models.BooleanField(default=False, verbose_name="Is Student")
    is_teacher = models.BooleanField(default=False, verbose_name="Is Teacher")
    is_parents = models.BooleanField(default=False, verbose_name="Is Parent")
    name = models.CharField(max_length=100,null=True, blank=True)
    mobile = models.CharField(max_length=15,null=True, blank=True)
    place = models.CharField(max_length=200,null=True, blank=True)
    email = models.EmailField(max_length=20,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    roll = models.CharField(max_length=100,null=True, blank=True)
    subject = models.CharField(max_length=100,null=True, blank=True)
    Qualification = models.CharField(max_length=100,null=True, blank=True)
    photo = models.ImageField(upload_to='profile/',null=True, blank=True)
    class_rooom = models.ForeignKey(Claass_no, on_delete=models.CASCADE, related_name='class_room', verbose_name="class_room",null=True, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return  url

class Parent(models.Model):   
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='studet_rele', verbose_name="studet_rele")
    parent= models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_rele', verbose_name="parent_rele")

class Subject(models.Model):   
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin', verbose_name="admin")
    name= models.CharField(max_length=100,null=True, blank=True)

class Assign_Subject(models.Model):   
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assign_admin', verbose_name="Assigning Admin",null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assign_teacher', verbose_name="Assigned Teacher",null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assign_subject', verbose_name="Assigned Subject",null=True, blank=True)
    class_no = models.CharField(max_length=100, null=True, blank=True, verbose_name="Class Number")

class Leave(models.Model):   
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_leave', verbose_name="admin_leave",null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_leave', verbose_name="teacher_leave",null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_leave', verbose_name="student_leave",null=True, blank=True)
    leave= models.CharField(max_length=200,null=True, blank=True)
    date=models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False,null=True, blank=True)

class Mark(models.Model):   
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_result', verbose_name="teacher_result",null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_result', verbose_name="student_result",null=True, blank=True)
    date=models.DateField(auto_now_add=True,null=True, blank=True)
    Exm_name= models.CharField(max_length=200,null=True, blank=True)
    result = models.ImageField(upload_to='result/',null=True, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.result.url
        except:
            url = ''
        return  url
    
class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_attendance')
    date = models.DateField(null=True, blank=True)
    present = models.BooleanField(default=False,null=True, blank=True)

class Notification(models.Model):   
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_notification', verbose_name="admin_notification",null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_notification',null=True, blank=True)
    notification=models.CharField(max_length=200,null=True, blank=True)
    date=models.DateField(auto_now_add=True,null=True, blank=True)
    to_see = models.BooleanField(default=False,null=True, blank=True)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Send_Notifiction(models.Model):
    sender = models.ForeignKey(User, related_name='sender_notifica', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver_notifica', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
