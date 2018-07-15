import os


def enVar(name, isOptional=False):
    val = os.getenv(name)
    if val is None:
        if isOptional:
            return "False"
        raise EnvironmentError
    return val


if enVar('EZPRINT_DEBUG') in ["True", "true", "1"]:
    DEBUG = True
elif enVar('EZPRINT_DEBUG') in ["False", "false", "0"]:
    DEBUG = False
else:
    raise ValueError("Invalid value for DEBUG")

SECRET_KEY = enVar("RED_DJANGO_SECRET")
DOMAIN_NAME = "ezprint.littleredlabs.com"
APP_NAME = "EZPrint"
SUPERUSER_ACCESS = enVar("SUPERUSER_ACCESS")
CLIENT_ID = "935053760033-gcc387s8h6corvoa9v2r46jfe3l98efr.apps.googleusercontent.com"


BUCKET_NAME = "ezprint.bucket"


MAX_API_PAGE_SIZE = 100
DEFAULT_API_PAGE_SIZE = 30
