import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { CommunitiesData } from '../models/communities_model';
import { communitiesService } from '../services/communities.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-communities',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './communities.component.html',
  styleUrl: './communities.component.css'
})
export class CommunitiesComponent {
  formData: CommunitiesData = { 
    timestamp: new Date(), number_of_panels: 0, panel_area_m2: 0, category: 'kertes ház', consumption: 0, air_temp: 0, clearsky_dhi: 0, clearsky_dni: 0,
    clearsky_ghi: 0, clearsky_gti: 0, cloud_opacity: 0, dhi: 0, dni: 0, ghi: 0, gti: 0, season: 'Winter', snow_soiling_ground: 0, snow_soiling_rooftop: 0
  };
  predictedP: number | undefined;
  plotUrl: string | undefined;

  s_options = ['Winter', 'Spring', 'Summer', 'Autumn'];
  c_options = ['kertes ház', 'ikerház', 'panel lakás', 'apartman', 'sorház', 'tanya', 'kunyhó', 'családi ház', 'irodaház', 'iskola', 'hivatal', 'könyvtár', 'gyár']

  constructor(private communitiesService: communitiesService, private router: Router) {}

  predict(){
    const newCommunitiesData: CommunitiesData = {
      timestamp: this.formData.timestamp,
      number_of_panels: this.formData.number_of_panels,
      panel_area_m2: this.formData.panel_area_m2,
      category: this.formData.category,
      consumption: this.formData.consumption,
      air_temp: this.formData.air_temp,
      clearsky_dhi: this.formData.clearsky_dhi,
      clearsky_dni: this.formData.clearsky_dni,
      clearsky_ghi: this.formData.clearsky_ghi,
      clearsky_gti: this.formData.clearsky_gti,
      cloud_opacity: this.formData.cloud_opacity,
      dhi: this.formData.dhi,
      dni: this.formData.dni,
      ghi: this.formData.ghi,
      gti: this.formData.gti,
      season: this.formData.season,
      snow_soiling_ground: this.formData.snow_soiling_ground,
      snow_soiling_rooftop: this.formData.snow_soiling_rooftop
    }

    this.communitiesService.getPrediction(newCommunitiesData).subscribe(response => {
      this.predictedP = response.predicted_production;
    })
  }
}
