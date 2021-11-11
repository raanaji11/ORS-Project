



from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Faculty
from service.forms import FacultyForm
from service.service.FacultyService import FacultyService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from django.http.response import JsonResponse
import json
from django.core import serializers   

class FacultyCtl(BaseCtl): 
    def preload(self,request,params={}):
        
        self.data = CollegeService().preload(self.form)
        collegeList=[]
        for x in self.data:
            collegeList.append(x.to_json())

        self.data=CourseService().preload(self.form)
        courseList=[]
        for y in self.data:
            courseList.append(y.to_json())

        self.data=SubjectService().preload(self.form)
        subjectList=[]
        for z in self.data:
            subjectList.append(z.to_json())
        return JsonResponse({"collegeList":collegeList,"courseList":courseList,"subjectList":subjectList})   
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["email"] = requestForm["email"]
        self.form["password"] = requestForm["password"]
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["dob"] = requestForm["dob"]
        self.form["college_ID"] = requestForm["college_ID"]
        self.form["subject_ID"] = requestForm["subject_ID"]
        self.form["course_ID"] = requestForm["course_ID"]
        
        

    def get(self,request, params = {}):
        service=FacultyService()
        c=service.get(params["id"])
        res={}
        if(c!=None):
            res["data"]=c.to_json()
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"data":res["data"]})

    def delete(self,request, params = {}):
        service=FacultyService()
        c=service.get(params["id"])
        res={}
        if(c!=None):
            service.delete(params["id"])
            res["data"]=c.to_json()
            res["error"]=False
            res["message"]="Data is Successfully deleted"
        else:
            res["error"]=True
            res["message"]="Data is not deleted"
        return JsonResponse({"data":res})


    def search(self,request, params = {}):
        print("faculty search is found")
        json_request=json.loads(request.body)
        if(json_request):
            params["firstName"]=json_request.get("firstName",None)
            params["pageNo"]=json_request.get("pageNo",None)
        service=FacultyService()
        c=service.search(params)
        self.service = c['data']
        courseList = CourseService().preload(self.form)
        subjectList = SubjectService().preload(self.form)
        collegeList = CollegeService().preload(self.form)

    
        for x in self.service:
            for y in courseList:
                if x.get("course_ID") == y.id:
                    x['courseName'] = y.courseName
            for z in subjectList:
                if x.get('subject_ID') == z.id:
                    x['subjectName'] = z.subjectName
            for d in collegeList:
                if x.get('college_ID') == d.id:
                    x['collegeName'] = d.collegeName

                
        res={}
        
        if(c!=None):
            res["resultkey"]=c["data"]
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse(res)

    def form_to_model(self,obj,request):
        e = CollegeService().get(self.form["college_ID"])
        s= SubjectService().get(self.form["subject_ID"])
        c= CourseService().get(self.form["course_ID"])
        pk = int(request["id"])
        if(pk>0):
            obj.id = pk
        obj.firstName = request["firstName"]
        obj.lastName = request["lastName"]
        obj.email=request["email"] 
        obj.password=request["password"] 
        obj.address=request["address"]  
        obj.gender=request["gender"]  
        obj.dob=request["dob"]  
        obj.college_ID=request["college_ID"]  
        obj.subject_ID=request["subject_ID"]  
        obj.course_ID=request["course_ID"]  
        # obj.collegeName=e.collegeName  
        # obj.subjectName=s.subjectName
        # obj.courseName=c.courseName  
               
        return obj

    def save(self,request, params = {}):      
        json_request=json.loads(request.body)
        self.request_to_form(json_request)
        res={}
        if(self.input_validation()):
            res["error"]=True
            res["message"]="Data is not saved"
        else:
            r=self.form_to_model(Faculty(), json_request)
            service=FacultyService()
            c=service.save(r)
            
            if(r!=None):
                res["data"]=r.to_json()
                res["error"]=False
                res["message"]="Data is Successfully saved"    
        return JsonResponse({"data":res,'form':self.form})

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = "Name can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "last name can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["email"])):
            inputError["email"] = "email can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "password can not be null"
            self.form["error"] = True
        
        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "Address can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["gender"])):
            inputError["gender"] = "gender can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "dob can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["college_ID"])):
            inputError["college_ID"] = "college_ID can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["subject_ID"])):
            inputError["subject_ID"] = "subject_ID can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "course_ID can not be null"
            self.form["error"] = True                  
        return self.form["error"]

    # Template html of Role page    
    def get_template(self):
        return "orsapi/AddFaculty.html"          

    # Service of Role     
    def get_service(self):
        return FacultyService()        
