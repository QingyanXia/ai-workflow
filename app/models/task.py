from dataclasses import dataclass, field
from typing import Optional, List
import uuid
from app.models.step import Step

"""
这是系统里所有任务的统一模板。
"""
@dataclass
class Task:
    input: str
    output: Optional[str] = None
    status: str = "pending"         # 默认状态：待执行
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    steps: List[Step] = field(default_factory=list)
