import os
from constructs import Construct
from abc import ABC, abstractmethod
from enum import Enum
from .utils import snake_case, kebab_case, camel_case, pascal_case


class PathStrFormat(Enum):
    SNAKE_CASE = lambda s: snake_case(s)
    KEBAB_CASE = lambda s: kebab_case(s)
    CAMEL_CASE = lambda s: camel_case(s)
    PASCAL_CASE = lambda s: pascal_case(s)
    SHOUTED_SNAKE_CASE = lambda s: snake_case(s).upper()


class Resource(ABC):
    scope: Construct
    env: object
    store_path_prefix: str

    def __init__(self, scope: Construct, env: object):
        self.scope = scope
        self.env = env
        self.store_path_prefix = self.get_path_str_format()(env.APP_NAME)

    @abstractmethod
    def get_path_str_format(self) -> PathStrFormat:
        pass
