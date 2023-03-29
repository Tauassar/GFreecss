import logging.config

from .api import API
from .exceptions import DuplicateRoute
from .exceptions import HTTPException
from .exceptions import MethodNotAllowed


from customFramework.settings import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
