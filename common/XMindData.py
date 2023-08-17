import jsonpath

from xmindparser import xmind_to_dict


class XMindData(object):
    """
    XMind数据处理
    """

    def __init__(self):
        """
        定义两个list数组
        """
        # 存放每一条用例
        self.case: list = []
        # 存放所有的用例list
        self.lists_data: list = []

    @staticmethod
    def read_XMind_to_list(XMindName) -> list:
        """
        获取XMind文件所有的内容
        :param XMindName:
        :return: list
        """
        return xmind_to_dict(XMindName)

    def __data_processing(self, data: dict):
        """
        私有方法，采用递归处理数据
        :param data: dict类型
        """
        self.case.append(data["title"])
        # 通过json path判断是该data是否包含topics节点（包含返回数据，不包含则返回False）
        # 如果找到的话返回的结果是一个列表
        result = jsonpath.jsonpath(data, "$.topics")

        # 判断result类型，不是bool类型的时候进行递归
        if type(result) != bool:
            for xm in result:
                for m in xm:
                    self.__data_processing(m)
            # 此处需要在把最后一个节点删除掉
            self.case = self.case[:-1]
        else:
            self.lists_data.append(self.case)
            self.case = self.case[:-1]

    def get_lists_data(self, data) -> list:


        """
        循环调用递归函数，读取数据，
        :param data: 传的数据参数是第一个画布的头节点的所有节点信: data = allData[0]["topic"]["topics"]
        :return: list嵌套list，每一个嵌套的list就是一条测试用例
        """
        for xm in data:
            self.__data_processing(xm)
            # 清空每次循环的遗留数据，不给后面造成影响
            self.case.clear()
        return self.lists_data

    def clear_init_list_data(self):
        """
        清空初始化列表数据，避免后面数据出现脏数据
        """
        self.case.clear()
        self.lists_data.clear()


if __name__ == '__main__':
    list1 = XMindData.read_XMind_to_list("../data/case.xmind")
    xm = XMindData()
    print(xm.get_lists_data(list1[0]["topic"]["topics"]))

