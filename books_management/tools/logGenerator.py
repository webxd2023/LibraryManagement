import logging

def ret_logger(logFilePath):
    print(logFilePath)
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    formator = logging.Formatter(fmt="%(asctime)s [ %(filename)s ] %(lineno)d行 | [ %(levelname)s ] | [ %(message)s ]", datefmt = "%Y-%m-%d-%X")
    sh = logging.StreamHandler()
    fh = logging.FileHandler(logFilePath,encoding="utf-8")
    logger.addHandler(sh)
    sh.setFormatter(formator)
    logger.addHandler(fh)
    fh.setFormatter(formator)
    return logger
