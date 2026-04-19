from dataclasses import dataclass, field
from typing import Optional
import uuid

@dataclass
class Step:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    input: Optional[str] = None
    output: Optional[str] = None
    status: str = "pending"