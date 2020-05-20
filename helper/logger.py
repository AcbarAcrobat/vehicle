import logging
import colorlog


formatter = colorlog.ColoredFormatter(
    "%(log_color)s[%(levelname).1s] %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL':	'bold_red,bg_white'
    },
    secondary_log_colors={},
    style='%'
)

handler = colorlog.StreamHandler()
handler.setFormatter(formatter)

LOGGER = colorlog.getLogger(__name__)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)
