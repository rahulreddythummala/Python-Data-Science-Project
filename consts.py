import os

_DB_NAME = "db.json"
_ROOT_DB_NAME = "Mark_Twain_Database/"
_APP_DATA_DIR = os.environ['LOCALAPPDATA'].replace('\\', '/') + "/"
ROOT_DB_DIR = _APP_DATA_DIR + _ROOT_DB_NAME
BOOKS_DIR = ROOT_DB_DIR + "books/"
DB_PATH = ROOT_DB_DIR + _DB_NAME
TABLE_BOOKS = "Books"
TABLE_BLOCKS = "Blocks"

CSV_1 = "cities_1851.csv"
CSV_2 = "cities_1878.csv"

SURROUND_WORD_COUNT = 200


TITLE = "title"
CREATOR = "creator"
DATE = "date"
PUBLISHER = "publisher"
SOURCE = "source"
IDENTIFIER = "identifier"
TYPE = "type"
FORMAT = "format"
GENRE = "genre"
PERIOD = "period"
THEME = "theme"
GENDER = "gender"
PATH = "path"
URL = "url"
