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
"""
def validate_friends_params(params):
    errors = []
    validated = {}
    eye_color_values = ['brown', 'blue']
    if 'eye_color' in params && params['eye_color'] not in eye_color_values:
        errors.append('eye_color should be from %s' % eye_color_values)
    else:
        validated['eye_color'] = params['eye_color']

    if 'has_died' in params && lower(params['has_died']) not in ['true', 'false']
        errors.append('has_died should be a boolean')
    else:
        validated['has_died'] = lower(params['has_died']) == 'true'

    if len(errors) > 0:
        raise BusinessException('Some filters are not valid', errors)
"""

