from flask import Flask
from requests import get

app = Flask(__name__)


class ServiceDTO:
    def __init__(self, service_host, action_route, ready_route, protocol="http", port=""):
        self.action_url = self.get_full_url(
            protocol, service_host, action_route, port
        )
        self.ready_url = self.get_full_url(
            protocol, service_host, ready_route, port
        )

    def get_full_url(self, protocol, host, route, port):
        return "%s://%s/%s" % (protocol, host, route) if not port else "%s://%s:%s/%s" % (protocol, host, port, route)


QUOTES_SERVICE = ServiceDTO('lotr-quotes', 'quote', 'ready', port="8080")


def check_service_ready(service):
    url = service.ready_url
    app.logger.info('Fetching: %s' % url)
    result = get(url)
    ready = (result.json()).get('ready', False)
    return ready


@app.route('/')
def start():
    try:
        ready = check_service_ready(QUOTES_SERVICE)
        if ready:
            return 'Already active!'
        else:
            return 'Starting...'
    except:
        return 'Big problem!'
