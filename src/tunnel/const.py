from pathlib import Path
from json import loads
from json_minify import json_minify

ROOT_DIR = Path(__file__).absolute().parent.parent.parent
DATA_DIR = ROOT_DIR / 'data'
SRC_DIR = ROOT_DIR / 'src'
CONFIG = loads(json_minify(open(DATA_DIR / 'config.json', 'r').read()))