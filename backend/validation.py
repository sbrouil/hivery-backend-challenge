import uuid
import re
from backend.exceptions import BusinessException

COMPANY_NAME_PATTERN = re.compile('^[A-Z]*$')

def bool_param_type(boolStr):
    return boolStr.lower() == 'true'

def UUID(value):
    return uuid.UUID(value)

def validate_uuid(uuid_str):
    try:
        uuid.UUID(uuid_str)
    except ValueError as e:
        raise BusinessException('The given UUID is invalid: %s' % e)

def validate_company_name(name):
    if not COMPANY_NAME_PATTERN.match(name):
        raise BusinessException('Invalid ompany name format, should only contain uppercase characters')
        