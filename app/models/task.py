from dataclasses import dataclass
from typing import Optional

"""
这是系统里所有任务的统一模板。
"""
@dataclass
class Task:
    input: str
    output: Optional[str] = None
    status: str = "pending"         # 默认状态：待执行