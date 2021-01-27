import random, time, pickle, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

from application import conf

options = webdriver.ChromeOptions()
options.headless = True

# User agent
user_agent = UserAgent()
options.add_argument(f'user-agent={user_agent.random}')

# disable web-driver
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(
    executable_path='',  # TODO: Указать абсолютный путь к файлу.
    # Драйвер chrome, скачать по ссылке: https://chromedriver.storage.googleapis.com/index.html.
    # Разархировать и положить в каталог .
    options=options
)

try:
    continue_and_exit = True
    driver.get(url='https://vk.com/')
    driver.implicitly_wait(3)

    # Осуществляет проверку cookie файла. При отсутствии вход и создание файла cookie.
    if not (os.path.exists(f'{conf.telephone}_cookie')):  # Файл cookie не существет.
        index_email = driver.find_element_by_id('index_email')
        index_email.send_keys(conf.telephone)
        driver.implicitly_wait(1)
        index_pass = driver.find_element_by_id('index_pass')
        index_pass.send_keys(conf.password)
        driver.implicitly_wait(1)
        index_pass.send_keys(Keys.ENTER)
        driver.implicitly_wait(1)
        pickle.dump(driver.get_cookies(), open(f'{conf.telephone}_cookie', 'wb'))
    else:  # Файл cookie существет.
        for cookie in pickle.load(open(f'{conf.telephone}_cookie', 'rb')):
            driver.add_cookie(cookie)
        driver.implicitly_wait(1)
        driver.refresh()
        driver.implicitly_wait(5)

    # Осуществляет переход по ссылке к музыке пользователя.
    l_aud = driver.find_element_by_id('l_aud')
    l_aud = l_aud.find_element_by_class_name('left_row')
    href_aud = l_aud.get_attribute('href')
    href_my_aud = str(href_aud) + '?section=all'
    driver.get(url=href_my_aud)
    driver.implicitly_wait(3)
    list_music = driver.find_elements_by_class_name('audio_row')
    list_music_length = len(list_music)

    while continue_and_exit != 'q':
        # Получает рандомную музыку из плейлиста, и воспроизводит ее.
        random_music = random.randint(0, list_music_length)
        music = list_music[random_music]
        driver.implicitly_wait(6)
        music.click()  # Воспроизводит музыку.
        time.sleep(25)  # Воспроизводит музыку в течении 25 секунд.
        music.click()  # Останавливает музыку
        driver.implicitly_wait(6)

        # Получает исполнителя музыки.
        music_executor = music.find_element_by_class_name('audio_row__performers')
        music_executor = music_executor.find_element_by_css_selector('a').text

        # Получает название музыки.
        music_title = music.find_element_by_class_name('audio_row__title_inner').text

        print('\n\n-------Угадайте музыку-------')
        input('И нажмите на любую клавишу для получения исполнителя и названия музыки...')
        print('Исполнитель: ', music_executor)
        print('Музыка: ', music_title)
        continue_and_exit = input(
            '\nДля продолжения и получения следующей композиции нажмите любую клавишу... Для выхода нажмите q : '
        )
        if continue_and_exit == '':
            continue_and_exit = True

except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()
