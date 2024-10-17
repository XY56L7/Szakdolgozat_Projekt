import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  private apiUrl = 'http://127.0.0.1:8000/api/predict/';

  constructor(private http: HttpClient) { }

  getPrediction(v_rms: number, i_rms: number, s: number) {
    const body = { V_rms: v_rms, I_rms: i_rms, S: s };
    return this.http.post<any>(this.apiUrl, body);
  }
}
