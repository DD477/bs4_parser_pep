import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS, LASTEST_VERSIONS_RESULT,
                       MAIN_DOC_URL, MAIN_PEP_URL, PEP_RESULT, RE_PATTERN,
                       WHATS_NEW_RESULT)
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        return None
    soup = BeautifulSoup(response.text, features='lxml')

    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})

    div_with_ul = find_tag(
        main_div, 'div', attrs={'class': 'toctree-wrapper'}
    )

    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'})

    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        WHATS_NEW_RESULT.append(
            (version_link, h1.text, dl_text)
        )

    return WHATS_NEW_RESULT


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Ничего не нашлось')

    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(RE_PATTERN, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        LASTEST_VERSIONS_RESULT.append(
            (link, version, status)
        )
    return LASTEST_VERSIONS_RESULT


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return None
    soup = BeautifulSoup(response.text, features='lxml')
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    archive_url = urljoin(downloads_url, pdf_a4_tag['href'])
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)

    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    def get_page_status(link):
        response = get_response(session, link)
        if response is None:
            return None
        soup = BeautifulSoup(response.text, features='lxml')
        dl = find_tag(soup, 'dl')

        return find_tag(
            dl, tag='', string='Status'
        ).parent.find_next_sibling().text

    def check_pep_status(table_status, page_status, link):
        if page_status not in EXPECTED_STATUS[table_status]:
            logging.info(
                '\n'
                'Несовпадающие статусы:\n'
                f'{link}\n'
                f'Статус в карточке: {page_status}\n'
                f'Ожидаемые статусы: {EXPECTED_STATUS[table_status]}'
            )

    response = get_response(session, MAIN_PEP_URL)
    if response is None:
        return None
    soup = BeautifulSoup(response.text, features='lxml')
    numerical_index = find_tag(
        soup, 'section', attrs={'id': 'numerical-index'}
    )
    tbody = find_tag(numerical_index, 'tbody')
    tr = tbody.find_all('tr')
    statuses_per_type = defaultdict(int)

    for item in tqdm(tr):
        td = find_tag(item, 'td')
        table_status = td.text[1:]
        link = urljoin(MAIN_PEP_URL, td.find_next_sibling().a['href'])
        page_status = get_page_status(link)
        check_pep_status(table_status, page_status, link)
        statuses_per_type[page_status] += 1

    PEP_RESULT.extend(
        [(status, statuses_per_type[status]) for status in statuses_per_type]
    )
    PEP_RESULT.append(('Total', sum(statuses_per_type.values())))

    return PEP_RESULT


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
