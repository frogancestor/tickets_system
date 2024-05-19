from django.db import models
from datetime import date, timedelta
# Create your models here.


class Position(models.Model):
    position = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.position}"


class Department(models.Model):
    department = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.department}"


class People(models.Model):
    surname = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    email = models.CharField(unique=True, max_length=20)
    phone = models.IntegerField(unique=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"


class Categories(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category}"


class Users(models.Model):
    person = models.ForeignKey(People, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.person}"


class SupportEmployers(models.Model):
    person = models.ForeignKey(People, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.person}"


class CategorySupportAssociation(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    support_employee = models.ForeignKey(SupportEmployers, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} {self.support_employee}"


class Credentials(models.Model):
    login = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    user = models.ForeignKey(People, on_delete=models.CASCADE)


class Priority(models.Model):
    priority = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.priority}"


class Status(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.status}"


class Ticket(models.Model):
    title = models.CharField(max_length=50) # определяет юзер
    description = models.CharField(max_length=250) # определяет юзер
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    support_employee = models.ForeignKey(CategorySupportAssociation, on_delete=models.CASCADE, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE) # определяет юзер
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


class Attachments(models.Model):
    file_name = models.CharField(max_length=30)
    file_extension = models.CharField(max_length=10)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)


class CustomAttributeType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class CustomAttribute(models.Model):
    name = models.CharField(unique=True, max_length=100)
    typeOfAttribute = models.ForeignKey(CustomAttributeType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.typeOfAttribute}"


class CategoryCustomAttribute(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    custom_attribute = models.ForeignKey(CustomAttribute, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.custom_attribute}"


class StrAttributeData(models.Model):
    data = models.CharField(max_length=30)
    attribute = models.ForeignKey(CustomAttribute, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attribute} - {self.data}"


class TextAttributeData(models.Model):
    data = models.CharField(max_length=250)
    attribute = models.ForeignKey(CustomAttribute, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attribute} - {self.data}"


class ListAttributeDataReference(models.Model):
    data = models.CharField(max_length=30)
    attribute = models.ForeignKey(CustomAttribute, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attribute} - {self.data}"


class ListAttributeData(models.Model):
    attribute = models.ForeignKey(CustomAttribute, on_delete=models.CASCADE)
    data = models.ForeignKey(ListAttributeDataReference, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attribute} - {self.data}"


class AutorizatedPeople(models.Model):
    token = models.CharField(max_length=128)
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    expiration_date = models.DateField(default=date.today() + timedelta(days=5))
