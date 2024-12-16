import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root' // Automatikusan globális lesz
})
export class SettingSevice{
    public selectedSetting = new BehaviorSubject<string>('0');

    constructor(){
        const savedSetting = localStorage.getItem('selectedSetting') || '0';
    }

    updateSetting(newSetting: string): void {
        this.selectedSetting.next(newSetting);
        localStorage.setItem('selectedSetting', newSetting);
    }

    getSelectedSetting(): string {
        return this.selectedSetting.getValue();
    }
}