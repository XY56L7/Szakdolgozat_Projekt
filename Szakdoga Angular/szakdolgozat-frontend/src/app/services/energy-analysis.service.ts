import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { EnergyAnalysis } from '../models/energy_analysis';

@Injectable({
  providedIn: 'root'
})
export class EnergyAnalysisService {

  private apiUrl = 'https://example.com/api/energy-analysis';  // A szerver URL-je

  constructor(private http: HttpClient) { }

  submitButtonForTesting(): Observable<EnergyAnalysis>{
    return this.http.get<any>('http://127.0.0.1:8000/api/users/energy/');
  }

  submitEnergyAnalysis(data: EnergyAnalysis): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'multipart/form-data' // Mivel fájl is van az űrlapon
    });

    const formData: FormData = new FormData();
    formData.append('device_option', data.device_option);
    data.devices.forEach(device => formData.append('devices', device));
    formData.append('time_interval', data.time_interval);
    formData.append('prediction_model', data.prediction_model);
    formData.append('V_rms', data.V_rms.toString());
    formData.append('I_rms', data.I_rms.toString());
    formData.append('P', data.P.toString());
    formData.append('S', data.S.toString());
    formData.append('start_date', data.start_date);
    formData.append('end_date', data.end_date);

    if (data.custom_model_file) {
      formData.append('custom_model_file', data.custom_model_file);
    }

    return this.http.post<any>(this.apiUrl, formData, { headers });
  }
}
