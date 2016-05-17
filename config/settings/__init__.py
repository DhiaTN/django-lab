from .base import get_env_variable


env = get_env_variable('DJANGO_ENV', 'development')
try:
	if env == 'development':
		from .dev import *
	elif env == 'production':
		from .prod import *
except ImportError as e:
	print("{0} settings file is missing!".format(env))
	raise e