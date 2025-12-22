import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommunitiesData } from '../models/communities_model';
import { CommunitiesDataGru } from '../models/communities_model_gru';

@Injectable({
  providedIn: 'root'
})
export class communitiesService {
  private rows: string[] = [];

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

  getPredictionForGRU(body : CommunitiesDataGru[]){
    return this.http.post<any>('http://127.0.0.1:8000/api/predict_communities_gru/', body);
  }

  async getBody(file : File | null = null): Promise<CommunitiesDataGru[]> {
    await this.getRows(file);
    const body = this.getData();

    return body;
  }

  private getRows(file : File | null = null): Promise<void> {
    return new Promise((resolve, reject) => {
      if (file) {
        const reader = new FileReader();

        reader.onload = (e: any) => {
          const text = e.target.result;
          this.rows = text.split('\n').slice(1);
          resolve();
        };
        reader.onerror = (error) => {
          reject(error);
        }

        reader.readAsText(file);
      }
      else{
        alert("You need to upload a file to use this!");

        resolve();
      }
    });
  }

  private getData(): CommunitiesDataGru[] {
    const objectToSend: CommunitiesDataGru[] = this.rows.map((row) => {
      const cols = row.split(';');

      const data: CommunitiesDataGru = {
        number_of_panels: Number(cols[0]),
        panel_area_m2: Number(cols[1]),
        category: cols[2],
        air_temp: Number(cols[3]),
        clearsky_dhi: Number(cols[4]),
        clearsky_dni: Number(cols[5]),
        clearsky_ghi: Number(cols[6]),
        clearsky_gti: Number(cols[7]),
        dhi: Number(cols[8]),
        dni: Number(cols[9]),
        ghi: Number(cols[10]),
        gti: Number(cols[11]),
        cloud_opacity: Number(cols[12]),
        season: cols[13],
        snow_soiling_ground: Number(cols[14]),
        snow_soiling_rooftop: Number(cols[15])
      };

      return data;
    });

    return objectToSend;
  }
}
