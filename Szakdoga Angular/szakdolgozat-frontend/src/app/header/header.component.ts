import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent implements OnInit {

  public isAuthenticated: boolean = false;

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    console.log('User is authenticated:', this.isAuthenticated);
    this.authService.authSubject.subscribe(authStatus => {
      console.log('AuthServ')
      if(authStatus){
        this.isAuthenticated = true;
      }
      console.log('User is authenticated:', this.isAuthenticated);
    });
  }
}