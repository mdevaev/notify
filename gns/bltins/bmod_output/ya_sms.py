import urllib.request
import urllib.parse
import urllib.error

import logging

from ulib import validators
import ulib.validators.common # pylint: disable=W0611

from raava import worker

from . import common
from ... import env


##### Public constants #####
S_SMS    = "sms"

O_SEND_URL = "send-url"
O_CC       = "cc"


###
CONFIG_MAP = {
    common.S_OUTPUT: {
        S_SMS: {
            O_SEND_URL: ("http://example.com", str),
        },
    },
}


##### Private objects #####
_logger = logging.getLogger(common.LOGGER_NAME)


##### Private methods #####
def _send_raw(task, to, body):
    to = validators.common.validStringList(to)

    request = urllib.request.Request(
        env.get_config(common.S_OUTPUT, S_SMS, O_SEND_URL),
        data=urllib.parse.urlencode({
                "resps": ",".join(to),
                "msg":   body,
            }).encode(),
        )
    opener = urllib.request.build_opener()
    _logger.debug("Sending to Golem SMS API: %s", to)

    task.checkpoint()
    if not env.get_config(common.S_OUTPUT, common.O_NOOP):
        try:
            result = opener.open(request).read().decode().strip()
            _logger.info("SMS sent to Golem to %s, response: %s", to, result)
        except urllib.error.HTTPError as err:
            result = err.read().decode().strip()
            _logger.exception("Failed to send SMS to %s, response: %s", to, result)
        except Exception:
            _logger.exception("Failed to send SMS to %s", to)
    else:
        _logger.info("SMS sent to Golem (noop) to %s", to)
    task.checkpoint()


##### Private classes #####
class _Sms:
    send_raw = worker.make_task_builtin(_send_raw)


##### Public constants #####
BUILTINS_MAP = {
    "sms": _Sms,
}
