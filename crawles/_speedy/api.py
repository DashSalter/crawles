from .Response import Response
from functools import partial
from io import BytesIO
from typing import Callable, Dict, Optional, Tuple, Union, List
from http.cookiejar import CookieJar

from curl_cffi.const import CurlHttpVersion
from curl_cffi.requests.headers import HeaderTypes
from curl_cffi.requests.session import BrowserType, Session
from .MetaSession import my_session

CookieTypes = Union[
    "Cookies", CookieJar, Dict[str, str], List[Tuple[str, str]]
]


def decorator(func):
    def inner(*args, **kwargs):
        response_ = func(*args, **kwargs)

        response = Response(response_)  # 创建新对象
        response.__dict__.update(response_.__dict__)  # 从原始数据更新到新对象
        return response

    return inner


impersonate_list = ['chrome99',
                    'chrome100',
                    'chrome101',
                    'chrome104',
                    'chrome107',
                    'chrome110',
                    'chrome99_android',
                    'edge99',
                    'edge101',
                    'safari15_3',
                    'safari15_5']


@decorator
def request(
        method: str,
        url: str,
        params: Optional[dict] = None,
        data: Optional[Union[Dict[str, str], str, BytesIO, bytes]] = None,
        json: Optional[dict] = None,
        headers: Optional[HeaderTypes] = None,
        cookies: Optional[CookieTypes] = None,
        files: Optional[Dict] = None,
        auth: Optional[Tuple[str, str]] = None,
        timeout: Union[float, Tuple[float, float]] = 30,
        allow_redirects: bool = True,
        max_redirects: int = -1,
        proxies: Optional[dict] = None,
        verify: Optional[bool] = None,
        referer: Optional[str] = None,
        accept_encoding: Optional[str] = "gzip, deflate, br",
        content_callback: Optional[Callable] = None,
        impersonate: Optional[Union[str, BrowserType]] = None,
        thread: Optional[str] = None,
        default_headers: Optional[bool] = None,
        curl_options: Optional[dict] = None,
        http_version: Optional[CurlHttpVersion] = None,
        debug: bool = False,
        interface: Optional[str] = None,
) -> Response:
    if impersonate and impersonate not in impersonate_list:
        raise ValueError(f'The parameter is incorrect, it should be {impersonate_list}')

    with Session(thread=thread, curl_options=curl_options, debug=debug) as s:
        return s.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            max_redirects=max_redirects,
            proxies=proxies,
            verify=verify,
            referer=referer,
            accept_encoding=accept_encoding,
            content_callback=content_callback,
            impersonate=impersonate,
            default_headers=default_headers,
            http_version=http_version,
            interface=interface,
        )


head = partial(request, "HEAD")
get = partial(request, "GET")
post = partial(request, "POST")
put = partial(request, "PUT")
patch = partial(request, "PATCH")
delete = partial(request, "DELETE")
options = partial(request, "OPTIONS")


@decorator
def session_get(url, params=None, headers=None, **kwargs):
    """session的get请求"""
    return my_session.meta_session('GET', url, params=params, headers=headers, **kwargs)


@decorator
def session_post(url, data=None, headers=None, **kwargs):
    """session的post请求"""
    return my_session.meta_session('POST', url, data=data, headers=headers, **kwargs)
