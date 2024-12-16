import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { SettingSevice } from '../services/setting.service';

@Component({
  selector: 'app-merchant-settings',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './merchant-settings.component.html',
  styleUrl: './merchant-settings.component.css'
})
export class MerchantSettingsComponent {
  settingForm: FormGroup;
  selectedSetting: string;
  
  constructor(private fb: FormBuilder, private settingService: SettingSevice ) {
    this.settingForm = this.fb.group({
      setting: [this.settingService.getSelectedSetting()]
    });
    this.selectedSetting = this.settingService.getSelectedSetting();
  }

  onSettingChange(setting: string): void {
    this.settingService.updateSetting(setting);
  }
}
