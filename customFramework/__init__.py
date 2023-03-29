import logging.config

from customFramework.api import API

from customFramework.settings import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
