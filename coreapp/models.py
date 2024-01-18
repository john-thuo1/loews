from django.db import models

# Create your models here.

class Report(models.Model):
    name = models.CharField(max_length=100)
    telephone_number = models.IntegerField(max_length=13)
    report_date = models.DateField()
    species = models.Choices( Grasshoppers,Desert Locusts, Spur Throated Locusts, Unknown)
    stage = models.Choices( Adults, Hoppers, Bands, Swarms, Unknown)
    size = models.Choices(helper_text="Area of Infestation")
    distribution = models.Choices(Unknown, Entire Property, Paddock Only, Entire Area)
    Image = models.FileField()
    
    Location = models.TextField()
    GPS_Cordinates = models.TextField(helper_text="Long, latitude")
    Vegetation_Details = models.Choices(Dry, Green)
    
    
    description = models.TextField(max_length=1000, help_text="Enter a brief description of the Report.")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"