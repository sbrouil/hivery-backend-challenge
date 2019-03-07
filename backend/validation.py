import uuid
from backend.exceptions import BusinessException

def UUID(value):
    return uuid.UUID(value)

def validate_person(person):
    if 'guid' in person:
        try:
            uuid.UUID(person['guid'])
        except ValueError as e:
            raise BusinessException('The given UUID is invalid: %s' % e)