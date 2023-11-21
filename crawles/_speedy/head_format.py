def head_format(header_data):  # 请求数据格式化函数
    head_dict = {}
    for data in header_data.splitlines():  # 将文本以行进行分割
        data = data.strip()  # 去重字符串左边的空格
        if not data:  # 过滤掉空的数据 ''  '    '
            continue
        if data.startswith(':'):  # 去重字符串的第一个冒号
            data = data.lstrip(':')

        key, value = data.split(':', maxsplit=1)

        # if 'accept-encoding' == str(key).lower():  # 过滤掉Accept-Encoding参数
        #     continue
        head_dict[key] = str(value).replace('^', '')

    return head_dict


if __name__ == '__main__':
    data1 = '''
    type: 0
    formhash: CDD4E5BDEA
    '''
    print(head_format(data1))
