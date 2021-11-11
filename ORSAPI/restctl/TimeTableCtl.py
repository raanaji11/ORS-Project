


from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import TimeTable
from service.forms import TimeTableForm
from service.service.TimeTableService import TimeTableService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from django.http.response import JsonResponse 
import json
# from django.core import serializers

class TimeTableCtl(BaseCtl): 
    
    def preload(self,request,params={}):
        
        self.data=CourseService().preload(self.form)
        courseList=[]
        for y in self.data:
            courseList.append(y.to_json())

        self.data=SubjectService().preload(self.form)
        subjectList=[]
        for z in self.data:
            subjectList.append(z.to_json())
        return JsonResponse({"courseList":courseList,"subjectList":subjectList})   

    def get(self,request, params = {}):
        service=TimeTableService()
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
        service=TimeTableService()
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
        json_request=json.loads(request.body)
        if(json_request):
            params["semester"]=json_request.get("semester",None)
            params["pageNo"]=json_request.get("pageNo",None)
     
        service=TimeTableService()
        c=service.search(params)
        self.service = c['data']
        courseList = CourseService().preload(self.form)
        subjectList = SubjectService().preload(self.form)
        

    
        for x in self.service:
            for y in courseList:
                if x.get("course_ID") == y.id:
                    x['courseName'] = y.courseName
            for z in subjectList:
                if x.get('subject_ID') == z.id:
                    x['subjectName'] = z.subjectName
            

                
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
        pk = int(request["id"])
        if(pk>0):
            obj.id = pk
        obj.examTime = request["examTime"]
        obj.examDate = request["examDate"]
        obj.subject_ID = request["subject_ID"] 
        obj.subjectName=request["subjectName"]
        obj.course_ID=request["course_ID"]
        obj.courseName=request["courseName"]
        obj.semester=request["semester"]
        return obj
  
    def save(self,request, params = {}):        
        json_request=json.loads(request.body)     
        r=self.form_to_model(TimeTable(), json_request)
        service=TimeTableService()
        c=service.save(r)
        res={}
        if(r!=None):
            res["data"]=r.to_json()
            res["error"]=False
            res["message"]="Data is Successfully saved"
        else:
            res["error"]=True
            res["message"]="Data is not saved"
        return JsonResponse({"data":res})

    # Template html of Role page    
    def get_template(self):
        return "orsapi/TimeTable.html"  

    # def input_validation(self):
    #     super().input_validation()
    #     inputError =  self.form["inputError"]
    #     if(DataValidator.isNull(self.form["examTime"])):
    #         inputError["examTime"] = " examTime can not be null"
    #         self.form["error"] = True

    #     if(DataValidator.isNull(self.form["examDate"])):
    #         inputError["examDate"] = "examDate can not be null"
    #         self.form["error"] = True

    #     if(DataValidator.isNull(self.form["subject_ID"])):
    #         inputError["subject_ID"] = "subject_ID can not be null"
    #         self.form["error"] = True

        

    #     if(DataValidator.isNull(self.form["course_ID"])):
    #         inputError["course_ID"] = "course Name can not be null"
    #         self.form["error"] = True

       
    #     if(DataValidator.isNull(self.form["semester"])):
    #         inputError["semester"] = "semester can not be null"
    #         self.form["error"] = True

    #     return self.form["error"]         

    # Service of Role     
    def get_service(self):
        return TimeTableService()        


       



