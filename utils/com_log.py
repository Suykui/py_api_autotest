import logging
import os
path  = os.path.abspath(os.path.join(os.path.abspath(__file__), "../.."))
# path = os.path.join(path, "log")
# print(path)
fh = logging.FileHandler(path + '/log/test.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s[%(levelname)s][%(funcName)s]%(message)s')
#logging.basicConfig(level=logging.INFO, format='%(asctime)s[%(levelname)s][%(funcName)s]%(message)s')
fh.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(fh)
logger.setLevel(logging.INFO)