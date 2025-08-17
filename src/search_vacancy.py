import httpx
import asyncio
from src import consts as c

def get_dictionary():
    """
    Функция для получения справочников hh.ru.
    Возвращает словарь с данными.
    """
    url = "https://api.hh.ru/dictionaries"
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except httpx.RequestError as e:
        raise Exception(f"Ошибка при запросе: {e}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")


def global_search_vacancy():
    """
    Функция для глобального поиска вакансий на hh.ru с учетом использования фильтров.
    Возвращает JSON-ответ с найденными вакансиями.
    """
    url="https://api.hh.ru/vacancies"
    data = {
        "page": 0,
        "per_page": 100,
        "text": ("https://api.hh.ru/vacancies?page=0&per_page=100&"
                 "text=(python* OR NAME:python*) AND NOT ( SQL OR Java OR JavaScript OR JS OR "
                 " C++ OR PHP OR Go OR Ruby OR Наставник OR Учитель OR Преподаватель)"
                 "&experience=noExperience&area=1&professional_role=96&premium=True"),  # Поиск по ключевому слову
        "experience":"noExperience, between1And3", #опыт работы вставить id из справочника hh
        "area": (1,2019), #регион вставить id из справочника hh
        "professional_role":96, #профессиональная роль вставить id из справочника hh
        "premium": True, #премиум вакансии
    }
    try:
        response = httpx.get(url, data=data, timeout=10.0)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except httpx.RequestError as e:
        raise Exception(f"Ошибка при запросе: {e}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
   
    
def get_suitable_vacancies(resume_id: int, bearer: str):
    """
    Функция для фильтрации подходящих вакансий по резюме.
    Возвращает список подходящих вакансий.
    """
    url="https://api.hh.ru/resumes/{resume_id}/similar_vacancies"
    data = {"resume_id": resume_id,
               "bearer":bearer} 
    try:
        response = httpx.get(url, data=data, timeout=10.0)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except httpx.RequestError as e:
        raise Exception(f"Ошибка при запросе: {e}") 
    
def get_vacancy_details(vacancy_id: int, bearer: str):
    """
    Возвращает подробную информацию по указанной вакансии
    Функция для получения деталей вакансии по ID.
    Возвращает JSON-ответ с деталями вакансии.
    """
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except httpx.RequestError as e:
        raise Exception(f"Ошибка при запросе: {e}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
    
def respond_to_vacancy(vacancy_id: int, resume_id: int, bearer: str):
    """
    Функция для отклика на вакансию.
    Возвращает JSON-ответ с результатом отклика.
    """
    url = "https://api.hh.ru/negotiations"
    headers = {"Authorization": bearer,} 
    data = {"message": "",
            "resume_id": resume_id,
            "vacancy_id":vacancy_id}# Сопроводительное сообщение можно добавить в заголовок
    try:
        response = httpx.post(url, json=data, headers=headers, data = data, timeout=10.0)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except httpx.RequestError as e:
        raise Exception(f"Ошибка при запросе: {e}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")