from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Position)
admin.site.register(Department)
admin.site.register(People)
admin.site.register(Categories)
admin.site.register(Users)
admin.site.register(SupportEmployers)
admin.site.register(CategorySupportAssociation)
admin.site.register(Credentials)
admin.site.register(Priority)
admin.site.register(Status)
admin.site.register(Ticket)
admin.site.register(Attachments)
admin.site.register(CustomAttributeType)
admin.site.register(CustomAttribute)
admin.site.register(CategoryCustomAttribute)
admin.site.register(StrAttributeData)
admin.site.register(TextAttributeData)
admin.site.register(ListAttributeDataReference)
admin.site.register(ListAttributeData)
