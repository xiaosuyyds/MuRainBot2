import os

WORK_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(WORK_PATH, "data")
LOGS_PATH = os.path.join(WORK_PATH, "logs")
PLUGINS_PATH = os.path.join(WORK_PATH, "plugins")
CONFIG_PATH = os.path.join(WORK_PATH, "config.yml")
