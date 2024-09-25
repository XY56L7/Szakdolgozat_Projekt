from django.db import models
from django.contrib.auth.models import User
    
    
class EnergyAnalysis(models.Model):
    DEVICE_OPTIONS = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        # Add other device options here
    ]
    
    device_option = models.CharField(max_length=100, choices=DEVICE_OPTIONS)
    devices = models.JSONField()  
    time_interval = models.CharField(max_length=50)
    prediction_model = models.CharField(max_length=100)
    V_rms = models.FloatField()  
    I_rms = models.FloatField()
    P = models.FloatField()
    S = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    custom_model_file = models.FileField(upload_to='custom_models/', blank=True, null=True) 

    def __str__(self):
        return f"Energy Analysis for {self.device_option} from {self.start_date} to {self.end_date}"
