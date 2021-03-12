import uuid

import xlwings as xw
from xlwings.conversion import Converter


class ObjectConverter(Converter):
    cache = {}

    @staticmethod
    def read_value(value, options):
        return ObjectConverter.cache[value]

    @staticmethod
    def write_value(value, options):
        unique = str(uuid.uuid4())
        ObjectConverter.cache[unique] = value
        # TODO: objects are never deleted
        # it would be nice to have access to the caller
        return unique


class SomeObject:
    def __init__(self, value: float):
        self.value = value

    def get(self, exponent: float) -> float:
        return self.value ** exponent


@xw.func
@xw.ret(convert=ObjectConverter)
def create_f(value: float) -> SomeObject:
    return SomeObject(value)


@xw.func
@xw.arg('some_object', convert=ObjectConverter)
def get_f(some_object: SomeObject, exponent: float) -> float:
    return some_object.get(exponent)


if __name__ == "__main__":
    xw.serve()
