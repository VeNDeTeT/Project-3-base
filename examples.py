"""
Примеры использования проекта (для тестирования и демонстрации).
Этот файл показывает, как использовать отдельные модули проекта.
"""

from api_manager import HeadHunterAPI
from db_manager import DatabaseManager
from vacancy_manager import VacancyManager, Vacancy
from query_manager import DBManager
import time


def example_1_api_usage() -> None:
    """
    Пример 1: Работа с API hh.ru
    Показывает, как получить информацию о компании и её вакансиях.
    """
    print("\n" + "=" * 60)
    print("ПРИМЕР 1: Работа с API hh.ru")
    print("=" * 60)

    api = HeadHunterAPI()

    # Получаем информацию о компании Яндекс (ID: 1122242)
    print("\n1. Получение информации о компании...")
    company_id = 1122242
    company_info = api.get_employer_info(company_id)

    if company_info:
        print(f"Компания: {company_info.get('name')}")
        print(f"Сайт: {company_info.get('site_url')}")
        print(f"Открытых вакансий: {company_info.get('open_vacancies')}")

    # Получаем вакансии компании
    print("\n2. Получение вакансий компании...")
    vacancies_data = api.get_employer_vacancies(company_id, page=0, per_page=10)

    if vacancies_data:
        vacancies_list = vacancies_data.get("items", [])
        print(f"Найдено вакансий на странице: {len(vacancies_list)}")
        print(f"Всего вакансий: {vacancies_data.get('found')}")

        # Показываем первые 3 вакансии
        for vacancy in vacancies_list[:3]:
            print(f"\n  • {vacancy.get('name')}")
            print(f"    ID: {vacancy.get('id')}")
            print(f"    Работодатель: {vacancy.get('employer', {}).get('name')}")

    time.sleep(0.5)  # Уважаем API


def example_2_vacancy_manager() -> None:
    """
    Пример 2: Работа с менеджером вакансий
    Показывает парсинг и фильтрацию вакансий.
    """
    print("\n" + "=" * 60)
    print("ПРИМЕР 2: Парсинг и фильтрация вакансий")
    print("=" * 60)

    api = HeadHunterAPI()

    # Получаем вакансии
    print("\n1. Получение вакансий из API...")
    vacancies_data = api.get_employer_vacancies(3529, page=0, per_page=20)

    if vacancies_data:
        # Парсим в объекты Vacancy
        print("2. Преобразование данных в объекты Vacancy...")
        vacancies = VacancyManager.extract_vacancies(vacancies_data.get("items", []))
        print(f"Успешно обработано: {len(vacancies)} вакансий")

        # Показываем информацию о вакансиях
        print("\n3. Информация о вакансиях:")
        for vacancy in vacancies[:3]:
            print(f"\n  • {vacancy.name}")
            print(
                f"    Зарплата: {vacancy.salary_from} - {vacancy.salary_to} {vacancy.currency}"
            )
            print(f"    Опыт: {vacancy.experience}")
            print(f"    Область: {vacancy.area}")

        # Фильтруем по ключевому слову
        print("\n4. Фильтрация по ключевому слову 'Python'...")
        python_vacancies = VacancyManager.filter_by_keyword(vacancies, "Python")
        print(f"Найдено вакансий: {len(python_vacancies)}")

    time.sleep(0.5)


def example_3_database_operations() -> None:
    """
    Пример 3: Операции с базой данных
    Показывает создание БД, таблиц и вставку данных.
    """
    print("\n" + "=" * 60)
    print("ПРИМЕР 3: Операции с базой данных")
    print("=" * 60)

    db = DatabaseManager()

    # Создание БД
    print("\n1. Создание/проверка существования БД...")
    if db.create_database():
        print("✓ БД готова к использованию")

    # Создание таблиц
    print("\n2. Создание таблиц...")
    if db.create_tables():
        print("✓ Таблицы созданы успешно")

    # Вставка тестовых данных
    print("\n3. Вставка тестовых данных...")
    db_manager = DBManager()

    # Добавляем тестовую компанию
    test_company = {
        "id": 999999,
        "name": "Тестовая Компания",
        "site": "https://test.com",
        "vacancies": 5,
    }

    if db_manager.insert_company(
        test_company["id"],
        test_company["name"],
        test_company["site"],
        test_company["vacancies"],
    ):
        print(f"✓ Компания '{test_company['name']}' добавлена")

    # Добавляем тестовую вакансию
    if db_manager.insert_vacancy(
        vacancy_id=999999,
        company_id=test_company["id"],
        name="Тестовая Python вакансия",
        salary_from=100000,
        salary_to=150000,
        currency="RUB",
        area="Москва",
        experience="1-3 года",
        employment_type="Полная занятость",
        description="Это тестовая вакансия",
        url="https://example.com/vacancy",
        published_at="2024-01-01T00:00:00",
    ):
        print("✓ Вакансия добавлена")


def example_4_queries() -> None:
    """
    Пример 4: Выполнение запросов к БД
    Показывает использование методов DBManager.
    """
    print("\n" + "=" * 60)
    print("ПРИМЕР 4: Запросы к БД")
    print("=" * 60)

    db_manager = DBManager()

    # Получаем компании и количество вакансий
    print("\n1. Компании и количество вакансий:")
    companies = db_manager.get_companies_and_vacancies_count()
    for company_name, vacancy_count in companies[:5]:  # Первые 5
        print(f"   {company_name}: {vacancy_count} вакансий")

    # Средняя зарплата
    print("\n2. Средняя зарплата:")
    avg_salary = db_manager.get_avg_salary()
    if avg_salary:
        print(f"   {avg_salary:.2f} RUB")

    # Вакансии с высокой зарплатой
    print("\n3. Вакансии с зарплатой выше средней:")
    high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    for company, vacancy, sal_from, sal_to, currency, url in high_salary_vacancies[:3]:
        print(f"   • {company} - {vacancy}")
        print(f"     Зарплата: {sal_from} - {sal_to} {currency}")

    # Поиск по ключевому слову
    print("\n4. Поиск вакансий со словом 'Python':")
    python_jobs = db_manager.get_vacancies_with_keyword("Python")
    print(f"   Найдено: {len(python_jobs)} вакансий")
    for company, vacancy, sal_from, sal_to, currency, url in python_jobs[:3]:
        print(f"   • {company} - {vacancy}")


def example_5_full_workflow() -> None:
    """
    Пример 5: Полный рабочий процесс
    Загрузка данных одной компании и их анализ.
    """
    print("\n" + "=" * 60)
    print("ПРИМЕР 5: Полный рабочий процесс")
    print("=" * 60)

    api = HeadHunterAPI()
    db = DatabaseManager()
    db_manager = DBManager()

    company_id = 3529  # 2ГИС

    print("\n1. Получение информации о компании...")
    company_info = api.get_employer_info(company_id)

    if company_info:
        company_name = company_info.get("name")
        print(f"   Компания: {company_name}")

        print("\n2. Получение вакансий...")
        all_vacancies = api.get_all_vacancies_for_employer(company_id)
        print(f"   Получено {len(all_vacancies)} вакансий")

        print("\n3. Парсинг вакансий...")
        vacancies = VacancyManager.extract_vacancies(all_vacancies)
        print(f"   Обработано {len(vacancies)} вакансий")

        print("\n4. Анализ данных:")
        vacancies_with_salary = [v for v in vacancies if v.salary_from or v.salary_to]
        print(f"   Вакансий с информацией о зарплате: {len(vacancies_with_salary)}")

        if vacancies_with_salary:
            salaries = []
            for v in vacancies_with_salary:
                if v.salary_from and v.salary_to:
                    salaries.append((v.salary_from + v.salary_to) / 2)
                elif v.salary_from:
                    salaries.append(v.salary_from)
                elif v.salary_to:
                    salaries.append(v.salary_to)

            if salaries:
                avg = sum(salaries) / len(salaries)
                print(f"   Средняя зарплата: {avg:.2f} RUB")

        print("\n5. Топ 5 вакансий по названию:")
        for vacancy in vacancies[:5]:
            print(f"   • {vacancy.name}")


# ============================================================================
# ЗАПУСК ПРИМЕРОВ
# ============================================================================

if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║        ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ПРОЕКТА                      ║")
    print("╚════════════════════════════════════════════════════════════╝")

    try:
        # Раскомментируйте нужные примеры:

        # example_1_api_usage()
        # example_2_vacancy_manager()
        # example_3_database_operations()
        # example_4_queries()
        # example_5_full_workflow()

        print("\n" + "=" * 60)
        print("Раскомментируйте нужные примеры в коде для их запуска")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Ошибка при выполнении примера: {e}")
        import traceback

        traceback.print_exc()
