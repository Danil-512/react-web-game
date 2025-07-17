from django.core.cache import cache
import json
from django.http import JsonResponse


def check_user_token_in_redis(request):
    """
    Проверяет, есть ли токен текущего пользователя в Redis.
    Возвращает True если токен найден и пользователь аутентифицирован, иначе False.
    """
    if not request.user.is_authenticated:
        return False

    if not hasattr(request, 'session') or not request.session.session_key:
        return False

    # Формируем ключ, под которым хранится сессия в Redis
    redis_key = f'django.contrib.sessions.cache.{request.session.session_key}'
    session_data = cache.get(redis_key)

    if not session_data:
        return False

    # Проверяем, что в данных сессии есть информация о пользователе
    if isinstance(session_data, bytes):
        session_data = session_data.decode('utf-8')

    try:
        if isinstance(session_data, str):
            session_data = json.loads(session_data)
    except json.JSONDecodeError:
        pass

    if isinstance(session_data, dict) and '_auth_user_id' in session_data:
        return session_data['_auth_user_id'] == str(request.user.id)

    return False

def debug_redis_sessions(request):
    try:
        # Логирование текущего состояния
        print("\n=== DEBUG SESSION INFO ===")
        print(f"Current session key: {request.session.session_key}")
        print(f"Session exists in request: {'yes' if hasattr(request, 'session') else 'no'}")

        # Получаем все ключи
        all_keys = cache.keys('*')
        print(f"\nAll keys in Redis: {all_keys}")

        # Фильтруем только сессии
        session_keys = [k for k in all_keys if k.startswith('django.contrib.sessions.cache.')]
        print(f"\nFound {len(session_keys)} session keys")

        sessions = []
        for key in session_keys:
            data = cache.get(key)
            print(f"\nProcessing key: {key}")
            print(f"Raw data: {data}")

            try:
                if isinstance(data, bytes):
                    data = data.decode('utf-8')
                if isinstance(data, str):
                    try:
                        data = json.loads(data)
                    except json.JSONDecodeError:
                        pass

                session_key = key.replace('django.contrib.sessions.cache.', '')
                sessions.append({
                    'key': session_key,
                    'user_id': data.get('_auth_user_id') if isinstance(data, dict) else None,
                    'data': data
                })
            except Exception as e:
                print(f"Error processing key {key}: {str(e)}")
                sessions.append({
                    'key': key,
                    'error': str(e)
                })

        return JsonResponse({
            'status': 'success',
            'current_session_key': request.session.session_key,
            'sessions': sessions,
            'all_redis_keys': all_keys
        })

    except Exception as e:
        print(f"\nError in debug_redis_sessions: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def test_redis_connection(request):
    try:
        # Тестовая запись
        cache.set('test_key', {'user_id': 1, 'test_data': 'hello'}, timeout=60)

        # Чтение
        data = cache.get('test_key')

        return JsonResponse({
            'status': 'success',
            'data_written': {'user_id': 1, 'test_data': 'hello'},
            'data_read': data,
            'keys_in_redis': cache.keys('*')
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
