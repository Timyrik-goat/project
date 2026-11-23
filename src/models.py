from dataclasses import dataclass, field, asdict
from uuid import uuid4
from enum import Enum

class Status(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"

class DealStage(str, Enum):
    VIEW = "view"
    NEGOTIATION = "negotiation"
    CLOSED = "closed"

@dataclass
class Object:
    id: str = field(default_factory=lambda: str(uuid4()))
    address: str = ""
    type: str = "apartment"
    area: float = 0.0
    rooms: int = 0
    price: float = 0.0
    status: str = Status.ACTIVE.value
    description: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "Object":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Client:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    phone: str = ""
    budget: float = 0.0
    requirements: dict = field(default_factory=dict)
    contact_date: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "Client":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Deal:
    id: str = field(default_factory=lambda: str(uuid4()))
    object_id: str = ""
    client_id: str = ""
    agent_id: str = ""
    stage: str = DealStage.VIEW.value
    created: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "Deal":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        return asdict(self)
