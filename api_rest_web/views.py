from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from api_rest_web.serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views import View

from  django.db import connection
from django.forms import model_to_dict

#from backend_django.api.models import Department
from api_rest.models import Department

# Create your views here.

""" INIT autenticacion cliente """
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# muestra utilidades de api rest en http://localhost:8000/api/
@api_view(['GET'])
def getRoutes(request):
    routes = [
        #'/api/token/',
        #'/api/register/',
        #'/api/token/refresh/',
        #'/api/deptos/'
        '/api_web/token/',
        '/api_web/register/',
        '/api_web/token/refresh/',
        #'/api_rest_web/deptos/'
    ]
    return Response(routes)

#  solo para testear de qe token capturado funca
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST) 
    
""" FIN autenticacion cliente """

""" #! INIT servicios para front """

class DeptoView(View):
    # Funcion Para obtener datos de deptos
    def get(self, request,id=0):

        # SI viene una id como parametro, buscar SOLO 1 depa, filtrando x el id otorgado
        if(id>0):
            query = """
                    SELECT 
                        d.id,
                        d.status,
                        d.price, 
                        r.region,
                        c.commune, 
                        d.address, 
                        d.short_description,
                        d.long_description,
                        d.capacity,
                        d.qty_rooms,
                        d.link_img
                    FROM 
                        department d 
                    JOIN
                        commune c
                    ON 
                        c.id = d.commune_id
                    JOIN 
                        region r
                    ON
                        r.id = c.region_id
                    WHERE
                        d.id = %s
                    """
            #ejecucion de la consulta usando funcion helper
            data = execute_to_dict(query,[id])                    
            
            return JsonResponse({
                'message': 'success',
                'deptos': data
            })        

        # si NO viene una id como parametro, buscar TODOS los depas
        else:
            query = """
                    SELECT 
                        d.id,
                        d.status,
                        d.price, 
                        r.region,
                        c.commune, 
                        d.address, 
                        d.short_description,
                        d.long_description,
                        d.capacity,
                        d.qty_rooms,
                        d.link_img
                    FROM 
                        department d 
                    JOIN
                        commune c
                    ON 
                        c.id = d.commune_id
                    JOIN 
                        region r
                    ON
                        r.id = c.region_id
                    """

            #ejecucion de la consulta usando funcion helper
            data = execute_to_dict(query)
        
            return JsonResponse({
                'message': 'success',
                'deptos': data
            })        

# funcion helper para ejecutar consultas a la bd,
# ademas rescata columnas de la consulta y las implementa como "clave" en el json a retornar
def execute_to_dict(query, params=None):
    with connection.cursor() as c:
        c.execute(query, params or [])
        names = [col[0].lower() for col in c.description]
        return [dict(list(zip(names, values))) for values in c.fetchall()]
