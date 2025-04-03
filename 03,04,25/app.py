from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
import csv 
import time 
from webdriver_manager.chrome import ChromeDriverManager  # Импорт для автоматической установки ChromeDriver

# Устанавливаем ChromeDriver с помощью webdriver_manager
driver = webdriver.Chrome(ChromeDriverManager().install())

try: 
    # Открываем страницу
    driver.get('https://www.kinopoisk.ru/lists/movies/movies-in-cinema/') 
    time.sleep(5)  # Ждем загрузки страницы 

    # Ожидаем, пока пользователь пройдет CAPTCHA 
    input("Пройдите CAPTCHA вручную и нажмите Enter, чтобы продолжить...") 

    # Обходим окно с куки 
    try: 
        cookie_button = driver.find_element(By.XPATH, '//button[contains(text(), "Принять")]') 
        cookie_button.click() 
        print("Куки приняты.") 
    except Exception as e: 
        print("Окно с куки не найдено или уже закрыто.") 

    # Находим элементы фильмов
    movies = driver.find_elements(By.CLASS_NAME, 'base-movie-main-info_link__YwtP1')[:10] 
    movie_data = [] 

    for movie in movies: 
        try: 
            title = movie.find_element(By.CLASS_NAME, 'styles_mainTitle__IFQyZ').text 
            additional_info = movie.find_element(By.CLASS_NAME, 'desktop-list-main-info_additionalInfo__Hqzof').text 
            country, author = additional_info.split('•')[0].strip(), additional_info.split('Режиссёр: ')[1].strip() 
            premiere_date = movie.find_element(By.CLASS_NAME, 'desktop-list-main-info_secondaryText__M_aus').text.split(',')[1].strip() 

            movie_data.append({ 
                'Название': title, 
                'Автор': author, 
                'Страна': country, 
                'Дата премьеры': premiere_date 
            }) 
        except Exception as e: 
            print(f"Ошибка при обработке фильма: {e}") 

    # Сохраняем данные в CSV-файл
    with open('movies.csv', 'w', newline='', encoding='utf-8') as csvfile: 
        fieldnames = ['Название', 'Автор', 'Страна', 'Дата премьеры'] 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 

        writer.writeheader() 
        writer.writerows(movie_data) 

    print("Данные успешно сохранены в файл movies.csv") 
finally: 
    driver.quit()
