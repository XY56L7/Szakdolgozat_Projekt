import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { EnergyAnalysisService } from '../services/energy-analysis.service';

@Component({
  selector: 'app-content',
  standalone: true,
  imports: [CommonModule, FormsModule],  
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.css']
})
export class ContentComponent {
  selectedDevices: string[] = [];
  customModelFile: File | null = null;

  constructor(private energyAnalysisService: EnergyAnalysisService) {}

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

  onSubmit(form: any): void {
    const energyAnalysisData = {
      device_option: form.value.device_option,
      devices: this.selectedDevices,
      time_interval: form.value.time_interval,
      prediction_model: form.value.prediction_model,
      V_rms: form.value.V_rms,
      I_rms: form.value.I_rms,
      P: form.value.P,
      S: form.value.S,
      start_date: form.value.start_date,
      end_date: form.value.end_date,
      custom_model_file: this.customModelFile || undefined
    };

    this.energyAnalysisService.submitEnergyAnalysis(energyAnalysisData).subscribe(response => {
      console.log('Analysis submitted successfully!', response);
    }, error => {
      console.error('Error submitting analysis', error);
    });
  }

  onSubmitForTesting(): void {
    console.log("54 sor submit gomb a tesztelesnek")
    this.energyAnalysisService.submitButtonForTesting().subscribe(
      x => console.log(x)
    );
  }
}
