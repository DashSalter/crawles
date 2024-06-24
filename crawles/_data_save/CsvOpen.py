from _csv import writer, reader

from typing import Iterable, Any


class CsvOpen:
    def __init__(self, filename, mode='r', encoding='gbk', newline='', **kwargs):
        """csv文件存储"""
        self._csv_file = open(filename, mode, encoding=encoding,  # 打开文件
                              newline=newline, **kwargs)
        if mode.startswith('r'):  # 使用写或者读
            self.reader_ = reader(self._csv_file)
        else:
            self.writer_ = writer(self._csv_file)

    def __iter__(self):  # 创建为可迭代对象
        return self

    def __next__(self):  # 循环数据
        return next(self.reader_)

    def read_line(self):  # 返回一行数据
        try:
            return self.__next__()
        except StopIteration:
            return None

    def read_lines(self) -> list:  # 返回列表所有数据
        return list(self.reader_)

    def __enter__(self):  # 上下文启动
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # 上下文自动关闭
        self.close()

    def close(self):  # 文件手动关闭
        if self._csv_file:
            self._csv_file.close()

    def writerow(self, row: Iterable[Any]):  # 写入一行
        self.writer_.writerow(row)

    def writerows(self, row: Iterable[Any]):  # 写入多行
        self.writer_.writerows(row)


if __name__ == '__main__':
    pass
    # csv_obj = CsvOpen('data.csv', mode='r')
    # csv_obj.writerow(['1', '2', '3', '4'])
    # csv_obj.writerow(['a', 'b', 'c', 'd'])
    # for i in csv_obj:
    #     print(i)
    # print(csv_obj.next_lines())

    # csv_obj.writerows([['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']])
    # csv_obj.close()

    # with CsvOpen('data.csv', mode='w+') as csv_obj:
    #     csv_obj.writerow(['a', 'b', 'c', 'd'])
    #     csv_obj.writerows([['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']])
