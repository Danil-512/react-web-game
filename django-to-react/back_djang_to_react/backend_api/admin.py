from django.contrib import admin

from backend_api.models import UsersList, UsersAuthorization, UsersInfo, MyClass1

# Register your models here.
admin.site.register(UsersList)
admin.site.register(UsersAuthorization)
admin.site.register(UsersInfo)
admin.site.register(MyClass1)

