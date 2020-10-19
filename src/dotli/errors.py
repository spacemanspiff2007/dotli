import typing


class DotliException(Exception):
    _msg_template: str

    def __init__(self, stack: tuple, value: typing.Any, *args, **kwargs):
        super().__init__(*args)

        self.stack = stack
        self.value = value
        self.ctx = kwargs

    def __str__(self):
        return self._msg_template.format(value=self.value, stack=self.stack, **self.ctx) + f' @ {".".join(self.stack)}'


class KeyNotAStringError(DotliException):
    _msg_template = 'Key "{value}" ({value_type}) is not a string!'


class IncompleteListError(DotliException):
    _msg_template = 'No entry for index "{value}" in list!'


class SeparatorInKeyError(DotliException):
    _msg_template = 'Separator "{separator}" is in key "{value}"!'

    def __init__(self, stack: tuple, value: typing.Any, separator: str, *args, **kwargs):
        super().__init__(stack, value, *args, separator=separator, **kwargs)


class KeyAlreadyExistsError(DotliException):
    _msg_template = 'Key "{value}" does already exist!'
