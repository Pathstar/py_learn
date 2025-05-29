# 1. 数据结构操作（列表推导式/字典生成）
def process_data(data: list) -> dict:
    """数据统计与转换（类型提示、字典推导式）"""
    return {
        "sum": sum(data),
        "avg": sum(data) / len(data),
        "squares": [x ** 2 for x in data],  # 列表推导式
        "evens": {x: x % 2 == 0 for x in data}  # 字典推导式
    }


# 2. 文件操作与异常处理
def read_file(filename: str) -> list:
    """带异常处理的文件读取（上下文管理器）"""
    try:
        with open(filename, 'r') as f:  # 上下文管理器
            return [float(line.strip()) for line in f]
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return []
    except ValueError as e:
        print(f"Invalid data: {e}")
        return []


# 3. 装饰器（高阶函数）
def timer(func):
    """函数执行时间记录装饰器"""
    from time import time
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"{func.__name__} executed in {end - start:.2f}s")
        return result

    return wrapper


# 4. 类与面向对象编程
class DataProcessor:
    """数据处理类（封装/继承/多态）"""

    def __init__(self, data: list):
        self.data = data

    @timer  # 应用装饰器
    def process(self):
        """处理方法（返回生成器节约内存）"""
        return (x * 2 for x in self.data if x > 0)  # 生成器表达式

    def __repr__(self):
        return f"DataProcessor({len(self.data)} elements)"


# 5. 使用常用内置模块
from collections import defaultdict


def count_frequency(items: list) -> dict:
    """使用collections模块统计频率"""
    counts = defaultdict(int)  # 默认字典
    for item in items:
        counts[item] += 1
    return dict(counts)


# 6. lambda和函数式编程
is_positive = lambda x: x > 0  # lambda函数
filter_positive = list(filter(is_positive, [-1, 0, 2, 3]))


# 7. 单元测试示例（面试可能需要现场写测试）
def test_process_data():
    """简单测试用例"""
    data = [1, 2, 3, 4]
    result = process_data(data)
    assert result["sum"] == 10
    assert result["avg"] == 2.5
    assert result["squares"] == [1, 4, 9, 16]


# 执行示例
if __name__ == "__main__":
    # 模块化执行
    data = read_file("data.txt")
    processor = DataProcessor(data)
    processed = processor.process()

    print(f"Processor: {processor}")
    print("Filtered positives:", filter_positive)
    print("Frequency:", count_frequency(['a', 'b', 'a']))

    test_process_data()
    print("All tests passed!")