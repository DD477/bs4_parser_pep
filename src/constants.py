from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
EXPECTED_STATUS = {
    'A': ['Active', 'Accepted'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn'],
    '': ['Draft', 'Active'],
}
WHATS_NEW_RESULT = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
LASTEST_VERSIONS_RESULT = [('Ссылка на документацию', 'Версия', 'Статус')]
PEP_RESULT = [('Статус', 'Количество')]
RE_PATTERN = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
