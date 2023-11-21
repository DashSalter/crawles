from requests.sessions import Session

from .MetaSession import my_session
from .optimized import optimized
from .response_optimized import response_optimized


@response_optimized
def get(url, params=None, headers=None, verify=None, proxies=None, **kwargs):
    """get请求"""
    return request("GET", url, params=params,
                   headers=headers, verify=verify,
                   proxies=proxies, **kwargs)


@response_optimized
def post(url, data=None, headers=None, verify=None, proxies=None, **kwargs):
    """post请求"""
    return request("POST", url, data=data,
                   headers=headers, verify=verify,
                   proxies=proxies, **kwargs)


@response_optimized
def session_get(url, params=None, headers=None, **kwargs):
    """session的get请求"""
    return my_session.meta_session('GET', url, params=params, headers=headers, **kwargs)


@response_optimized
def session_post(url, data=None, headers=None, **kwargs):
    """session的post请求"""
    return my_session.meta_session('POST', url, data=data, headers=headers, **kwargs)


@optimized
def request(method: str, url: str, **kwargs):
    # headers 数据优化
    with Session() as session:
        return session.request(method=method, url=url, **kwargs)
