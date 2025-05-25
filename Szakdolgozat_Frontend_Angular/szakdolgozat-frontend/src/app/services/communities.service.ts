import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommunitiesData } from '../models/communities_model';

@Injectable({
  providedIn: 'root'
})
export class communitiesService {

  constructor(private http: HttpClient) { }

  getPrediction(object : CommunitiesData) {
    const body = { 
        Timestamp: object.timestamp, Number_of_panels: object.number_of_panels, Panel_area_m2: object.panel_area_m2,
        Category: object.category, Consumption: object.consumption, Air_temp: object.air_temp, Clearsky_dhi: object.clearsky_dhi,
        Clearsky_dni: object.clearsky_dni, Clearsky_ghi: object.clearsky_ghi, Clearsky_gti: object.clearsky_gti, Cloud_opacity: object.cloud_opacity,
        Dhi: object.dhi, Dni: object.dni, Ghi: object.ghi, Gti: object.gti, Snow_soiling_rooftop: object.snow_soiling_rooftop,
        Snow_soiling_ground: object.snow_soiling_ground, Season: object.season
    };
    return this.http.post<any>('http://127.0.0.1:8000/api/predict_communities/', body);
  }
}
