from abc import ABC, abstractmethod
from typing import Optional, List

class KnowledgeBase(ABC):
    @abstractmethod
    def query(self, text: str) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def list_entries(self) -> List[dict]:
        raise NotImplementedError()
