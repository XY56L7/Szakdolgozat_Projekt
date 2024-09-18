import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { EnergyAnalysisService } from '../services/energy-analysis.service';
import { PredictionData } from '../models/energy_model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-content',
  standalone: true,
  imports: [CommonModule, FormsModule],  
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.css']
})
export class ContentComponent {
  formData: PredictionData = { v_rms: 0, i_rms: 0, s: 0, p: 0 }; // Using the model
  predictedP: number | undefined;
  plotUrl: string | undefined;
  selectedDevices: string[] = [];
  customModelFile: File | null = null;

  constructor(private energyAnalysisService: EnergyAnalysisService, private router: Router) {}

  // Hívjuk az API-t a formData objektummal
  predict() {
    const newPredictionData: PredictionData = {
      v_rms: this.formData.v_rms,
      i_rms: this.formData.i_rms,
      s: this.formData.s,
      p: this.formData.p,
    };
    this.energyAnalysisService.getPrediction(newPredictionData).subscribe(response => {
      this.predictedP = response.predicted_power;
      this.plotUrl = 'C:\Users\Martin\Desktop\szakdoga\Projekt\Szakdolgozat_Projekt\Szakdoga Django\django_backend\api\media\prediction_plot4918.png'; // Dinamikusan beállítjuk az elérési utat

      if (response.image_path) {
        console.log('Image URL:', this.plotUrl);
        this.plotUrl=response.image_path;
      }
            // Navigate to the evaluate route and pass the prediction data
            this.router.navigate(['/evaluate'], {
              state: { predictedP: this.predictedP, plotUrl: this.plotUrl }
            });
            // localStorage.setItem('predictedP', JSON.stringify(this.predictedP));
            // localStorage.setItem('plotUrl', this.plotUrl);
    });
  }

  onFileSelected(event: any): void {
    this.customModelFile = event.target.files[0];
  }

  onDeviceSelectionChange(event: any, device: string): void {
    if (event.target.checked) {
      this.selectedDevices.push(device);
    } else {
      this.selectedDevices = this.selectedDevices.filter(d => d !== device);
    }
  }

}
