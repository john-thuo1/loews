from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


class Report(models.Model):
    TYPE_SPECIES = [
        ("Unknown", "Unknown"),
        ("Bombay Locust ( Nomadacris succincta)", "Bombay Locust ( Nomadacris succincta)"),
        ("Desert Locusts(Schistocerca gregaria)", "Desert Locusts(Schistocerca gregaria)"),
        ("Grasshoppers", "Grasshoppers"),
        ("Migratory locust (Locusta migratoria)", "Migratory locust (Locusta migratoria)"),
        (" red locust (Nomadacris septemfasciata)", " red locust (Nomadacris septemfasciata)"),
        ("Spur Throated Locusts", "Spur Throated Locusts"),
        ("Tree locust (Anacridium sp.)", "Tree locust (Anacridium sp.)"),
    ]

    LOCUST_STAGE = [
        ("Adults", "Adults"),
        ("Hoppers/Nymph(Breeding Ground)", "Hoppers/Nymph(Breeding Ground)"),
        ("Fledglings(Young Adults)", "Fledglings(Young Adults)"),
        ("Eggs(Breeding Ground)", "Eggs(Breeding Ground)"),
        ("Unknown", "Unknown"),
    ]

    LAND_SIZE = [
        ("< 1 Acre", "< 1 Acre"),
        ("1 Acre", "1 Acre"),
        ("2 Acres", "2 Acres"),
        ("> 5 Acres", "> 5 Acres"),
        ("1 Ha", "1 Ha"),
        ("> 1 Ha", "> 1 Ha"),
        ("> 10 Ha", "> 10 Ha"),
        ("> 100 Ha", "> 100 Ha"),
    ]

    LOCUST_DISTRIBUTION = [
        ("Entire Field", "Entire Field"),
        ("Paddock Only", "Paddock Only"),
        ("Entire Area", "Entire Area"),
        ("Unknown", "Unknown"),
    ]

    LOCATION_SEASON = [
        ("Wet Season/Long Rains(April-June)", "Rainy/Wet Season(April-June)"),
        ("Short Rains/Wet Season(April-June)", "Rainy/Wet Season(April-June)"),
        ("Dry/Hot Season(January-March)", "Dry Season(January-March)"),
        ("Dry/Cold Season(July-August)", "Dry/Cold Season(July-August)"),
        ("Dry/Warm Season(September-October)", "Dry/Warm Season(September-October)"),
        ("Wet Season/Short Rains(November-December)", "Wet Season/Short Rains(November-December)"),
    ]

    SOIL = [
        ("Loose Sandy Soil", "Loose Sandy Soil"),
        ("Clay Soil", "Clay Soil"),
        ("Loam Soil", "Loam Soil"),
        ("Alluvial Soil", "Alluvial Soil"),
        ("Laterite Soil", "Laterite Soil"),
        ("Peat Soil", "Peat Soil"),
        ("Unknown", "Unknown"),
    ]

    VEGETATION_COVER = [
        ("Staple Crops", " Staple Crops"),
        ("Pasture and Grasslands", "Pasture and Grasslands"),
        ("Vegetable Crops", "Vegetable Crops"),
        ("Fruit Orchards", "Fruit Orchards"),
        ("Unknown", "Unknown"),
    ]

    name = models.CharField(max_length=100)
    phone_number = models.CharField(help_text="Include Country Code e.g +254710100000", max_length=13)
    report_date = models.DateField(help_text="Choose Date when Infestation/Breeding was noticed from the Calender")
    species = models.CharField(help_text="Enter the Locust Species", choices=TYPE_SPECIES, max_length=150)
    stage = models.CharField(help_text="Enter the Locust Stage", choices=LOCUST_STAGE, max_length=150)
    size = models.CharField(help_text="Land Size Infested/Breeding Ground", choices=LAND_SIZE, max_length=150)
    distribution = models.CharField(help_text="Locust Distribution", choices=LOCUST_DISTRIBUTION, max_length=150)
    image = models.ImageField(
        help_text="Upload a clear Image of Area Infested",
        upload_to='report_images/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    location = models.CharField(help_text="Location of the Locust Infestation/Breeding Grounds(Name, District, County)", max_length=255)
    season = models.CharField(help_text="Location Season", choices=LOCATION_SEASON, max_length=255)
    soil_type = models.CharField(help_text="Enter the Soil Type in the Affected Field especially for Breeding Grounds",choices=SOIL, max_length=255)
    vegetation_details = models.CharField(help_text="Vegetation types in the context of locusts (Cultivated and Agricultural areas).", choices=VEGETATION_COVER, max_length=255)
    gps_coordinates = models.CharField(help_text="Longitude, latitude e.g (-34.6, 26.1)", max_length=30)
    
    class Meta:
        verbose_name = "Report" 
        verbose_name_plural = "Reports"  

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"

    def __str__(self):
        return f'{self.user.username}: {self.message}'

