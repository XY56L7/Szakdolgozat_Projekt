from django.db import models

# Create your models here.

#How ur data will look like

class User(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.name
    
    
class EnergyAnalysis(models.Model):
    DEVICE_OPTIONS = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        # Add other device options here
    ]
    
    device_option = models.CharField(max_length=100, choices=DEVICE_OPTIONS)
    devices = models.JSONField()  # To store the array of devices
    time_interval = models.CharField(max_length=50)
    prediction_model = models.CharField(max_length=100)
    V_rms = models.FloatField()  # For storing floating-point numbers
    I_rms = models.FloatField()
    P = models.FloatField()
    S = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    custom_model_file = models.FileField(upload_to='custom_models/', blank=True, null=True)  # Optional file upload

    def __str__(self):
        return f"Energy Analysis for {self.device_option} from {self.start_date} to {self.end_date}"
