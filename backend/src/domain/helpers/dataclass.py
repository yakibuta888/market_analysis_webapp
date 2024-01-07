from dataclasses import dataclass
from abc import ABCMeta

@dataclass(frozen=True, eq=True)
class DataClassBase(metaclass=ABCMeta):
    pass
