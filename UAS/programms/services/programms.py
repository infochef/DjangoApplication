from abc import ABC, abstractmethod
from typing import List
from ..models import Programs_Offered, Programs_Scheduled

class ProgramService(ABC):

    @abstractmethod
    def add_program_offered(self, programs_offered: Programs_Offered):
        pass

    @abstractmethod
    def update_program_offered(self, programs_offered: Programs_Offered):
        pass

    @abstractmethod
    def delete_program_offered(self, program_name: str):
        pass

    @abstractmethod
    def list_all_programs(self) -> List[Programs_Offered]:
        pass

    @abstractmethod
    def create_scheduled_program(self, programs_scheduled: Programs_Scheduled):
        pass

    @abstractmethod
    def update_scheduled_program(self, programs_scheduled: Programs_Scheduled):
        pass

    @abstractmethod
    def delete_scheduled_program(self, scheduled_program_id: int):
        pass

    @abstractmethod
    def list_all_scheduled_programs(self, program_name: str) -> List[Programs_Scheduled]:
        pass
