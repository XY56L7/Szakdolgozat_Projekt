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
  formData: PredictionData = { v_rms: 0, i_rms: 0, s: 0, device: '' }; // Using the model
  predictedP: number | undefined;
  plotUrl: string | undefined;
  selectedDevice: string | null = null; // Changed to a single selected device
  customModelFile: File | null = null;

  constructor(private energyAnalysisService: EnergyAnalysisService, private router: Router) {}

  predict() {
    const newPredictionData: PredictionData = {
      v_rms: this.formData.v_rms,
      i_rms: this.formData.i_rms,
      s: this.formData.s,
      device: this.selectedDevice || '' // Use selectedDevice
    };

    this.energyAnalysisService.getPrediction(newPredictionData).subscribe(response => {
      this.predictedP = response.predicted_power;

      if (response.image_path) {
        this.plotUrl = response.image_path;
        console.log('Image URL:', this.plotUrl);
      }

      this.router.navigate(['/evaluate'], {
        state: { predictedP: this.predictedP, plotUrl: this.plotUrl }
      });
    });
  }

  onFileSelected(event: any): void {
    this.customModelFile = event.target.files[0];
  }

  onDeviceSelectionChange(event: any, device: string): void {
    // Set the selected device based on the radio button checked state
    if (event.target.checked) {
      this.selectedDevice = device;
    }
  }
}
