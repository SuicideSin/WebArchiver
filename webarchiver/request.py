"""Method for requesting web pages."""
import logging
import time

import requests

logger = logging.getLogger(__name__)


def get(url, status_codes=[200], content_length=0, max_tries=1,
        headers=None, cookies=None, preserve_url=False, stream=False,
        sleep_time=5, session=None):
    """GETs an URL.

    Uses a GET request for an URL. The response undergoes undergoes a number of
    checks detailed in the `Args` list below.

    Args:
        url: The URL to download using GET.
        status_code (list, optional): The list of status codes the response is
            allowed to have. Default is ``[200]``.
        content_length (int, optional): The minimum size of the payload.
            Default is 0.
        max_tries (int, optional): The minimum number of tries in case the
            response is bad. Default is 1.
        headers (dict, optional): The headers to use for the GET request.
            Default is None.
        cookies (dict, optional): The cookies to use for the GET request.
            Default is None.
        preserve_url (bool, optional): Whether a redirect of the request is
            permitted or not. Default is False.
        stream (bool, optional): Whether to make the GET request a stream for
            :mod:`requests`. A stream will return immediatly and allow looping
            over the response while it comes in. Default is False.
        sleep_time (int, optional): The time in seconds to wait between tries.
            Default is 5 seconds.
        session (:obj:`requests.sessions.Session`, optional): The session to
            use for the request. If no session is specified, no session will
            be used. Default is None.

    Returns:
        :obj:`requests.models.Response`: The response of the GET request.
        bool: False if request was not succesful or response was bad.
    """
    tries = 0
    while tries < max_tries:
        try:
            logger.debug('Getting URL %s, try %s.', url, tries)
            response = (session or requests).get(url, headers=headers,
                                                 cookies=cookies,
                                                 stream=stream)
            if not stream:
                if len(response.text) < content_length:
                    logger.warning('Content length URL %s %s < %s.', url,
                                   len(response.text), content_length)
                    assert len(response.text) > content_length
            if response.status_code not in status_codes:
                logger.warning('Status code URL %s %s not in %s.', url,
                               response.status_code, status_codes)
                assert response.status_code in status_codes
            if preserve_url and response.url != url:
                logger.warning('URL %s changed to %s.', url, response.url)
                assert response.url == url
            return response
        except:
            tries += 1
            if tries < max_tries:
                logger.info('Sleeping %s seconds for getting URL %s.',
                            sleep_time, url)
                time.sleep(sleep_time)
    return False

