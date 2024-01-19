from django.db import models
from django.core.validators import FileExtensionValidator


class Report(models.Model):
    TYPE_SPECIES = {
        "Unknown": "Unknown",
        "Bombay Locust ( Nomadacris succincta)":"Bombay Locust ( Nomadacris succincta)",
        "Desert Locusts(Schistocerca gregaria)": "Desert Locusts(Schistocerca gregaria)",
        "Grasshoppers": "Grasshoppers",
        "Migratory locust (Locusta migratoria)": "Migratory locust (Locusta migratoria)",
        " red locust (Nomadacris septemfasciata)": " red locust (Nomadacris septemfasciata)",
        "Spur Throated Locusts": "Spur Throated Locusts",
        "Tree locust (Anacridium sp.)": "Tree locust (Anacridium sp.)",
    }

    LOCUST_STAGE = {
        "Adults": "Adults",
        "Hoppers/Nymph": "Hoppers/Nymph",
        "Fledglings": "Fledglings",
        "Eggs":"Eggs",
        "Unknown": "Unknown",
    }

    LAND_SIZE = {
        "< 1 Acre": "< 1 Acre",
        "1 Acre": "1 Acre",
        "2 Acres": "2 Acres",
        "> 5 Acres": "> 5 Acres",
        "1 Ha": "1 Ha",
        "> 1 Ha": "> 1 Ha",
        "> 10 Ha": "> 10 Ha",
        "> 100 Ha": "> 100 Ha",
    }

    LOCUST_DISTRIBUTION = {
        "Entire Field": "Entire Field",
        "Paddock Only": "Paddock Only",
        "Entire Area": "Entire Area",
        "Unknown": "Unknown",
    }

    VEGETATION_COVER = {
        "Dry": "Dry",
        "Green": "Green",
        "Sandy":"Sandy",
        "Unknown" : "Unknown",
    }

    name = models.CharField(max_length=100)
    phone_number = models.CharField(help_text="Include Country Code e.g +254710100000", max_length=13)
    report_date = models.DateField()
    species = models.CharField(help_text="Enter the Locust Species", choices=TYPE_SPECIES, max_length=50)
    stage = models.CharField(help_text="Enter the Locust Stage", choices=LOCUST_STAGE, max_length=50)

    size = models.CharField(help_text="Land Size Infested/Breeding Ground", choices=LAND_SIZE, max_length=20)
    distribution = models.CharField(help_text="Locust Distribution", choices=LOCUST_DISTRIBUTION, max_length=20)

    image = models.ImageField(
        help_text="Upload a clear Image of Area Infested",
        upload_to='report_images/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    location = models.CharField(help_text="Location of the Locust Infestation/Breeding Grounds(Name, District, County)", max_length=255)
    vegetation_details = models.CharField(help_text="Type of Vegetation Infested", choices=VEGETATION_COVER, max_length=20)
    gps_coordinates = models.CharField(help_text="Longitude, latitude e.g (-34.6, 26.1)", max_length=30, blank=True, null=True)
