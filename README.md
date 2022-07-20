# Парсер документации PEP

## Описание:
Парсит статьи по нововведениям в Python, статусы последних версий со ссылками на документацию, формирование таблицы с количеством PEP в каждом статусе, а так же скачивает документации по последней версии Python.

### Используемые технологии:

[![Python](https://img.shields.io/badge/-Python%203.10.4-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![BeautifulSoup](https://img.shields.io/badge/-BeautifulSoup%204.11.1-464646?style=flat-square)](https://pypi.org/project/beautifulsoup4/)
[![lxml](https://img.shields.io/badge/-lxml%204.9.1-464646?style=flat-square)](https://pypi.org/project/lxml/)
[![PrettyTable](https://img.shields.io/badge/-PrettyTable%203.3.0-464646?style=flat-square)](https://pypi.org/project/prettytable/)
[![requests-cache](https://img.shields.io/badge/-requests_cache%200.9.5-464646?style=flat-square)](https://pypi.org/project/requests-cache/)
[![tqdm](https://img.shields.io/badge/-tqdm%204.64.0-464646?style=flat-square)](https://pypi.org/project/tqdm/)

### Как запустить проект:

- Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/DD477/bs4_parser_pep
```
```
cd bs4_parser_pep
```

- Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```
```
source venv/bin/activate
```

- Обновить менеджер пакетов (pip) 

```
python3 -m pip install --upgrade pip
```


- Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Режимы работы парсера:
1. ```python main.py whats-new``` — Парсер статей по нововведениям в Python;
2. ```python main.py latest-versions``` — Статусы последних версий со ссылками на документацию;
3. ```python main.py download``` — Скачивание документации по последней версии Python;
4. ```python main.py pep``` — Формирование таблицы с количеством PEP по статусам.


### Запуск парсера:
```
main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}
Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

### Автор:

- [Dmitrii Dobrodeev](https://github.com/DD477)

### Лицензия:
- MIT
