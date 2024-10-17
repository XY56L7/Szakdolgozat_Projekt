import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router'; // Import Router

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'] // Fixed 'styleUrl' to 'styleUrls'
})
export class HeaderComponent implements OnInit {

  public isAuthenticated: boolean = false;
  public userName: string = '';

  constructor(private authService: AuthService, private router: Router) {} // Inject Router

  ngOnInit(): void {
    console.log('User is authenticated:', this.isAuthenticated);
    this.authService.authSubject.subscribe(authStatus => {
      console.log('AuthServ')
      if (authStatus) {
        this.isAuthenticated = true;
      }
      console.log('User is authenticated:', this.isAuthenticated);
    });

    this.authService.authUserNameSubject.subscribe(authName => {
      if (authName) {
        this.userName = authName.userName;
      }
    });
  }

  logout(): void {
    this.authService.logout(); // Call the logout method from AuthService
    this.isAuthenticated = false; // Update local state
    this.router.navigate(['/login']); // Redirect to login page
  }
}
