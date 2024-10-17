import { Component } from '@angular/core';

@Component({
  selector: 'app-monitoring',
  standalone: true,
  imports: [],
  templateUrl: './monitoring.component.html',
  styleUrl: './monitoring.component.css'
})
export class MonitoringComponent {
  images: string[] = [
    'assets/images/monitoring1.png',
    'assets/images/monitoring2.jpg',
  ];
  
  currentIndex: number = 0; 
  currentImage: string = this.images[this.currentIndex]; 

  switchImage() {
    this.currentIndex = (this.currentIndex + 1) % this.images.length;
    this.currentImage = this.images[this.currentIndex];
  }
}
