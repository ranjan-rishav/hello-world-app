import logging
_logger = logging.getLogger('src')

_logger.setLevel(logging.DEBUG)
log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d]: %(message)s')
sh = logging.StreamHandler()
fh = logging.FileHandler("src.log",mode='a')
sh.setLevel(logging.INFO)
fh.setLevel(logging.DEBUG)
sh.setFormatter(log_format)
fh.setFormatter(log_format)
_logger.addHandler(sh)
_logger.addHandler(fh)