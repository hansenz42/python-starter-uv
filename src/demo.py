from src.common.config import config_manager
from src.common.log import log_manager

# 读取 log_level 配置
log_level = config_manager.get_value('log_level')

# 获取日志
log = log_manager.get_logger('main')

log.debug(f'current log level is {log_level}')