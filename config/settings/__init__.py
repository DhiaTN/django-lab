from .base import get_env_variable


env = get_env_variable('DJANGO_ENV', 'development')
try:
	if env == 'development':
		from .dev import *
	elif env == 'production':
		from .prod import *
	else:
		err_msg = "Expected DJANGO_ENV value: [development, production],  <{0}> found."
		raise ValueError(err_msg.format(env))
	# reset loggers level
	for logger in LOGGING['loggers']:
		LOGGING['loggers'][logger].update({
			'level': LOGGING_LEVEL
		})
except ImportError as e:
	print("{0} settings file is missing!".format(env))
	raise e