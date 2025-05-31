from .models import CustomUserManager, AccessTypes
from .serializer import UserAccessSerializer, AccessTypesSerializer

from .models import CustomUser
from .serializer import UsersListSerializer

from .serializer import UsersInfoSerializer

#from sequences import get_next_value

from .models import UserInfo
from django.contrib.auth.hashers import make_password



def access_type_create(p_id, p_descr):
    # Проверяем, не существует ли уже такой тип доступа
    if not AccessTypes.objects.filter(accessTypeId=p_id).exists():
        print('Такого типа прав доступа еще не было')
        AccessTypes.objects.create(accessTypeId=p_id, accessTypeDescr=p_descr)
    else:
        print('Попытка создать права доступа с существующим номером')


def ensure_default_access_type():
    if not AccessTypes.objects.filter(accessTypeId=1).exists():
        access_type_create(1, 'standard')

# Функция на добавление нового пользователя
# def add_new_user(p_user_login, p_user_password):
#
#     try:
#         if UsersList.objects.filter(userLogin=p_user_login).exists():
#             print(f"Пользователь с логином {p_user_login} уже существует")
#             return False
#
#         # Создание стандартного типа доступа если его нет
#         ensure_default_access_type()
#
#         # Получение стандартного типа доступа
#         default_access = AccessTypes.objects.get(accessTypeId=1)
#
#         print('User Create Start')
#         # Добавление данных в таблицу с пользователями
#         new_user = UsersList.objects.create(
#             userLogin=p_user_login
#         )
#         new_user1 = UsersList.objects.get(userLogin=p_user_login).userId
#         print(f'New id is: {new_user1}')
#         #UsersList.objects.create(userId=new_user, userLogin=p_user_login)
#         # Добавление данных в таблицу с паролями
#         UsersAuthorization.objects.create(userId=new_user,  userPassword=p_user_password)
#         # Добавление строки без данных в таблицу с личной информацией. Заполняется в другой функции.
#         UsersInfo.objects.create(userId=new_user, userFirstName='', userSecondName='', userEmail='')
#         # Добавление строки в таблицу с информацией о правах доступа пользователя
#         UsersAccess.objects.create(userId=new_user, accessTypeId=default_access)
#         return True
#
#     except Exception as e:
#         #print(f"Error creating user: {e}")
#         print("Ошибка регистрации")
#         return False

def add_new_user(p_user_login, p_user_password):
    try:
        # Проверка существования пользователя
        if CustomUser.objects.filter(username=p_user_login).exists():
            print(f"Пользователь с логином {p_user_login} уже существует")
            return False

        # Создание стандартного типа доступа если его нет
        ensure_default_access_type()

        # Получение стандартного типа доступа
        default_access = AccessTypes.objects.get(accessTypeId=1)

        print('User Create Start')

        # Создаем пользователя через кастомный менеджер
        new_user = CustomUser.objects.create_user(
            username=p_user_login,
            password=p_user_password,
            access_type=default_access
        )

        print(f'New id is: {new_user.id}')

        # Создаем пустую запись с дополнительной информацией
        UserInfo.objects.create(
            user=new_user,
            first_name='',
            second_name='',
            email=''
        )

        return True

    except Exception as e:
        print(f"Ошибка регистрации: {str(e)}")
        return False

