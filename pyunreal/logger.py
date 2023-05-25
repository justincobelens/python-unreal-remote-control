import logging

logging.getLogger("pyunreal").setLevel(logging.DEBUG)

class UnrealLogging:
    PACKAGE_NAME = "pyunreal"
    DEFAULT_FORMAT = logging.Formatter(
        fmt='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S')
    DEFAULT_LEVEL = logging.CRITICAL

    @classmethod
    def get_logger(cls, name):
        if not name.startswith(cls.PACKAGE_NAME):
            raise RuntimeError("The package logger name should be 'pyunreal.xxx.xxx' but {}".format(name))

        logger = logging.getLogger(name)

        # check if the logger already has handlers attached to it. If not, add a new StreamHandler
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(cls.DEFAULT_FORMAT)
            logger.addHandler(console_handler)
        else:
            logger.handlers[0].setFormatter(cls.DEFAULT_FORMAT)

        return logger

    @classmethod
    def set_default_format(cls, format):
        cls.DEFAULT_FORMAT = format

    @classmethod
    def disable(cls):
        logging.getLogger(cls.PACKAGE_NAME).setLevel(logging.CRITICAL)

    @classmethod
    def enable(cls, level=logging.DEBUG):
        logging.getLogger(cls.PACKAGE_NAME).setLevel(level)

    @classmethod
    def set_level(cls, level):
        """
        Set the logging level.

        The level parameter should be a string that specifies the desired logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL').
        """
        levels = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        logging.getLogger(cls.PACKAGE_NAME).setLevel(levels.get(level.upper(), cls.DEFAULT_LEVEL))

