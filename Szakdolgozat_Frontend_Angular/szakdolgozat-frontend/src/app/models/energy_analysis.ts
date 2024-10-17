export interface EnergyAnalysis {
    device_option: string;
    devices: string[];
    time_interval: string;
    prediction_model: string;
    V_rms: number;
    I_rms: number;
    P: number;
    S: number;
    start_date: string;
    end_date: string;
    custom_model_file?: File;
  }
  