import json
from django.views import View
from .models import *
from django.http import JsonResponse
from django.forms import model_to_dict
from  django.db import connection


class EmployeeLoginView(View):
    def post(self,request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        user_id = 0
        session = ''
        error = ''
        if post_data['login'] == 1:
            try:
                query = "SELECT CASE WHEN (SELECT count(session_id) FROM employee_session WHERE user_id_id = {} ) <= 0 THEN to_char('UNREGISTER') ELSE (SELECT to_char(session_id) FROM employee_session WHERE user_id_id = {} ) END AS \"session_id\" FROM DUAL".format(post_data['user_id'],post_data['user_id'])
                result = cursor.execute(query)
                for i in result:
                    session = i[0]
            except:
                error = "ERROR"
        elif post_data['login'] == 2:
            try:
                login = cursor.callfunc("FN_LOGIN",int ,[post_data['username'],post_data['password']])
                connection.commit()
                user_id = login
            except:
                error = "ERROR"

        result_data = {
            "user_id":user_id,
            "session": session,
            "error": error
        }

        return JsonResponse(result_data, safe=False)

class EmployeeView(View):
    def post(self,request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        user_id = 0
        full_name = ""
        position = ""
        session_id = ""
        error = "NO ERROR"
        if post_data['user_id'] > 0:
            try:
                query = "SELECT es.user_id_id ,INITCAP(e.name) || ' ' || INITCAP(e.last_name) as \"full_name\" ,et.position ,es.session_id FROM employee_session es JOIN employee e ON es.user_id_id = e.id JOIN employee_type et ON e.employee_type_id_id = et.id WHERE es.user_id_id = {}".format(post_data['user_id'])
                result = cursor.execute(query)
                for i in result:
                    user_id = i[0]
                    full_name = i[1]
                    position = i[2]
                    session_id = i[3]
            except:
                error = "ERROR"

            result_data = {
                "user_id":user_id,
                "full_name":full_name,
                "position":position,
                "session_id":session_id,
                "error":error
            }
        return JsonResponse(result_data, safe=False)

class EmployeeLogoutView(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        error = "NO ERROR"
        try:
            query = "update employee_session set session_id = 'NO SESSION' where user_id_id = {}".format(post_data['user_id'])
            result = cursor.execute(query)
            connection.commit()
        except:
            error = "ERROR"

        result_data = {
            "error":error    
        }
        return JsonResponse(result_data, safe=False)



class ExtraServicesView(View):

    def get(self, request):
        extra_services = Services.objects.all()
        return JsonResponse(list(extra_services.values()), safe=False)

    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        name = ""
        price = 0
        location = ""
        avaible = ""
        #extra_services = cursor.callfunc("FN_ADD_SERVICE",int ,['service_type','name','price','location','avaible'])


        extra_services_response = {
            "name":name,
            "price":price,
            "location":location,
            "available":avaible
        } 
        return JsonResponse(extra_services_response, safe=False)
    

class EmployeeDetailView(View):
    def get(self, request, pk):
        employee = Employee.objects.get(pk=pk)
        return JsonResponse(model_to_dict(employee))
