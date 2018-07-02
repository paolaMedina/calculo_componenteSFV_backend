from django.db import models


class GeneralFVForm(models.Model):
    power_of_plant_fv = models.IntegerField()
    total_panels_fv = models.IntegerField()
    power_of_panel_fv = models.IntegerField()
    ambient_temperature =  models.IntegerField()
    lowest_ambient_temperature_expected = models.IntegerField()
    investment_type = models.CharField(max_length = 40)
    service_type = models.CharField(max_length = 40)
    service_voltage = models.IntegerField()
    instalation_place = models.CharField(max_length = 40)
    class Meta:
        managed = False
