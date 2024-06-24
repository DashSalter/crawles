from curl_cffi.requests.session import Session


class SingletonMeta(type):
    def __call__(cls, *args, **kwargs):
        """单例模式"""
        if not hasattr(cls, '_instance'):
            cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class MetaSession(metaclass=SingletonMeta):
    """使用同一个Session,需要继承单例对象"""
    session = Session()

    def meta_session(self, method, url, **kwargs):
        return self.session.request(method=method, url=url, **kwargs)


my_session = MetaSession()
