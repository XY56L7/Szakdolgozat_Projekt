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
  formData: PredictionData = { v_rms: 0, i_rms: 0, s: 0, device: '' };
  predictedP: number | undefined;
  plotUrl: string | undefined;
  selectedDevice: string | null = null;
  customModelFile: File | null = null;
  selectedAnalysisType: string = ''; 

  energyCommunityData = {
    year: 2024,
    month: 1,
    day: 15,
    hour: 12,
    number_of_panels: 10,
    season: 'Winter',
    category: 'kertes ház'
  };

  constructor(private energyAnalysisService: EnergyAnalysisService, private router: Router) {}

  predict() {
    if (this.selectedAnalysisType === 'device') {
      const newPredictionData: PredictionData = {
        v_rms: this.formData.v_rms,
        i_rms: this.formData.i_rms,
        s: this.formData.s,
        device: this.selectedDevice || ''
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
    } else if (this.selectedAnalysisType === 'consumption') {
      const data = {
        year: this.energyCommunityData.year,
        month: this.energyCommunityData.month,
        day: this.energyCommunityData.day,
        hour: this.energyCommunityData.hour,
        number_of_panels: this.energyCommunityData.number_of_panels,
        season: this.energyCommunityData.season,
        category: this.energyCommunityData.category
      };

      this.energyAnalysisService.getConsume(data).subscribe(resp => {
        this.predictedP = resp.consumption_power;

        this.router.navigate(['/evaluate'], {
          state: { predictedP: this.predictedP }
        });
      });
    }else if (this.selectedAnalysisType === 'production') {
      const data = {
        year: this.energyCommunityData.year,
        month: this.energyCommunityData.month,
        day: this.energyCommunityData.day,
        hour: this.energyCommunityData.hour,
        number_of_panels: this.energyCommunityData.number_of_panels,
        season: this.energyCommunityData.season,
        category: this.energyCommunityData.category
      };

      this.energyAnalysisService.getConsume(data).subscribe(resp => {
        this.predictedP = resp.production_power;

        this.router.navigate(['/evaluate'], {
          state: { predictedP: this.predictedP }
        });
      });
    }
  }

  onFileSelected(event: any): void {
    this.customModelFile = event.target.files[0];
  }
}
