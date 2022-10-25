import os
import sys
import urllib.request
import zipfile
import requests
URL = "https://pypi.org/simple/"  # Ссылка на pypi, откуда берутся пакеты (в глобальном доступе для программы)
list_of_dependency = {}
# Функция для нахождения ссылки для скачивания
def get_url(content):
    content = content.replace(" ", '\n').split('\n')
    ans = ""
    for i in range(len(content)):
        if ("href=" in content[-1 - i]) and ("whl" in content[-1 - i]):
            ans = content[-1 - i]
            break
    return ans.replace("href=", "")[1:-1]
# Ищем метаданные
def find_meta(dirlist):
    for elem in dirlist:
        if "METADATA" in elem:
            return elem
    return None
# Достаём зависимости
def get_dependencies(lines):
    ans = []
    for elem in lines:
        if ("requires-dist" in elem.lower()) and ("python" not in elem.lower()) and ("extra" not in elem.lower()):
            temp = elem.split()
            for i in range(len(temp)):
                if "requires-dist" in temp[i].lower():
                    ans.append(temp[i + 1])
                    break
    return ans
def add(name, dependency):
    list_of_dependency[name]=dependency
    print(name," -> ", dependency)
# Основная функция
def main1(package_name):
    # Получение ссылки на скачивание пакета
    response = requests.get(URL + package_name + '/')
    url_to_download = get_url(response.content.decode("UTF-8"))
    try:
        # Пробуем скачать пакет
        urllib.request.urlretrieve(url_to_download, package_name + ".zip")
    except ValueError:  # Если скачивание не получается
        print("Package name is invalid")
        sys.exit()
    file = zipfile.ZipFile(package_name + ".zip", 'r')  # Считываем данные из архива
    metadata = file.open(find_meta(file.namelist()), 'r')  # Ищем файл метаданных и открываем его
    text = metadata.readlines()  # Считываем данные
    text = list(i.decode("UTF-8") for i in text)  # Перекодировка в UTF-8
    dependencies = get_dependencies(text)  # Достаём все зависимости
    for dependency in dependencies:
        add(package_name, main1(dependency))
    # Закрываем и удаляем
    metadata.close()
    file.close()
    os.remove(package_name + ".zip")
    return package_name
if __name__ == '__main__':
    n = input("Введите имя пакета: ")
    res = main1(n) # Вызов основной функции
