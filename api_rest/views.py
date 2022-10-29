import base64
import json
import django
from django.views import View
from .models import *
from django.http import JsonResponse
from django.forms import model_to_dict
from  django.db import connection
from datetime import date
import time
import cx_Oracle

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
                query = "SELECT es.user_id ,INITCAP(e.name) || ' ' || INITCAP(e.last_name) as \"full_name\" ,et.position ,es.session_id FROM employee_session es JOIN employee e ON es.user_id = e.id JOIN employee_type et ON e.employee_type_id = et.id WHERE es.user_id = {}".format(post_data['user_id'])
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

class EmployeeDetailView(View):
    def get(self, request, pk):
        employee = Employee.objects.get(pk=pk)
        return JsonResponse(model_to_dict(employee))

class EmployeeLogoutView(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        error = "NO ERROR"
        try:
            query = "update employee_session set session_id = 'NO SESSION' where user_id = {}".format(post_data['user_id'])
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
    
    

class ExtraServicesByIdView(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        cursor.callproc('GET_SERVICE_BY_ID',[out_cursor, post_data['service_id']])
        service = []
        for i in out_cursor:
            service_json = {
                "id": i[0],
                "service_type_id":i[1],
                "name": i[2],
                "price": i[3],
                "location": i[4],
                "available":True if i[5] == 1 else False
            }
            service.append(service_json)
        
        return JsonResponse(service, safe=False)

class ExtraServiceByReservation(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode) 

        cursor.callproc('GET_RESERVATION_EXTRA_SERVICE',[out_cursor, post_data['reservation_id']])
        services = []
        for i in out_cursor:
            if (i[0] == 0):
                continue
            services_id_json = {
                "id":i[0]
            }
            services.append(services_id_json)

        return JsonResponse(services,safe=False)


class AddExtraServicesView(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        extra_services = cursor.callfunc("FN_ADD_SERVICE",int,[post_data['service_type_id'],post_data['name'],post_data['price'],post_data['location'],post_data['available']])
        connection.commit()
        extra_services_response = {
            "response":extra_services
        } 
        return JsonResponse(extra_services_response, safe=False)

class DepartmentView(View):
    def get(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        cursor.callproc('GET_DEPARTMENT',[out_cursor])
        department = []
        for i in out_cursor:
            department_json= {
                "id":i[0],
                "address":i[1],
                "is_new":i[2],
                "qty_room":i[3],
                "price":i[4],
                "commune":i[5],
                "department_type":i[6],
                "short_description":i[7],
                "long_description":i[8],
                "department_image":i[9] if i[9] == None else str(base64.b64encode(i[9].read()), 'utf-8')
            } 
            department.append(department_json)
        return JsonResponse(department, safe=False)
    
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        cursor.callproc('GET_DEPARTMENT_BY_COMMUNE',[out_cursor,post_data['commune']])
        department = []
        for i in out_cursor:
            department_json= {
                "id":i[0],
                "address":i[1],
                "is_new":i[2],
                "qty_room":i[3],
                "price":i[4],
                "commune":i[5],
                "department_type":i[6],
                "short_description":i[7],
                "long_description":i[8],
                "department_image":i[9] if i[9] == None else str(base64.b64encode(i[9].read()), 'utf-8')
            } 
            department.append(department_json)
        return JsonResponse(department, safe=False)
        
class DepartmentViewById(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_cursor = django_cursor.connection.cursor()
        cursor.callproc('GET_DEPTO_BY_ID',[out_cursor, post_data['id']])
        department_result = []
        for i in out_cursor:
            json_department = {
                "id":i[0],
                "address":i[1],
                "qty_room":i[4],
                "price":i[5],
                "commune":i[8],
                "department_type":i[9],
                "short_description":i[2],
                "long_description":i[3],
                "department_image":i[6] if i[6] == None else str(base64.b64encode(i[6].read()), 'utf-8'),
                "is_new":i[10]
            }
            department_result.append(json_department)
        return JsonResponse(department_result, safe=False)

class AddDepartment(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        image = base64.b64decode(post_data['department_image'])
        department = cursor.callfunc("FN_ADD_DEPARTMENT",int,[post_data['address'],post_data['qty_rooms'],post_data['price'],post_data['commune'], post_data['department_type'], post_data['short_description'], post_data['long_description'], image])
        connection.commit()
        department_response = {
            "response":department
        }
        return JsonResponse(department_response, safe=False) 

class CommuneView(View):
    def get(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        cursor.callproc('GET_ALL_COMMUNES', [out_cursor])
        commune = []
        for i in out_cursor:
            commune_json = {
                "id": i[0],
                "commune":i[1],
                "id_region_id":i[2]
            }
            commune.append(commune_json)
        return JsonResponse(commune, safe=False)

class ProductView(View):
    def get(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        cursor.callproc('GET_ALL_PRODUCT',[out_cursor])
        json_product = []
        for i in out_cursor:
            product = {
                "id":i[0],
                "name":i[1],
                "brand":i[2],
                "product_type":i[3]
            }
            json_product.append(product)

        return JsonResponse(json_product,safe=False)

    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_number = cursor.var(cx_Oracle.NUMBER)
        cursor.callproc('ADD_PRODUCT',[post_data['name'], post_data['brand'], post_data['product_type'],post_data['price'], out_number])
        connection.commit()
        id_product = out_number.getvalue()
        return JsonResponse({
            "response":id_product
        })


class ProductViewById(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_cursor = django_cursor.connection.cursor()
        cursor.callproc('GET_PRODUCT_BY_ID', [out_cursor, post_data['product_id']])
        json_product = []
        for i in out_cursor:
            product = {
                "id":i[0],
                "name":i[1],
                "brand":i[2],
                "product_type":i[3],
                "status":i[4]
            }
            json_product.append(product)

        return JsonResponse(json_product, safe=False)


class ProductViewByCategory(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_cursor = django_cursor.connection.cursor()
        cursor.callproc('GET_PRODUCT_BY_CATEGORY', [out_cursor, post_data['department_type']])
        json_product = []
        for i in out_cursor:
            product = {
                "id":i[0],
                "name":i[1],
                "brand":i[2],
                "product_type":i[3]
            }
            json_product.append(product)

        return JsonResponse(json_product, safe=False)

class ProductTypeView(View):
    def get(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        cursor.callproc('GET_PRODUCT_TYPE',[out_cursor])
        product_type = []
        for i in out_cursor:
            product_type_json = {
                "id": i[0],
                "description":i[1]
            }
            product_type.append(product_type_json)
        return JsonResponse(product_type, safe=False)

class ProductStatusView(View):
    def post(self,request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_number = cursor.var(cx_Oracle.NUMBER)
        cursor.callproc('UPDATE_PRODUCT_STATUS',[post_data['product_id'], post_data['status'], out_number])
        connection.commit()
        product_id = out_number.getvalue()
        return JsonResponse({
            "response":product_id
        })



class DepartmentInventoryView(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_cursor = django_cursor.connection.cursor()
        cursor.callproc('GET_DEPARTMENT_INVENTORY',[out_cursor,post_data['department_id']])
        json_inventory = []
        for i in out_cursor:
            inventory = {
                "id":i[0],
                "date_time":i[1].strftime("%d/%m/%Y"),
                "qty":i[2],
                "name":i[3],
                "brand":i[4],
                "product_type":i[5],
                "product_id":i[6],
                "status":i[7],
                "price":i[8]
            }
            json_inventory.append(inventory)

        return JsonResponse(json_inventory,safe=False) 

class AddDepartmentInventoryView(View):
    def post(self,request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_number = cursor.var(cx_Oracle.NUMBER)
        cursor.callproc('ADD_DEPARTMENT_INVENTORY',[post_data['qty'], post_data['department_id'], post_data['product_id'], out_number])
        connection.commit()
        department_inventory_id = out_number.getvalue()
        return JsonResponse({
            "response":department_inventory_id
        })

class getNotaVailableDates(View):
     def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode) 

        out_cursor = django_cursor.connection.cursor()
        out_cursor2 = django_cursor.connection.cursor()
        cursor.callproc('GET_RESERVATION',[out_cursor, post_data['department_id']])
        json_data = []
        dates = {}
        for i in out_cursor:
            dates["check_in"] = i[0].date().strftime("%d/%m/%Y")
            dates["check_out"] = i[1].date().strftime("%d/%m/%Y")

        cursor.callproc('GET_DEPARTMENT_DISPONIBILITY',[out_cursor2, post_data['department_id']])
        for i in out_cursor2:
            dates["maintenance_start"] = i[0].date().strftime("%d/%m/%Y")
            dates["maintenance_finish"] = i[1].date().strftime("%d/%m/%Y")
        json_data.append(dates)

        return JsonResponse(json_data, safe=False)

class AddDepartmentMaintenance(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        out_cursor2 = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_number = cursor.var(cx_Oracle.NUMBER)
        cursor.callproc('GET_DEPARTMENT_DISPONIBILITY',[out_cursor, post_data['department_id']])
        dates = {}
        json_data = []
        flag = 1
        department_maintenance = 0
        named_tuple = time.localtime()
        time_string = time.strftime("%Y/%m/%d", named_tuple)

        if post_data['start_date'] >= time_string:
            for i in out_cursor:
                if post_data['start_date'] >= i[0].date().strftime("%Y/%m/%d") and post_data['start_date'] <= i[1].date().strftime("%Y/%m/%d"):
                    flag = 0
                    department_maintenance = -1
                    break
            cursor.callproc('GET_RESERVATION',[out_cursor2, post_data['department_id']])
            for i in out_cursor2:
                if post_data['start_date'] >= i[0].date().strftime("%Y/%m/%d") and post_data['start_date'] <= i[1].date().strftime("%Y/%m/%d"):
                    flag = 0
                    department_maintenance = -2
                    break
            if flag == 1:
                cursor.callproc('ADD_MAINTENANCE',[post_data['start_date'],post_data['finish_date'],post_data['department_id'], out_number])
                connection.commit()
                department_maintenance = out_number.getvalue()
                json_data.append(dates)

        return JsonResponse({
            "response":department_maintenance
        })

class MarkDepartmentAsAvailable(View):
    def post(self,request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_number = cursor.var(cx_Oracle.NUMBER) 
        cursor.callproc('MARK_DEPARTMENT_AS_AVAILABLE',[post_data['department_id'],out_number])
        return_value = out_number.getvalue()
        return JsonResponse({
            "response":return_value
        })

class ReservationByIdView(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        cursor3 = django_cursor.connection.cursor()
        cursor4 = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_cursor = django_cursor.connection.cursor()
        out_cursor3 = django_cursor.connection.cursor()
        out_cursor4 = django_cursor.connection.cursor()
        reservation = []
        service_extra =[]
        service_extra_reservation = []
        department_result = []
        cursor.callproc('GET_RESERVATION_EXTRA_SERVICE',[out_cursor, post_data['reservation_id']])
        for x in out_cursor:
            service_extra.append(x[0])
        for j in service_extra:
            cursor2 = django_cursor.connection.cursor()
            out_cursor2 = django_cursor.connection.cursor()
            cursor2.callproc('GET_SERVICE_BY_ID',[out_cursor2, j])
            for e in out_cursor2:
                service_extra_json = {
                    "id":e[0],
                    "service_type_id":e[1],
                    "name":e[2],
                    "price":e[3],
                    "location":e[4],
                    "available":True if e[5] == 1 else False
                }
                service_extra_reservation.append(service_extra_json)
            cursor2.close()
            out_cursor2.close()

        cursor3.callproc('GET_RESERVATION_BY_ID',[out_cursor3, post_data['reservation_id']])
        for i in out_cursor3:
            cursor4.callproc('GET_DEPTO_BY_ID',[out_cursor4, i[11]])
            for z in out_cursor4:
                json_department = {
                    "id":z[0],
                    "address":z[1],
                    "qty_room":z[4],
                    "price":z[5],
                    "commune":z[8],
                    "department_type":z[9],
                    "short_description":z[2],
                    "long_description":z[3],
                    "department_image":z[6] if z[6] == None else str(base64.b64encode(z[6].read()), 'utf-8'),
                    "is_new":z[10]
                }
                department_result.append(json_department)
            reservation_json = {
                "id":i[0],
                "total_amount":i[1],
                "reservation_amount":i[2],
                "qty_customers":i[3],
                "reservation_date":i[4].strftime("%Y/%m/%d"),
                "check_in":i[5].strftime("%Y/%m/%d"),
                "check_out":i[6].strftime("%Y/%m/%d"),
                "status":i[7],
                "first_name":i[8],
                "last_name":i[9],
                "email":i[10],
                "department":department_result,
                "service_extra":service_extra_reservation
            }
            reservation.append(reservation_json)

        return JsonResponse(reservation, safe=False)

class ReservationStatusView(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor() 
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_number = cursor.var(cx_Oracle.NUMBER) 
        cursor.callproc('MARK_RESERVATION',[post_data['reservation_id'], post_data['action'], out_number])
        return_value = out_number.getvalue()
        return JsonResponse({
            "response":return_value
        }) 

class ReservationView(View):
    def get(self,request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        cursor.callproc('GET_ALL_RESERVATIONS',[out_cursor])
        reservation = []
        for i in out_cursor:
            reservation_json ={
                "id":i[0],
                "total_amount":i[1],
                "reservation_amount":i[2],
                "qty_customers":i[3],
                "check_in":i[4],
                "check_out":i[5],
                "status":i[6],
                "first_name":i[7],
                "last_name":i[8],
                "email":i[9],
                "department_id":i[10]
            }
            reservation.append(reservation_json)
        return JsonResponse(reservation, safe=False)

class AddTransactionView(View):
    def post(self,request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        out_number = cursor.var(cx_Oracle.NUMBER)
        print(post_data)
        cursor.callproc('ADD_TRANSACTION',[post_data['reservation_id'], post_data['amount'],post_data['status'],post_data['transaction_type'],out_number])
        connection.commit()
        id_transaction = out_number.getvalue()
        return JsonResponse({
            "id_transaction":id_transaction
        })


class AddExtraServiceToReservation(View):
    def post(self, request):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cursor = django_cursor.connection.cursor()
        json_decode = request.body.decode('utf-8')
        post_data = json.loads(json_decode)
        total_amount = 0
        cursor.callproc('GET_RESERVATION_BY_ID',[out_cursor, post_data['reservation_id']])
        for i in out_cursor:
            total_amount = i[1]

        service_price = 0
        for z in post_data['services']:


            reservation_details_out = cursor.var(cx_Oracle.NUMBER)
            cursor_reservation_details=django_cursor.connection.cursor()
            cursor_reservation_details.callproc('ADD_RESERVATION_DETAILS',[z, post_data['reservation_id'], reservation_details_out])
            cursor_reservation_details.close()
            if reservation_details_out.getvalue() > 0:
                cursor2 = django_cursor.connection.cursor()
                out_cursor2 = django_cursor.connection.cursor()
                cursor2.callproc('GET_SERVICE_BY_ID',[out_cursor2, z])

                for x in out_cursor2:
                    service_price+=x[3]
                cursor2.close()
                out_cursor2.close()

        total = total_amount + service_price
        cursor4 = django_cursor.connection.cursor()
        out_number = cursor.var(cx_Oracle.NUMBER)
        cursor4.callproc('UPDATE_RESERVATION_TOTAL', [post_data['reservation_id'], total, out_number])
        return_value = out_number.getvalue()

        return JsonResponse({
            "response":return_value
        }) 

