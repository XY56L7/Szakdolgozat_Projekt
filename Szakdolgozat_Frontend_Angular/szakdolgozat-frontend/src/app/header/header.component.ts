import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  public isAuthenticated: boolean = false;
  public userName: string = '';
  public isNavbarCollapsed: boolean = false;

  private collapseTimeout: any;

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.authService.authSubject.subscribe(authStatus => {
      if(authStatus){
        this.isAuthenticated = true;
      }
    });

    this.authService.authUserNameSubject.subscribe(authName => {
      if (authName) {
        this.userName = authName.userName;
      }
    });

    this.setNavbarCollapseTimer();
  }

  expandNavbar(): void {
    clearTimeout(this.collapseTimeout);
    this.isNavbarCollapsed = false;
  }

  collapseNavbar(): void {
    this.setNavbarCollapseTimer();
  }

  private setNavbarCollapseTimer(): void {
    this.collapseTimeout = setTimeout(() => {
      this.isNavbarCollapsed = true;
    }, 3000); // 3 másodperc után összehúzza a navbar-t
  }

  logout(): void {
    this.authService.logout();
    this.isAuthenticated = false;
    this.router.navigate(['/login']);
  }
}
