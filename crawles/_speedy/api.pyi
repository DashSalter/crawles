from collections.abc import Mapping
from typing import Any
from typing_extensions import TypeAlias

from .Response import Response
from requests.sessions import (RequestsCookieJar,
                               _Auth, _Cert, _Data, _Files, _HooksInput, _Params,
                               _TextMapping, _Timeout, _Verify)
from typing import Optional, Union

from curl_cffi.requests.session import BrowserType

_HeadersMapping: TypeAlias = Mapping[str, str | bytes]


def request(
        method: str | bytes,
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Any | None = ...,
        impersonate: Optional[Union[str, BrowserType]] = None,
) -> Response: ...


def get(
        url: str | bytes,
        params: _Params | None = ...,
        *,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Any | None = ...,
        impersonate: Optional[Union[str, BrowserType]] = None,
) -> Response: ...


def options(
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Any | None = ...,
        impersonate: Optional[Union[str, BrowserType]] = None,
) -> Response: ...


def head(
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Any | None = ...,
        impersonate: Optional[Union[str, BrowserType]] = None,
) -> Response: ...


def post(
        url: str | bytes,
        data: _Data | None = ...,
        json: Any | None = ...,
        *,
        params: _Params | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        impersonate: Optional[Union[str, BrowserType]] = None,
) -> Response: ...


def put(
        url: str | bytes,
        data: _Data | None = ...,
        *,
        params: _Params | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Any | None = ...,
        impersonate: Optional[Union[str, BrowserType]] = None,
) -> Response: ...


def patch(
        url: str | bytes,
        data: _Data | None = ...,
        *,
        params: _Params | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Any | None = ...,
        impersonate: Optional[Union[str, BrowserType]] = None,
) -> Response: ...


def delete(
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Any | None = ...,
        impersonate: Optional[Union[str, BrowserType]] = None,
) -> Response: ...



def session_get(
        url: str | bytes,
        params: _Params | None = ...,
        *,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Any | None = ...,
        impersonate: Optional[Union[str, BrowserType]] = None,
) -> Response: ...


def session_post(
        url: str | bytes,
        data: _Data | None = ...,
        json: Any | None = ...,
        *,
        params: _Params | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        impersonate: Optional[Union[str, BrowserType]] = None,
) -> Response: ...