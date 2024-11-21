from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import razorpay
from django.conf import settings
razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
# Create your views here.

def index(request):
    return render(request,'index.html')


def home(request):
    return render(request,'home.html')
################  logout ######################

def Logout(request):  
    logout(request)
    return redirect('home')

############################admin panel ###################################
############################################

######admin home
def admin_home(request):
        # Count total number of students
    total_students = User.objects.filter(is_student=True).count()

    # Count total number of teachers
    total_teachers = User.objects.filter(is_teacher=True).count()

    # Count total number of parents
    total_parents = Parent.objects.count() 

    total_class = Claass_no.objects.count() 
    context={
        'total_students':total_students,
        'total_teachers':total_teachers,
        'total_parents':total_parents,
        'total_class':total_class
    }
    return render(request,'admin/index.html',context)


#####admin register

def admin_register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw1 = request.POST.get("password")
        passw2= request.POST.get("password1")
        name= request.POST.get("name")
        email= request.POST.get("email")
        mobile= request.POST.get("phone")
        image=request.FILES.get('img')
        if passw1 ==passw2:
            if User.objects.filter(username=uname).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'admin/register.html')
            else:
                user = User.objects.create_user(
                    username=uname,
                    password=passw1,
                    name=name,
                    email=email,
                    mobile=mobile,
                    photo=image,
                    is_admin=True,
                )
                user.save()
                # Add a success message
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('admin_login')
        else:
            messages.error(request, 'password not matching.')
            return redirect('admin_register')
        
    else:
        return render(request, "admin/register.html")
    
#####admin login
    
def admin_login(request):  
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_admin:
            login(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, "admin/login.html")

##########view profile 

def view_adm_profile(request,pk):
    view=User.objects.get(pk=pk,is_admin=True)
    context={
        'view':view
    }
    return render(request,'admin/view_profile.html',context)

##########update profile 
def update_adm_profile(request,pk):
    update=User.objects.get(pk=pk,is_admin=True)
    if request.method == 'POST':
        if 'img' in request.FILES:
            if len(update.photo) > 0:
                os.remove(update.photo.path)
            update.photo = request.FILES['img']
        update.name=request.POST.get('name')
        update.mobile=request.POST.get('mobile')
        update.place=request.POST.get('place')  
        update.email=request.POST.get('email') 
        update.save()
        messages.success(request,"Update successfully")
        return redirect('view_adm_profile',pk=update.pk)
    context={
        'update':update
    }
    return render(request,'admin/update_profile.html',context)


#########add subject 

def add_subject(request):
    if request.method == 'POST':      
        name=request.POST.get('name')
        admin=request.user
        sub=Subject.objects.create(
            name=name,
            admin=admin
        )
        sub.save()
        messages.success(request,"Subject successfully Added")
        return redirect('add_subject')
    return render(request,'admin/add_subject.html')

######### view subject

def view_subject(request):
    view=Subject.objects.all()
    context={
        'view':view
    }
    return render(request,'admin/view_subject.html',context)

#########update subject
def update_subject(request,pk):
    update=Subject.objects.get(pk=pk)
    if request.method =='POST':
        update.name=request.POST.get('name')
        update.save()
        messages.success(request,"Updation successfully Completed")
        return redirect('view_subject')
    context={
        'update':update
    }
    return render(request,'admin/update_subject.html',context)

########### delete subject
def delete_subject(request,pk):
    view=Subject.objects.get(pk=pk)
    view.delete()
    return redirect('view_subject')

########  add teacher 

def teacher_register(request):
    class_room=Claass_no.objects.all()
    if request.method == "POST":
        uname = request.POST.get("username")
        passw1 = request.POST.get("password")
        name= request.POST.get("name")
        email= request.POST.get("email")
        place= request.POST.get("place")
        address= request.POST.get("address")
        qualification= request.POST.get("qualification")
        mobile= request.POST.get("phone")
        image=request.FILES.get('img')
        class_room= request.POST.get("Class")
        class_instance= Claass_no.objects.get(pk=class_room)

        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'admin/add_teacher.html')
        else:
            user = User.objects.create_user(
                username=uname,
                password=passw1,
                name=name,
                email=email,
                place=place,
                address=address,
                Qualification=qualification,
                mobile=mobile,
                photo=image,
                class_rooom=class_instance,
                is_teacher=True,
            )
            user.save()
                # Add a success message
            messages.success(request, 'Teacher Registration successful.')
            return redirect('view_adm_teacher')
    context={
        'class_room':class_room
    }
    return render(request, "admin/add_teacher.html",context)

####### view teacher

def view_adm_teacher(request):
    view= User.objects.filter(is_teacher=True)
    context={
        'view':view
    }
    return render(request,'admin/view_teacher.html',context)

########## update teacher

def update_adm_teacher(request,pk):
    update=User.objects.get(pk=pk)
    class_room=Claass_no.objects.all()
    if request.method == 'POST':
        if 'img' in request.FILES:
            if len(update.photo) > 0:
                os.remove(update.photo.path)
            update.photo = request.FILES['img']
        update.name=request.POST.get('name')
        update.username = request.POST.get("username")
        update.mobile=request.POST.get('phone')
        update.place=request.POST.get('place')  
        update.email=request.POST.get('email') 
        update.address= request.POST.get("address")
        update.Qualification= request.POST.get("qualification")
        class_room= request.POST.get("Class")
        class_instance= Claass_no.objects.get(pk=class_room)
        update.class_rooom=class_instance
        update.save()
        messages.success(request,"Updation successfully")
        return redirect('view_adm_teacher')
    context={
        'update':update,
        'class_room':class_room
    }
    return render(request,'admin/update_teacher.html',context)
    
####### delete teacher 

def delete_adm_teacher(request,pk):
    view=User.objects.get(pk=pk)
    view.delete()
    return redirect('view_adm_teacher')

#### add assign to subject

def add_assign_teacher(request):
    teacher=User.objects.filter(is_teacher=True)
    subject=Subject.objects.all()
    if request.method == "POST":
        teacher = request.POST.get("teacher")
        teacher_instance=User.objects.get(pk=teacher)
        subject = request.POST.get("subject")
        subject_instance=Subject.objects.get(pk=subject)
        class_no= request.POST.get("class")
    

        assign = Assign_Subject.objects.create(
            
            admin=request.user,
            teacher=teacher_instance,
            subject=subject_instance,
            class_no=class_no,
            
        )
        assign.save()
    #             # Add a success message
        messages.success(request, 'Subject Assign successfully Comleted.')
        return redirect('view_assign_teacher')
    context={
        'teacher':teacher,
        'subject':subject
    }
    return render(request, "admin/assign_sub.html",context)

####### view assign to subject

def view_assign_teacher(request):
    admin=request.user
    view= Assign_Subject.objects.filter(admin=admin)
    context={
        'view':view
    }
    return render(request,'admin/view_assign_sub.html',context)

########## update assign to subject

def update_assign_teacher(request,pk):
    teacher=User.objects.filter(is_teacher=True)
    subject=Subject.objects.all()
    update=Assign_Subject.objects.get(pk=pk)
    if request.method == 'POST': 
        teacher=request.POST.get('teacher')
        teacher_instance=User.objects.get(pk=teacher)
        update.teacher=teacher_instance
        subject = request.POST.get("subject")
        subject_instance=Subject.objects.get(pk=subject)
        update.subject=subject_instance
        update.save()
        messages.success(request,"Updatation successfully Completed")
        return redirect('view_assign_teacher')
    context={
        'update':update,
        'teacher':teacher,
        'subject':subject
    }
    return render(request,'admin/update_assign_sub.html',context)
    

####### delete assign to subject 

def delete_assign_teacher(request,pk):
    view=Assign_Subject.objects.get(pk=pk)
    view.delete()
    return redirect('view_assign_teacher')

########  add student 

def student_register(request):
    class_room=Claass_no.objects.all()
    if request.method == "POST":
        register = request.POST.get("Reg")
        uname = request.POST.get("username")
        passw1 = request.POST.get("password")
        name= request.POST.get("name")
        email= request.POST.get("email")
        place= request.POST.get("place")
        address= request.POST.get("address")   
        mobile= request.POST.get("phone")
        class_room= request.POST.get("Class")
        class_instance= Claass_no.objects.get(pk=class_room)
        image=request.FILES.get('img')

        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'admin/add_student.html')
        else:
            user = User.objects.create_user(
                roll=register,
                username=uname,
                password=passw1,
                name=name,
                email=email,
                place=place,
                address=address,          
                mobile=mobile,
                photo=image,
                class_rooom=class_instance,
                is_student=True,
            )
            user.save()
                # Add a success message
            messages.success(request, 'Student Registration successfully.')
            return redirect('view_adm_student')
    context={
        'class_room':class_room
    }
    return render(request, "admin/add_student.html",context)

####### view student

def view_adm_student(request):
    view= User.objects.filter(is_student=True)
    context={
        'view':view
    }
    return render(request,'admin/view_student.html',context)

########## update teacher

def update_adm_student(request,pk):
    update=User.objects.get(pk=pk)
    class_room=Claass_no.objects.all()
    if request.method == 'POST':
        if 'img' in request.FILES:
            if len(update.photo) > 0:
                os.remove(update.photo.path)
            update.photo = request.FILES['img']
        update.roll=request.POST.get('register')
        class_room= request.POST.get("Class")
        class_instance= Claass_no.objects.get(pk=class_room)
        update.class_rooom=class_instance
        update.name=request.POST.get('name')
        update.username = request.POST.get("username")
        update.mobile=request.POST.get('phone')
        update.place=request.POST.get('place')  
        update.email=request.POST.get('email') 
        update.address= request.POST.get("address")
        update.save()
        messages.success(request,"Updation successfully")
        return redirect('view_adm_student')
    context={
        'update':update,
        'class_room':class_room
    }
    return render(request,'admin/update_student.html',context)

####### delete student 

def delete_adm_student(request,pk):
    view=User.objects.get(pk=pk)
    view.delete()
    return redirect('view_adm_student')

#########add class 

def add_class(request):
    if request.method == 'POST':      
        class_no=request.POST.get('class')
        cls=Claass_no.objects.create(
            class_no=class_no,
          
        )
        cls.save()
        messages.success(request,"successfully Added Class")
        return redirect('add_class')
    return render(request,'admin/add_class.html')

##########view class 

def view_class(request):
    view=Claass_no.objects.all()
    context={
        'view':view
    }
    return render(request,'admin/view_class.html',context)
####### delete class 

def delete_class(request,pk):
    view=Claass_no.objects.get(pk=pk)
    view.delete()
    return redirect('view_class')

########  add parent 

def parent_register(request):
    if request.method == "POST":
      
        uname = request.POST.get("username")
        passw1 = request.POST.get("password")
        name= request.POST.get("name")
        place= request.POST.get("place")
        address= request.POST.get("address")   
        mobile= request.POST.get("phone")
        image=request.FILES.get('img')

        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'admin/add_parents.html')
        else:
            user = User.objects.create_user(
            
                username=uname,
                password=passw1,
                name=name,
                place=place,
                address=address,          
                mobile=mobile,
                photo=image,
                is_parents=True,
            )
            user.save()
                # Add a success message
            messages.success(request, 'Parents Registration successfully.')
            return redirect('view_adm_parents')
 
    return render(request, "admin/add_parents.html")

####### view parent

def view_adm_parents(request):
    view= User.objects.filter(is_parents=True)
    context={
        'view':view
    }
    return render(request,'admin/view_parent.html',context)

########## update parent

def update_adm_parents(request,pk):
    update=User.objects.get(pk=pk)
    if request.method == 'POST':
        if 'img' in request.FILES:
            if len(update.photo) > 0:
                os.remove(update.photo.path)
            update.photo = request.FILES['img']
        update.name=request.POST.get('name')
        update.username = request.POST.get("username")
        update.mobile=request.POST.get('phone')
        update.place=request.POST.get('place')  
      
        update.address= request.POST.get("address")
  
        
        update.save()
        messages.success(request,"Updation successfully")
        return redirect('view_adm_parents')
    context={
        'update':update,
    }
    return render(request,'admin/update_parent.html',context)

####### delete parent 

def delete_adm_parent(request,pk):
    view=User.objects.get(pk=pk)
    view.delete()
    return redirect('view_adm_parents')

#### add assign to parent

def add_assign_parent(request):
    student=User.objects.filter(is_student=True)
    parent=User.objects.filter(is_parents=True)
    if request.method == "POST":
        paren = request.POST.get("parent")
        parent_instance=User.objects.get(pk=paren)
        studen = request.POST.get("student")
        student_instance=User.objects.get(pk=studen)

        assign = Parent.objects.create(
            student=student_instance,
            parent=parent_instance,
            
        )
        assign.save()
    #             # Add a success message
        messages.success(request, 'Parent Assign successfully Comleted.')
        return redirect('add_assign_parent')
    context={
        'student':student,
        'parent':parent
    }
    return render(request, "admin/assign_parent.html",context)

####### view assign to parent

def view_assign_parent(request):
    view= Parent.objects.all()
    context={
        'view':view
    }
    return render(request,'admin/view_assign_parent.html',context)

#### send notification

def send_adm_notification(request):
    admin=request.user
    if request.method == "POST":
        message = request.POST.get("message")
        assign = Notification.objects.create(
            admin=admin,
            notification=message,           
        )
        assign.save()
        messages.success(request, 'successfully Send Notification.')
        return redirect('send_adm_notification')   
    return render(request, "admin/add_notific.html")

####### view Replay notification

def view_adm_replay_notif(request):
    view=Notification.objects.filter(to_see=True)
    context={
        'view':view
    }
    return render(request,'admin/view_replay_notif.html',context)


######### view Leave 

def view_adm_leave(request):
    admin=request.user
    view=Leave.objects.filter(admin=admin)
    context={
        'view':view
    }
    return render(request,'admin/view_leave.html',context)

###########approve request #############

def approve_leave_request(request,pk):
    requ=Leave.objects.get(pk=pk)
    if requ.admin == request.user:
        requ.status =True
        requ.save()
    return redirect('view_adm_leave')

######### view student 

def view_std_feedback(request):
    view=User.objects.filter(is_student=True)
    context={
        'view':view
    }
    return render(request,'admin/student.html',context)
##########feedback with student

def feedback_with_student(request,pk):
    student=User.objects.get(pk=pk)
    admin=request.user
    view_chat=Message.objects.filter(receiver=student, sender=admin) | Message.objects.filter(receiver=admin, sender=student)
    if request.method =='POST':
        message =request.POST.get('content')
        chat=Message.objects.create(
            sender=admin,
            receiver=student,
            content=message
        )
        chat.save()
        return redirect('feedback_with_student',pk=pk)
    context={
       
        'view_chat':view_chat.order_by('timestamp')
    }
    return render(request,'admin/feedback.html',context)

############################teacher panel ###################################
############################################

######teacher home
def teacher_home(request):
    teacher_room=request.user.class_rooom
    view=User.objects.filter(is_student=True,class_rooom=teacher_room)
    context={
        'view':view
    }
    return render(request,'teacher/index.html',context)

#####teacher login
    
def teacher_login(request):  
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_teacher:
            login(request, user)
            return redirect('teacher_home')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, "teacher/login.html")

##########view profile 

def view_teacher_profile(request,pk):
    view=User.objects.get(pk=pk,is_teacher=True)
    context={
        'view':view
    }
    return render(request,'teacher/view_profile.html',context)

##########update profile 
def update_teacher_profile(request,pk):
    update=User.objects.get(pk=pk,is_teacher=True)
    if request.method == 'POST':
        if 'img' in request.FILES:
            if len(update.photo) > 0:
                os.remove(update.photo.path)
            update.photo = request.FILES['img']
        update.username=request.POST.get('username')
        update.name=request.POST.get('name')
        update.mobile=request.POST.get('mobile')
        update.place=request.POST.get('place')  
        update.email=request.POST.get('email') 
        update.Qualification=request.POST.get('Qualification') 
        update.address=request.POST.get('address') 
        update.save()
        messages.success(request,"Update successfully")
        return redirect('view_teacher_profile',pk=update.pk)
    context={
        'update':update
    }
    return render(request,'teacher/update_profile.html',context)

######### view Aadmin

def view_admin(request):
    view=User.objects.filter(is_admin=True)
    context={
        'view':view
    }
    return render(request,'teacher/admin.html',context)

######### view class Students

def view_teach_student(request):
    teacher_room=request.user.class_rooom
    view=User.objects.filter(is_student=True,class_rooom=teacher_room)
    context={
        'view':view
    }
    return render(request,'teacher/students.html',context)

######### view class Students Detals

def view_teach_student_detials(request):
    teacher_room=request.user.class_rooom
    view=User.objects.filter(is_student=True,class_rooom=teacher_room)
    context={
        'view':view
    }
    return render(request,'teacher/view_student.html',context)

#########add Leave 

def add_teacher_leave(request,pk):
    admin=User.objects.get(pk=pk)
    if request.method == 'POST':      
        date=request.POST.get('date')
        leave=request.POST.get('leave')
        teacher=request.user
        leav=Leave.objects.create(
            admin=admin,
            teacher=teacher,
            leave=leave,
            date=date
        )
        leav.save()
        messages.success(request,"successfully Send Your Leave Form")
        return redirect('add_teacher_leave',pk=pk)
    return render(request,'teacher/add_leave.html')

######### view Leave 

def view_teacher_leave(request):
    teacher=request.user
    view=Leave.objects.filter(teacher=teacher,teacher__is_teacher=True,admin__is_admin=True)
    context={
        'view':view
    }
    return render(request,'teacher/view_leave.html',context)

#########add Result 

def add_result(request,pk):
    student=User.objects.get(pk=pk,is_student=True)
    if request.method == 'POST':      
        result=request.FILES.get('img')
        exm_name=request.POST.get('name')
        teacher=request.user
        mark=Mark.objects.create(
            teacher=teacher,
            student=student,
            Exm_name=exm_name,
            result=result
        )
        mark.save()
        messages.success(request,"successfully Added Student Result.")
        return redirect('add_result',pk=pk)
    return render(request,'teacher/add_result.html')

######### view Result 

def view_result(request):
    teacher=request.user
    view=Mark.objects.filter(teacher=teacher)
    context={
        'view':view
    }
    return render(request,'teacher/view_result.html',context)

########## update mark

def update_result(request,pk):
    update=Mark.objects.get(pk=pk)
    if request.method == 'POST':
        if 'img' in request.FILES:
            if len(update.result) > 0:
                os.remove(update.result.path)
            update.result = request.FILES['img']
        update.Exm_name=request.POST.get('name')
        
        update.save()
        messages.success(request,"Updation successfully")
        return redirect('view_result')
    context={
        'update':update,
    }
    return render(request,'teacher/update_mark.html',context)

####### take attendance

def take_attendance(request):
    if request.method == 'POST':
        # Extract the date from the form
        date = request.POST.get('date')
        
        # Retrieve the list of students from the form
        students_present = request.POST.getlist('students')
        
        # Get the teacher's ID
        teacher_id = request.user.id
        
        # Check if attendance for this date already exists
        if Attendance.objects.filter(date=date).exists():
            messages.warning(request, "Attendance for this date already exists.")
            return redirect('take_attendance')
        
        # Iterate over all students in the class
        teacher_room = request.user.class_rooom
        all_students = User.objects.filter(is_student=True, class_rooom=teacher_room)
        
        # Iterate over all students and mark them as present or absent based on form data
        for student in all_students:
            if str(student.id) in students_present:
                present = True
            else:
                present = False
            # Create a new attendance record for the student
            Attendance.objects.create(student=student, teacher_id=teacher_id, date=date, present=present)
        
        # Redirect to a success page or any other page as needed
        messages.success(request, "Attendance successfully completed.")
        return redirect('take_attendance')
    
    else:
        teacher_room = request.user.class_rooom
        view = User.objects.filter(is_student=True, class_rooom=teacher_room)
        context = {'view': view}
        return render(request, 'teacher/take_attendance.html', context)
######### view attendance

def view_attendance(request):
    return render(request,'teacher/attendance.html')

######### search #############

def search_attendance(request):
    query=request.GET.get('search', '')

    view = Attendance.objects.filter(
        Q(date__icontains=query)       
    )
    context={
        'view':view,
    }
    return render(request,'teacher/view_attendance.html',context)

def update_attendance(request, pk):
    if request.method == 'POST':
        # Get the attendance record
        attendance_record = get_object_or_404(Attendance, pk=pk)
        
        # Extract data from the form
        new_attendance_status = request.POST.get('attendance_status')
        
        # Update the attendance record
        if new_attendance_status == 'present':
            attendance_record.present = True
        elif new_attendance_status == 'absent':
            attendance_record.present = False
        
        # Save the updated record
        attendance_record.save()
        
        # Optionally, you can add a success message
        messages.success(request, "Attendance updated successfully.")
        
    # Redirect back to the view attendance page
    return redirect('view_attendance')

########## view notifications

def view_teach_notifications(request):
    view=Notification.objects.filter(to_see=False)
    context={
        'view':view
    }
    return render(request,'teacher/view_notifi.html',context)

########## view notifications

def replay_teach_notifications(request,pk):
    admin=User.objects.get(pk=pk)
    if request.method == "POST":
        message = request.POST.get("message")
        assign = Notification.objects.create(
            admin=admin,
            teacher=request.user,
            notification=message,
            to_see=True           
        )
        assign.save()
        messages.success(request, 'successfully Send Notification.')
        return redirect('view_teach_notifications')  
    return render(request,'teacher/replay_notifi.html')

######### view  student Leave 

def view_std_leave_request(request):
    teacher=request.user
    teacher_room=request.user.class_rooom
    view=Leave.objects.filter(teacher=teacher,student__is_student=True,student__class_rooom=teacher_room)
    context={
        'view':view
    }
    return render(request,'teacher/view_std_leave.html',context)

###########approve request #############

def approve_std_leave_request(request,pk):
    requ=Leave.objects.get(pk=pk)
    if requ.teacher == request.user:
        requ.status =True
        requ.save()
    return redirect('view_std_leave_request')

###########View  Parent #############

def view_parents(request):
    # Get the current user
    current_user = request.user

    # Check if the current user is a teacher
    if current_user.is_teacher:
        # If the user is a teacher, get the students in their class
        students_in_class = User.objects.filter(class_rooom=current_user.class_rooom)

        # Get the parents associated with these students
        parents = Parent.objects.filter(student__in=students_in_class)
    elif current_user.is_parents:
        # If the user is a parent, get the parent-child relationship
        parents = Parent.objects.filter(parent=current_user)
    else:
        # If the user is not a teacher or parent, return an empty queryset
        parents = Parent.objects.none()
    return render(request,'teacher/view_parent.html',{'parents': parents})


########## send notification #########

def notification_with_parent(request,pk):
    parent=User.objects.get(pk=pk)
    teacher=request.user
    view_chat=Message.objects.filter(receiver=parent, sender=teacher) | Message.objects.filter(receiver=teacher, sender=parent)
    if request.method =='POST':
        message =request.POST.get('content')
        chat=Message.objects.create(
            sender=teacher,
            receiver=parent,
            content=message
        )
        chat.save()
        return redirect('notification_with_parent',pk=pk)
    context={
       
        'view_chat':view_chat.order_by('timestamp')
    }
    return render(request,'teacher/notif_to_parent.html',context)


############################Student panel ###################################
############################################

######Student home
def student_home(request):
    student=request.user.class_rooom
    teacher=User.objects.filter(class_rooom=student,is_teacher=True)
    context={
        'teacher':teacher
    }
    return render(request,'student/index.html',context)

#####student login
    
def student_login(request):  
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_student:
            login(request, user)
            return redirect('student_home')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, "student/login.html")

##########view profile 

def view_std_profile(request,pk):
    view=User.objects.get(pk=pk,is_student=True)
    context={
        'view':view
    }
    return render(request,'student/view_profile.html',context)

##########update profile 
def update_std_profile(request,pk):
    update=User.objects.get(pk=pk,is_student=True)
    if request.method == 'POST':
        if 'img' in request.FILES:
            if len(update.photo) > 0:
                os.remove(update.photo.path)
            update.photo = request.FILES['img']
        update.username=request.POST.get('username')
        update.name=request.POST.get('name')
        update.mobile=request.POST.get('mobile')
        update.place=request.POST.get('place')  
        update.email=request.POST.get('email') 
        update.address=request.POST.get('address') 
        update.save()
        messages.success(request,"Update successfully")
        return redirect('update_std_profile',pk=update.pk)
    context={
        'update':update
    }
    return render(request,'student/update_profile.html',context)

######### view attendance

def view_std_attendance(request):
    student=request.user
    view=Attendance.objects.filter(student=student)
    context={
        'view':view
    }
    return render(request,'student/view_attendace.html',context)

######### view result

def view_std_result(request):
    student=request.user
    view=Mark.objects.filter(student=student)
    context={
        'view':view
    }
    return render(request,'student/view_result.html',context)



######## view teacher

def view_teacher(request):
    student=request.user.class_rooom
    teacher=User.objects.filter(class_rooom=student,is_teacher=True)
    context={
        'teacher':teacher
    }
    return render(request,'student/view_teacher.html',context)

#########add Leave 

def add_std_leave(request,pk):
    student=request.user
    teacher=User.objects.get(pk=pk)
    if request.method == 'POST':      
        date=request.POST.get('date')
        leave=request.POST.get('leave')
        leav=Leave.objects.create(
            student=student,
            teacher=teacher,
            leave=leave,
            date=date
        )
        leav.save()
        messages.success(request,"successfully Send Your Leave Form")
        return redirect('add_std_leave',pk=pk)
    return render(request,'student/add_leave.html')

######### view Leave 

def view_std_leave(request):
    student=request.user
    view=Leave.objects.filter(student=student)
    context={
        'view':view
    }
    return render(request,'student/view_leave.html',context)

######### view admin 

def view_std_admin(request):
    view=User.objects.filter(is_admin=True)
    context={
        'view':view
    }
    return render(request,'student/admin.html',context)

##########feedback with admin

def feedback_with_admin(request,pk):
    admin=User.objects.get(pk=pk)
    student=request.user
    view_chat=Message.objects.filter(receiver=admin, sender=student) | Message.objects.filter(receiver=student, sender=admin)
    if request.method =='POST':
        message =request.POST.get('content')
        chat=Message.objects.create(
            sender=student,
            receiver=admin,
            content=message
        )
        chat.save()
        return redirect('feedback_with_admin',pk=pk)
    context={
        'admin':admin,
        'view_chat':view_chat.order_by('timestamp')
    }
    return render(request,'student/feedback.html',context)

########## view notifications

def view_std_notifications(request):
    view=Notification.objects.filter(admin__is_admin=True,to_see=False)
    context={
        'view':view
    }
    return render(request,'student/view_notif.html',context)


############################parent panel ###################################
############################################

######parent home
def parent_home(request):
    parent=request.user
    parent_relation = get_object_or_404(Parent, parent=parent)

    student = parent_relation.student.class_rooom

    teacher = User.objects.filter(class_rooom=student,is_teacher=True)
    context={
        'teacher':teacher
    }
    return render(request,'parent/index.html',context)

#####parent login
    
def parent_login(request):  
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_parents:
            login(request, user)
            return redirect('parent_home')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, "parent/login.html")

##########view profile 

def view_parent_profile(request,pk):
    view=Parent.objects.get(parent=pk)
    context={
        'view':view
    }
    return render(request,'parent/view_profile.html',context)

##########update profile 
def update_parent_profile(request,pk):
    update=Parent.objects.get(parent=pk)
    if request.method == 'POST':
        if 'img' in request.FILES:
            if len(update.parent.photo) > 0:
                os.remove(update.parent.photo.path)
            update.parent.photo = request.FILES['img']
        update.parent.name=request.POST.get('name')
        update.parent.mobile=request.POST.get('mobile')
        update.parent.place=request.POST.get('place')  
        update.parent.address=request.POST.get('address') 
      
        update.parent.save()
        messages.success(request,"Update successfully")
        return redirect('view_parent_profile',pk=update.parent.pk)
    context={
        'update':update
    }
    return render(request,'parent/update_profile.html',context)

##########view profile 

def view_parent_profile(request,pk):
    view=Parent.objects.get(parent=pk)
    context={
        'view':view
    }
    return render(request,'parent/view_profile.html',context)

##########view student profile 

def view_pat_std_profile(request,pk):
    view=Parent.objects.get(parent=pk)
    context={
        'view':view
    }
    return render(request,'parent/student_details.html',context)

######### view attendance

def view_std_prt_attendance(request):
    parent = request.user
    parent_relation = get_object_or_404(Parent, parent=parent)
    
    # Retrieve the student associated with the parent
    student = parent_relation.student
    
    # Retrieve attendance records for the specific student
    attendance_records = Attendance.objects.filter(student=student)
    
    context = {
        'attendance_records': attendance_records,
        'student': student,
    }
    return render(request,'parent/view_attendance.html',context)

######### view result

def view_std_prt_result(request):
    parent = request.user
    parent_relation = get_object_or_404(Parent, parent=parent)
    
    # Retrieve the student associated with the parent
    student = parent_relation.student
    
    # Retrieve attendance records for the specific student
    result = Mark.objects.filter(student=student)
    
    context = {
        'result': result,
        'student': student,
    }
    return render(request,'parent/view_result.html',context)

######## view teacher
def parent_view_student_teacher(request):
    parent=request.user
    parent_relation = get_object_or_404(Parent, parent=parent)

    student = parent_relation.student.class_rooom

    teacher = User.objects.filter(class_rooom=student,is_teacher=True)
    return render(request, 'parent/view_student_teacher.html', {'teacher': teacher})

########## send notification to teacher #########

def notification_with_teacher(request,pk):
    teacher=User.objects.get(pk=pk)
    parent=request.user
    view_chat=Message.objects.filter(receiver=teacher, sender=parent) | Message.objects.filter(receiver=parent, sender=teacher)
    if request.method =='POST':
        message =request.POST.get('content')
        chat=Message.objects.create(
            sender=parent,
            receiver=teacher,
            content=message
        )
        chat.save()
        return redirect('notification_with_teacher',pk=pk)
    context={
       
        'view_chat':view_chat.order_by('timestamp')
    }
    return render(request,'parent/notif_to_teacher.html',context)



#########3# Charity###

def charity(request):
    return render(request,'charity.html')

def payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            try:
                amount = int(amount)
                if amount > 0:
                    currency = 'INR'
                    amount *= 100  # Convert to paisa (1 INR = 100 paisa)
                    
                    # Create a Razorpay order
                    razorpay_order = razorpay_client.order.create(dict(
                        amount=amount,
                        currency=currency,
                        payment_capture='0'  # Payment capture is set to manual
                    ))
                    
                    razorpay_order_id = razorpay_order["id"]
                    callback_url = 'http://127.0.0.1:8000/home'  # Update with your actual callback URL

                    context = {
                        'razorpay_order_id': razorpay_order_id,
                        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
                        'razorpay_amount': amount,
                        'currency': currency,
                        'callback_url': callback_url
                    }
                    return render(request, "payment.html", context)
                else:
                    messages.error(request, "Amount should be greater than 0.")
            except ValueError:
                messages.error(request, "Invalid amount entered.")
        else:
            messages.error(request, "Amount not provided.")
    
    return render(request, "charity.html")
# def payment(request):
    # item = Product.objects.get(id=id)
    # currency = 'INR'
    # amt = item.price
    # product = Cart.objects.filter(product=id, usr=request.user.id).first()
    # product.payment_status = True
    # product.save()
    # amount = amt * 100
    # razorpay_order = razorpay_client.order.create(dict(amount=amount,
    #                     currency=currency,
    #                     payment_capture='0'))
    # razorpay_order_id = razorpay_order["id"]
    # callback_url = 'http://127.0.0.1:8000/index'
    # context = {}
    # context['razorpay_order_id'] = razorpay_order_id
    # context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    # context['razorpay_amount'] = amount
    # context['currency'] = currency
    # context['callback_url'] = callback_url 
    # context['slotid'] = "1"
    # return render(request, "payment.html",context)