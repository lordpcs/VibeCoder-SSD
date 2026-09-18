from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from app.schemas.task import TaskDefinition
from app.core.process_manager import ProcessManager

class BaseAgentRunner(ABC):
    def __init__(self, process_manager: ProcessManager):
        self.process_manager = process_manager

    @property
    @abstractmethod
    def agent_id(self) -> str:
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        pass

    @abstractmethod
    async def run(
        self,
        task: TaskDefinition,
        compiled_prompt: str,
        working_dir: str
    ) -> int:
        """
        Executes the agent for the given task and returns process exit code.
        """
        pass
