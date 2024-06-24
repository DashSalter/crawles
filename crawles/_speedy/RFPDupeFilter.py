from hashlib import sha1


def to_bytes(text, encoding=None, errors='strict'):
    """返回 text的二进制表示形式。如果 ''text''已经是 bytes 对象，按原样返回。"""
    if isinstance(text, bytes):
        return text
    if not isinstance(text, str):
        raise TypeError('to_bytes must receive a str or bytes '
                        f'object, got {type(text).__name__}')
    if encoding is None:
        encoding = 'utf-8'
    return text.encode(encoding, errors)


class RFPDupeFilter:
    """Request Fingerprint duplicates filter"""

    def __init__(self, file_path=None):
        self.file = None
        self.fingerprints = set()
        self.include_headers = False

        if file_path:
            self.file = open(file_path, 'a+')
            self.file.seek(0)
            self.fingerprints.update(x.rstrip() for x in self.file)

    def request_seen(self, request) -> bool:
        fp = self.request_fingerprint(request)  # 得到url对象
        if fp in self.fingerprints:
            return True  # 返回True 表示已经存在
        self.fingerprints.add(fp)
        if self.file:  # 如果有文件对象则写入
            self.file.write(fp + '\n')
        return False

    def close(self):
        if self.file:
            self.file.close()

    def request_fingerprint(self, request):
        """请求指纹获取"""
        fp = sha1()
        if self.include_headers:
            for k, v in request.headers.items():
                fp.update(to_bytes(f'{k}{v}'))

        fp.update(to_bytes(request.method))
        fp.update(to_bytes(request.url))

        for k, v in request.data.items():
            fp.update(to_bytes(f'{k}{v}'))

        return fp.hexdigest()
