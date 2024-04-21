from rest_framework.response import Response


class CustomResponse(Response):
    @classmethod
    def data_response(cls, data, message, meta=None, status=None):
        response_data = {
            'data': data,
            'message': message,
            'meta': meta
        }
        return cls(data=response_data, status=status)
