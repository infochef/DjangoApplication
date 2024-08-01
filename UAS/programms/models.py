from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Programs_Scheduled(models.Model):

    Scheduled_program_id = models.AutoField(_("Scheduled Program Id"), primary_key=True)
    ProgramName = models.CharField(_("Program Name"), max_length=50)
    Location = models.CharField(_("Location"), max_length=50)
    Start_Date = models.DateField(_("Start Date"), auto_now=False, auto_now_add=False)
    End_Date = models.DateField(_("End Date"), auto_now=False, auto_now_add=False)
    sessions_per_week = models.IntegerField(_("Sessions Per Week"))

    class Meta:
        db_table = 'Programs Scheduled'
        verbose_name = 'Program Scheduled'
        verbose_name_plural = 'Programs Scheduled'

    def __str__(self):
        return (
            f"{self.Scheduled_program_id} {self.ProgramName} {self.Location} {self.Start_Date} {self.End_Date}"
            f"{self.sessions_per_week}"
             )


class Programs_Offered(models.Model):

    ProgramId = models.AutoField(_("Program Id"), primary_key=True)
    ProgramName = models.CharField(_("Program_Name"), max_length=50)
    Description = models.CharField(_("Description"), max_length=50)
    Applicant_eligibility = models.CharField(_("Applicant Eligibility"), max_length=30)
    Duration = models.IntegerField(_("Duration"))
    Degree_certificate_offered = models.CharField(_("Degree Certificate Offered"), max_length=20)
    

    class Meta:
        db_table = 'Programs Offered'
        verbose_name = 'Program Offered'
        verbose_name_plural = 'Programs Offered'

    def __str__(self):
       return (
           f"{self.ProgramId} {self.ProgramName} {self.Description} {self.Applicant_eligibility} {self.Duration}"
           f"{self.Degree_certificate_offered}"
       )

 
