from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session

# import controller classes
from .ctl.UserCtl import UserCtl
from .ctl.CollegeCtl import CollegeCtl
from .ctl.LoginCtl import LoginCtl
from .ctl.WelcomeCtl import WelcomeCtl
from .ctl.RoleCtl import RoleCtl
from .ctl.RoleListCtl import RoleListCtl
from .ctl.FacultyCtl import FacultyCtl
from .ctl.FacultyListCtl import FacultyListCtl
from .ctl.CourseCtl import CourseCtl
from .ctl.StudentCtl import StudentCtl
from .ctl.MarksheetCtl import MarksheetCtl
from .ctl.SubjectCtl import SubjectCtl
from .ctl.SubjectListCtl import SubjectListCtl
from .ctl.TimeTableCtl import TimeTableCtl
from .ctl.TimeTableListCtl import TimeTableListCtl
from .ctl.UserListCtl import UserListCtl
from .ctl.UserCtl import UserCtl
from .ctl.CollegeListCtl import CollegeListCtl
from .ctl.CourseListCtl import CourseListCtl
from .ctl.MarksheetListCtl import MarksheetListCtl
from .ctl.StudentListCtl import StudentListCtl
from .ctl.RegistrationCtl import RegistrationCtl
from .ctl.ForgetPasswordCtl import ForgetPasswordCtl
from .ctl.ChangePasswordCtl import ChangePasswordCtl
from .ctl.LogoutCtl import LogoutCtl
from .ctl.IndexCtl import IndexCtl
from .ctl.MyProfileCtl import MyProfileCtl
from .ctl.HomeCtl import HomeCtl





'''
Calls respective controller with id
'''


@csrf_exempt
def actionId(request, page="", operation="", id=0):
    info(request, page, id)

    if request.session.get('user') is not None and page != "":
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})
    elif page == "Registration":
        ctlName = "Registration" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})
    elif (page == "Home"):
        ctlName = "Home" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})

    elif (page == "ForgetPassword"):
        ctlName = "ForgetPassword" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})

    elif (page == "Login"):
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})

    else:
        res = redirect("/ORS/Login")

    return res


@csrf_exempt
def auth(request, page="", operation="", id=0):
    print("Auth-->", info(request, page, id))
    if page == "Logout":
        Session.objects.all().delete()
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id, "operation": operation})

    return res


def index(request):
    res = render(request, 'ors/project.html')
    return res



































def info(request, page, action):
    print("REQ Method: ", request.method)
    print("Page: ", page)
    print("Action: ", action)
    print("Base Path: ", __file__)