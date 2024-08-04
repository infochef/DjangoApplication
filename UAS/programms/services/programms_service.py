import logging
from typing import List
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .programms import ProgramService
from ..models import Programs_Offered, Programs_Scheduled

logger = logging.getLogger(__name__)

class ProgramServiceImpl(ProgramService):

    def add_program_offered(self, programs_offered: Programs_Offered):
        try:
            programs_offered.save()
            logger.info(f"Program offered added: {programs_offered.ProgramName}")
        except ValidationError as e:
            logger.error(f"Validation error while adding program offered: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while adding program offered: {e}")
            raise

    def update_program_offered(self, programs_offered: Programs_Offered):
        try:
            programs_offered.save()
            logger.info(f"Program offered updated: {programs_offered.ProgramName}")
        except ObjectDoesNotExist:
            logger.error(f"Program offered not found: {programs_offered.ProgramId}")
            raise
        except ValidationError as e:
            logger.error(f"Validation error while updating program offered: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while updating program offered: {e}")
            raise

    def delete_program_offered(self, program_name: str):
        try:
            program = Programs_Offered.objects.get(ProgramName=program_name)
            program.delete()
            logger.info(f"Program offered deleted: {program_name}")
        except ObjectDoesNotExist:
            logger.error(f"Program offered not found: {program_name}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while deleting program offered: {e}")
            raise

    def list_all_programs(self) -> List[Programs_Offered]:
        try:
            programs = Programs_Offered.objects.all()
            logger.info("Listed all programs offered")
            return list(programs)
        except Exception as e:
            logger.error(f"Unexpected error while listing all programs offered: {e}")
            raise

    def create_scheduled_program(self, programs_scheduled: Programs_Scheduled):
        try:
            programs_scheduled.save()
            logger.info(f"Scheduled program created: {programs_scheduled.ProgramName}")
        except ValidationError as e:
            logger.error(f"Validation error while creating scheduled program: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while creating scheduled program: {e}")
            raise

    def update_scheduled_program(self, programs_scheduled: Programs_Scheduled):
        try:
            programs_scheduled.save()
            logger.info(f"Scheduled program updated: {programs_scheduled.ProgramName}")
        except ObjectDoesNotExist:
            logger.error(f"Scheduled program not found: {programs_scheduled.Scheduled_program_id}")
            raise
        except ValidationError as e:
            logger.error(f"Validation error while updating scheduled program: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while updating scheduled program: {e}")
            raise

    def delete_scheduled_program(self, scheduled_program_id: int):
        try:
            program = Programs_Scheduled.objects.get(Scheduled_program_id=scheduled_program_id)
            program.delete()
            logger.info(f"Scheduled program deleted: {scheduled_program_id}")
        except ObjectDoesNotExist:
            logger.error(f"Scheduled program not found: {scheduled_program_id}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while deleting scheduled program: {e}")
            raise

    def list_all_scheduled_programs(self, program_name: str) -> List[Programs_Scheduled]:
        try:
            programs = Programs_Scheduled.objects.filter(ProgramName=program_name)
            logger.info(f"Listed all scheduled programs for program: {program_name}")
            return list(programs)
        except Exception as e:
            logger.error(f"Unexpected error while listing all scheduled programs: {e}")
            raise
