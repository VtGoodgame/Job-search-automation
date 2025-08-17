import httpx
from urllib.parse import urlparse, parse_qs
from src import consts as c


def get_access_code(code_telegram: int) -> str:
    """
    Получает authorization_code от hh.ru через редирект.
    Возвращает строку code.
    """
    url = "https://hh.ru/oauth/authorize"
    params = {
        "response_type": "code",
        "client_id": c.Client,
        "state": code_telegram,
        "redirect_uri": c.Redirect, # Убедитесь, что Redirect указан правильно
    }
    # Используем httpx для отправки GET-запроса
    # и отключаем авто-редирект, чтобы получить код авторизации
    try:
        with httpx.Client(follow_redirects=False, timeout=10.0) as client:
            resp = client.get(url, params=params)

            if resp.status_code != 302:
                raise Exception(f"Ожидался редирект (302), но получен {resp.status_code}")

            # Забираем редирект (http://localhost/?code=...&state=...)
            location = resp.headers.get("Location")
            if not location:
                raise Exception("В ответе нет заголовка Location")

            # Парсим код из Location
            parsed = urlparse(location)
            query = parse_qs(parsed.query)
            code_list = query.get("code")
            if not code_list:
                raise Exception("В редиректе нет параметра 'code'")

            return code_list[0]

    except httpx.RequestError as e:
        raise Exception(f"Ошибка при запросе: {e}")


def get_token_app():
    """
    Функция для получения токена от лица приложения.
    """
    url = "https://hh.ru/oauth/token"
    headers ={
        "client_id": c.Client,
        "client_secret": c.Client_Secret,
        "grant_type": "client_credentials"
    }
    responce = httpx.post(url, headers=headers)
    if responce.status_code == 200:
        token = responce.json().get("access_token")
        if token:
            return token    
    else:
        raise Exception(f"Ошибка при получении токена: {responce.status_code} - {responce.text}")
    
def get_user_token(user_code):
    """
    Функция для получения токена пользователя.
    """
    url = "https://hh.ru/oauth/token"
    headers = {
        "client_id": c.Client,
        "client_secret": c.Client_Secret,
        "grant_type": "authorization_code",
        "code": user_code,
        "redirect_uri": c.Redirect
    }
    response = httpx.post(url, headers=headers)
    if response.status_code == 200:
        token = response.json().get("access_token")
        if token:
            return token
    else:
        raise Exception(f"Ошибка при получении токена пользователя: {response.status_code} - {response.text}")
    
def refresh_access_token(refresh_token):
    """
    Функция для обновления токена доступа.
    """
    url = "https://hh.ru/oauth/token"
    headers = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    response = httpx.post(url, headers=headers)
    if response.status_code == 200:
        new_token = response.json().get("access_token")
        if new_token:
            return new_token
    else:
        raise Exception(f"Ошибка при обновлении токена: {response.status_code} - {response.text}")