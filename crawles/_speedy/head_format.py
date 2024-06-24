from re import findall


def head_format(header_data: str) -> dict:
    """请求数据格式化函数"""
    if not isinstance(header_data, str):
        raise TypeError('The parsed object needs to be a string')

    data = findall('([-a-zA-Z]+)\s*:\s*(.*)', header_data)
    return {key: value for key, value in data}


if __name__ == '__main__':
    data1 = '''
    :Accept: */*
    Accept-Encoding:zh-CN,zh;q=0.9
    X-Requested-With      :   XMLHttpRequest
    sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    '''
    import crawles
    crawles.op(head_format(data1))
