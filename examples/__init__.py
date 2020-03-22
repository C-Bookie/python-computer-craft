# wget http://127.0.0.1:8080/ py
from .hello import program as hello
from .dig import dig
from .test import test

__all__ = (hello, dig, test)
