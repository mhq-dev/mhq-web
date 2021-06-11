import requests


class BadRequestException(Exception):
    def __init__(self, message=''):
        self.message = message


def get_key_value_dict(key_values):
    kv_dict = dict()
    for kv in key_values:
        kv_dict[kv.key] = kv.value
    return kv_dict


class RequestExecution:

    def __init__(self, request):
        self.request = request

    def get(self):

        return requests.get(self.request.url,
                            headers=get_key_value_dict(self.request.get_enabled_headers()),
                            params=get_key_value_dict(self.request.get_enabled_params())
                            )

    def post(self):
        return requests.post(self.request.url,
                             json=self.request.body,
                             headers=get_key_value_dict(self.request.get_enabled_headers())
                             )

    def put(self):
        return requests.put(self.request.url,
                            data=self.request.body,
                            headers=get_key_value_dict(self.request.get_enabled_headers())
                            )

    def delete(self):
        return requests.delete(self.request.url,
                               headers=get_key_value_dict(self.request.get_enabled_headers())
                               )

    def execute(self):
        method_types = {'get': self.get, 'post': self.post, 'put': self.put, 'delete': self.delete}

        try:
            result = method_types[self.request.http_method]()
        except Exception as e:
            raise BadRequestException(message=str(e))

        try:
            result_body = result.json()
        except ValueError:
            result_body = result.text

        return {
            "status": result.status_code,
            "headers": dict(result.headers),
            "cookies": dict(result.cookies),
            "body": result_body,
        }
