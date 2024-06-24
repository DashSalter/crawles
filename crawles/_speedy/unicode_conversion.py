from re import sub


def chinese_tou(text: str):  # 文本转换unicode
    # hex(x): 将整数 x 转换为十六进制字符串表示
    # ord(c): 返回字符 c 的Unicode码值
    # [2:] 去掉十六进制表示中的前缀"0x"
    return "".join([f'\\\\u{hex(ord(char))[2:]}' for char in text])


def unicode_toc(text: str):  # unicode转换文本
    # int(i, 16) 将十六进制的 Unicode 编码转换为整数
    # chr(x): 返回Unicode码值为 x 的字符
    return sub(r'\\u([0-9a-fA-F]{4}|[0-9a-fA-F]{2})',
               lambda match: chr(int(match.group(1), 16)),
               text)


if __name__ == '__main__':
    print('数据1转unicode:', chinese_tou("1"))
    print('数据aA会转unicode:', chinese_tou("aA会"))

    texts = "你好Hello, \\u4F60\\u597D\\u31\\u4F60\\u597D\\u31\\u4F60\\u597D\\u31"  # 包含 Unicode 编码的字符串
    print(unicode_toc(texts))
