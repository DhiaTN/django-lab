import logging


class ConsoleLogger(object):
    log_levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']

    def __call__(self, name, log_level='debug'):
        if not log_level.upper() in self.log_levels:
            raise ValueError("Invalid logging level.")

        log_level = getattr(logging, log_level.upper())

        # create logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)

        # create console handler
        handler = logging.StreamHandler()
        handler.setLevel(log_level)

        # create formatter
        output_pattern = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(output_pattern)
        handler.setFormatter(formatter)

        # add handler to logger
        logger.addHandler(handler)
        return logger


getLogger = ConsoleLogger()
