import logging
import sys

_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

_console = logging.StreamHandler(sys.stdout)
_console.setLevel(logging.WARNING)
_console.setFormatter(_fmt)

_file = logging.FileHandler("logs/app.log")
_file.setLevel(logging.INFO)
_file.setFormatter(_fmt)

logger = logging.getLogger("data_pebbles")
logger.setLevel(logging.DEBUG)
logger.addHandler(_console)
logger.addHandler(_file)
