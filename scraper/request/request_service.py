from fake_useragent import UserAgent
import requests
import os

class RequestService:
    class RequestException(Exception):
        def __init__(self, method, url, headers, params, response, status_code):
            self.method = method
            self.url = url
            self.headers = headers
            self.params = params
            self.response = response
            self.status_code = status_code
            message =\
                f"Error sending request: {method} {url} returned {status_code}.\n" \
                f"Headers: {headers}\n" \
                f"Params: {params}\n" \
                f"Response: {response}\n"
            super().__init__(message)

    class BadRequestException(RequestException):
        def __init__(self, method, url, headers, params, response):
            super().__init__(method, url, headers, params, response, 400)

    class UnauthorizedException(RequestException):
        def __init__(self, method, url, headers, params, response):
            super().__init__(method, url, headers, params, response, 401)

    class RecordNotFoundException(RequestException):
        def __init__(self, method, url, headers, params, response):
            super().__init__(method, url, headers, params, response, 404)

    class InternalServerException(RequestException):
        def __init__(self, method, url, headers, params, response):
            super().__init__(method, url, headers, params, response, 500)

    class BadGatewayException(RequestException):
        def __init__(self, method, url, headers, params, response):
            super().__init__(method, url, headers, params, response, 502)

    class GatewayTimeoutException(RequestException):
        def __init__(self, method, url, headers, params, response):
            super().__init__(method, url, headers, params, response, 504)

    ERROR_CODE_MAP = {
        400: BadRequestException,
        401: UnauthorizedException,
        403: None,
        404: RecordNotFoundException,
        422: None,
        500: InternalServerException,
        502: BadGatewayException,
        504: GatewayTimeoutException
    }

    def __init__(self):
        self.user_agent_generator = UserAgent()

    def build_headers(self):
        headers = {
            'Connection': 'close',
            'accept-encoding': 'gzip, deflate',
            'User-Agent': self.user_agent_generator.random
        }
        return headers

    def get_proxies(self):
        username = os.getenv("PROXY_AUTH_USERNAME")
        password = os.getenv("PROXY_AUTH_PASSWORD")
        proxy_url = os.getenv("PROXY_URL")
        proxy_port = os.getenv("PROXY_PORT")
        proxies = {
            'http': f'http://{username}:{password}@{proxy_url}:{proxy_port}',
            'https': f'http://{username}:{password}@{proxy_url}:{proxy_port}'
        }
        return proxies

    def send_request(self, method, url, params = None):
        session = requests.Session()
        headers = session.headers = self.build_headers()
        session.proxies = self.get_proxies()

        functor = RequestService.get_request_method_functor(session, method)

        # Send the request

        print(f"Sending request to {url}")
        print(f"Params: {params}")

        response = functor(url, params=params, verify=False)

        status_code = response.status_code
        if status_code >= 400:
            error = RequestService.ERROR_CODE_MAP[status_code]
            raise error(method, url, headers, params, response.text)
        else:
            return response.text

    @staticmethod
    def get_request_method_functor(session, http_method):
        functor_name = http_method.value
        functor = getattr(session, functor_name)
        return functor
