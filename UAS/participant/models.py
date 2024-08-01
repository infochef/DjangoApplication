from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Participant(models.Model):
    Roll_no = models.IntegerField(_("Roll No"))
    Email_id = models.EmailField(_("Email Id"), max_length=254)
    Application_id = models.ForeignKey("Application", verbose_name=_("Application Id"), on_delete=models.CASCADE)
    Scheduled_program_id = models.IntegerField(_("Scheduled Program Id"))

    class Meta:
        db_table = 'Participant'
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'

    def __str__(self):
        return f"{self.Roll_no} {self.Email_id} {self.Application_id} {self.Scheduled_program_id}"

class Application(models.Model):
    Application_id = models.AutoField(_("Application Id"), primary_key=True)
    Full_Name = models.CharField(_("Full Name"), max_length=50)
    Date_of_birth = models.DateField(_("Date Of Birth"))
    Highest_qualification = models.CharField(_("Highest Qualification"), max_length=50)
    Marks_obtained = models.IntegerField(_("Marks Obtained"))
    Goals = models.CharField(_("Goals"), max_length=50)
    Email_id = models.EmailField(_("Email Id"), max_length=254)
    Scheduled_program_id = models.IntegerField(_("Scheduled Program Id"))
    Status = models.CharField(_("Status"), max_length=50)
    Date_Of_Interview = models.DateField(_("Date Of Interview"))

    class Meta:
        db_table = 'Application'
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return (
            f"{self.Application_id} {self.Full_Name} {self.Date_of_birth} {self.Highest_qualification} "
            f"{self.Marks_obtained} {self.Goals} {self.Email_id} {self.Scheduled_program_id} {self.Status} "
            f"{self.Date_Of_Interview}"
        )
