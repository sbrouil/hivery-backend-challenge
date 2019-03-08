"""
Declare some usefull exception that van be catched by the Flask error handler and
transformed into correct REST API error response
"""
class BusinessException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class NotFound(BusinessException):
    def __init__(self, resource_name, resource_id):
        super(NotFound, self).__init__("%s %s not found" % (resource_name, resource_id), 404)