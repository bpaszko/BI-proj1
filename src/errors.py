class ConfigError(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MissingOptionError(ConfigError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OptionTypeError(ConfigError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OptionValueError(ConfigError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidSeqLengthError(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
