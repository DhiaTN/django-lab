import logging


class ConsoleLogger(object):

    log_levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']

    def __call__(self, name, log_level='debug', formatter=None):

        if not log_level.upper() in self.log_levels:
            raise ValueError("Invalid logging level.")

        # create logger
        logger = logging.getLogger(name)

        # set logging Level
        log_level = getattr(logging, log_level.upper())
        logger.setLevel(log_level)

        # create console handler
        handler = logging.StreamHandler()
        handler.setLevel(log_level)

        # create formatter
        if formatter:
            formatter_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(formatter_format)
            handler.setFormatter(formatter)

        # add handler to logger
        logger.addHandler(handler)
        return logger


getLogger = ConsoleLogger()