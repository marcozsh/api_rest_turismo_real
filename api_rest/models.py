from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
from distutils.command.check import check
from distutils.command.upload import upload
from operator import mod
from pyexpat import model
from re import I
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models



class Region(models.Model):
    region = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'region'
        ordering = ['id']

class Commune(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='id_region_fk', default=None)
    commune = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'commune'
        ordering = ['id']

class Company(models.Model):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='commune_id_fk', default=None)
    rut = models.CharField(max_length=100, null=False)
    company_name = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    mail_address = models.CharField(max_length=100, null=False)
    legal_representative = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'company'
        ordering = ['id']

class WorkArea(models.Model):
    description = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'work_area'
        ordering = ['id']

class EmployeeType(models.Model):
    position = models.CharField(max_length=100, null=False)
    work_area = models.ForeignKey(WorkArea, on_delete=models.CASCADE, related_name='work_area_id_fk', default=None)
    class Meta:
        db_table = 'employee_type'
        ordering = ['id'] 

class Employee(models.Model):
    employee_type = models.ForeignKey(EmployeeType, on_delete=models.CASCADE, related_name='employee_type_id_fk', default=None)
    rut = models.CharField(max_length=100, null=False)
    name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    mail_address = models.EmailField(max_length=100, null=False)
    profile_photo = models.BinaryField(blank=True, null=True)
    class Meta:
        db_table = 'employee'
        ordering = ['id']

class EmployeeAccount(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='user_id_fk', default=None)
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'employee_account'
        ordering = ['id']

class EmployeeSession(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='session_user_id_fk', default=None)
    session_id = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'employee_session'
        ordering = ['id']


class Payment(models.Model):
    type = models.CharField(max_length=100, null=False)
    guarantee_payment = models.IntegerField(default=0, null=False)
    amount = models.IntegerField(default=0, null=False)
    total_payment = models.IntegerField(default=0, null=False)
    class Meta:
        db_table = 'payment'
        ordering = ['id']

class Rent(models.Model):
    tariff = models.IntegerField(default=0, null=False)
    rental_date = models.DateField(null=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payment_id_fk', default=None)
    class Meta:
        db_table = 'rent'
        ordering = ['id']

class ProductType(models.Model):
    description = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'product_type'
        ordering = ['id']

class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='product_type_fk', default=None)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    product_image = models.BinaryField(blank=True, null=True)
    class Meta:
        db_table = 'product'
        ordering = ['id']

class Customer(models.Model):
    rut = models.CharField(max_length=100, null=False)
    name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'customer'
        ordering = ['id']


class CustomerAccount(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_user_id_fk', default=None)
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    regular_customer = models.BooleanField(default=False)
    class Meta:
        db_table = 'customer_account'
        ordering = ['id']

class Vehicle(models.Model):
    color = models.CharField(max_length=100, null=False)
    id_vehicle = models.CharField(max_length=100, null=False)
    brand = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'vehicle'
        ordering = ['id']

class DepartmentType(models.Model):
    description = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'department_type'
        ordering = ['id']

class Department(models.Model):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='department_commune_id_fk', default=None)
    department_type = models.ForeignKey(DepartmentType, on_delete=models.CASCADE, related_name='department_type_id_fk', default=None)
    address = models.CharField(max_length=100, null=False)
    status = models.BooleanField(default=False)
    short_description = models.CharField(max_length=100, null=False, default='')
    long_description = models.CharField(max_length=200, null=True)
    qty_rooms = models.IntegerField(default=0, null=False)
    price = models.IntegerField(default=0, null=False)
    department_image = models.BinaryField(blank=True, null=True)
    class Meta:
        db_table = 'department'
        ordering = ['id']

class DepartmentMaintenance(models.Model):
    maintenance_date = models.DateField(null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_maintance_id_fk', default=None)
    last_maintenance = models.DateField(null=False)
    description = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'department_maintenance'
        ordering = ['id']

class DepartmentInventory(models.Model):
    department = models.ForeignKey (Department, on_delete=models.CASCADE, related_name='department_id_fk', default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_id_fk', default=None)
    date_time = models.DateField(null=False)
    qty = models.IntegerField(default=0, null=False)
    class Meta:
        db_table = 'department_inventory'
        ordering = ['id']


class ServicesType(models.Model):
    description = models.CharField(max_length=200, null=False)
    class Meta:
        db_table = 'service_type'
        ordering = ['id']

class Services(models.Model):
    service_type = models.ForeignKey(ServicesType, on_delete=models.CASCADE, related_name='service_type_fk', default=None)
    name = models.CharField(max_length=200, null=False, default=None)
    price = models.IntegerField(default=0, null=False)
    location = models.CharField(max_length=250, null=True, default=None)
    available = models.BooleanField(default=False)
    class Meta:
        db_table = 'service'
        ordering = ['id']

class ReservationStatus(models.Model):
    status = models.BooleanField(default=False)
    class Meta:
        db_table = 'reservation_status'
        ordering = ['id']

class Finance(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='finance_user_id_fk', default=None)
    income = models.IntegerField(default=0, null=False)
    egress = models.IntegerField(default=0, null=False)
    total = models.IntegerField(default=0, null=False)
    date_time = models.DateField(null=False)
    class Meta:
        db_table = 'finance'
        ordering = ['id']

class Tour(models.Model):
    destination = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    hire_date = models.DateField(null=False)
    class Meta:
        db_table = 'tour'
        ordering = ['id']

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='r_id_customer_fk', default=None)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='r_id_service_fk', default=None)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='r_id_payment_fk', default=None)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='r_id_employee_fk', default=None)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='r_id_vehicle_fk', default=None)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='r_id_department_fk', default=None)
    reservation_status = models.ForeignKey(ReservationStatus, on_delete=models.CASCADE, related_name='r_id_reservation_status_fk', default=None)
    qty_customer = models.IntegerField(default=1, null=False)
    reservation_date = models.DateField(null=False)
    check_in = models.DateField(null=False)
    check_out = models.DateField(null=False)
    class Meta:
        db_table = 'reservation'
        ordering = ['id']

