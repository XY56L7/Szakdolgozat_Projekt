import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-evaluate',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './evaluate.component.html',
  styleUrl: './evaluate.component.css'
})
export class EvaluateComponent {
  predictedP: number | undefined;
  plotUrl: string | undefined;

  constructor(private router: Router) {
    const state = this.router.getCurrentNavigation()?.extras.state;
    this.predictedP = state?.['predictedP'];
    this.plotUrl = state?.['plotUrl'];
  }
}
