from src import consts as c
import pytest
import httpx
from urllib.parse import urlparse, parse_qs

@pytest.mark.parametrize("url, expected_status", [
    (c.auth_url, 200),
])
def test_auth_url(url, expected_status):
    """
    Отправляет GET-запрос к указанному URL с помощью httpx и проверяет статус-код.
    """
    try:
        response = httpx.get(url, timeout=10.0)
        assert response.status_code == expected_status, \
            f"Ожидался статус {expected_status}, но получен {response.status_code}"
    except httpx.TimeoutException:
        pytest.fail(f"Запрос к {url} превысил таймаут (10 секунд)")
    except httpx.ConnectError:
        pytest.fail(f"Не удалось подключиться к {url}. Проверьте URL и подключение к сети.")
    except httpx.RequestError as e:
        pytest.fail(f"Произошла ошибка при запросе: {e}")


new_code=""
# get authorization code
@pytest.mark.parametrize("url, expected_status", [
    (c.auth_url, 302),
])
def test_status_code(url, expected_status):
    """
    Отправляет GET-запрос к указанному URL с помощью httpx, 
    проверяет статус-код и получает authorization code из редиректа.
    """
    try:
        params = {
            "response_type": "code",
            "client_id": c.Client,
        }

        # Отключаем авто-редирект
        response = httpx.get(url, params=params, timeout=10.0, follow_redirects=False)

        assert response.status_code == expected_status, \
            f"Ожидался статус {expected_status}, но получен {response.status_code}"

        # Получаем URL редиректа
        location = response.headers.get("Location")
        if not location:
            pytest.fail("Заголовок Location отсутствует в ответе")

        # Парсим код авторизации
        parsed_url = urlparse(location)
        query_params = parse_qs(parsed_url.query)
        code_list = query_params.get("code")

        if not code_list:
            pytest.fail("Параметр 'code' не найден в редиректе")

        new_code = str(code_list[0])
        print(f"Authorization code: {new_code}")

    except httpx.TimeoutException:
        pytest.fail(f"Запрос к {url} превысил таймаут (10 секунд)")
    except httpx.ConnectError:
        pytest.fail(f"Не удалось подключиться к {url}. Проверьте URL и подключение к сети.")
    except httpx.RequestError as e:
        pytest.fail(f"Произошла ошибка при з+апросе: {e}")


#post token
#редиректит на localhost  и передает туда code нужно оттуда как то своровать)
@pytest.mark.parametrize("url, expected_status", [
    (c.token_url, 200),
])
def test_get_token(url, expected_status, code=new_code):
    """
    Отправляет POST-запрос к указанному URL с помощью httpx и проверяет статус-код.
    """
    try:
        param={
            "client_id":c.Client,  
            "client_secret": c.Client_Secret,  
            "code": code,
            "grant_type":"authorization_code",
        }
        response = httpx.post(url, params=param, timeout=10.0)
        assert response.status_code == expected_status, \
            f"Ожидался статус {expected_status}, но получен {response.status_code}"
    except httpx.TimeoutException:
        pytest.fail(f"Запрос к {url} превысил таймаут (10 секунд)")
    except httpx.ConnectError:
        pytest.fail(f"Не удалось подключиться к {url}. Проверьте URL и подключение к сети.")
    except httpx.RequestError as e:
        pytest.fail(f"Произошла ошибка при запросе: {e}")

#test url https://api.hh.ru/openapi/redoc#tag/Vakansii/operation/apply-to-vacancy
#test url https://api.hh.ru/openapi/redoc#tag/Perepiska-(otklikipriglasheniya)-dlya-soiskatelya/operation/get-negotiation-item
#test get my resume https://api.hh.ru/resumes/mine
# test подборка вакансий похожих на резюме https://api.hh.ru/resumes/{resume_id}/similar_vacancies