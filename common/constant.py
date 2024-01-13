import os
import re
import time
import logging

# -----PATH-----
BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR    = os.path.join(BASE_DIR, "template")
LOG_DIR         = os.path.join(BASE_DIR, "logs")
SCRIPTS_DIR     = os.path.join(BASE_DIR, "scripts")
OUTPUT_DIR      = os.path.join(BASE_DIR, "output")
COMMON_DIR      = os.path.join(BASE_DIR, "common")
INPUT_DIR       = os.path.join(BASE_DIR, "input")
# -----CONFIG-----
CMD_RETRY_TIME = 1
# -----PATTERN-----
IP_PATTERN = re.compile(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
TIME_PATTERN = {
    "default": "%Y%m%d%H%M%S",
    "text": "%Y-%m-%d %H:%M:%S",
    "textf": "%Y-%m-%d %H:%M:%S.%f",
    "timestamp": "%Y-%m-%d-%H:%M:%S",
    "timestampf": "%Y-%m-%d-%H:%M:%S.%f"
}
FIELD_PREFIX = ["min", "max", "avg"]
# -----LOGGER-----
LOG_PATH        = os.path.join(LOG_DIR, "log.txt")
TIMESTAMP = time.strftime(TIME_PATTERN["timestamp"], time.localtime(time.time()))
# critical > error > warning > info > debug
LOGGER_NAME = "basic_logger"
LOG_LEVEL = logging.INFO
LOG_FORMATTER = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s', TIME_PATTERN["text"])
LOGGER = logging.getLogger(LOGGER_NAME)
LOGGER.setLevel(LOG_LEVEL)
FH = logging.FileHandler(LOG_PATH, encoding="utf-8")
FH.setLevel(LOG_LEVEL)
FH.setFormatter(LOG_FORMATTER)
LOGGER.addHandler(FH)
SH = logging.StreamHandler()
SH.setLevel(LOG_LEVEL)
SH.setFormatter(LOG_FORMATTER)
LOGGER.addHandler(SH)
# -----CONSTANT-----
BYTES_TO_GIGA = 1024 * 1024 * 1024
BITS_TO_GIGA = BYTES_TO_GIGA * 8
YAML_SPLIT = "----------"