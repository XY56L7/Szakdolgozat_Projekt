import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { Router } from '@angular/router';

interface TokenResponse {
  access: string;
  refresh: string;
  userName:string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:8000/api/';
  public authSubject = new BehaviorSubject<TokenResponse | null>(null);
  public authUserNameSubject = new BehaviorSubject<TokenResponse | null>(null);

  constructor(private http: HttpClient, private router: Router) { }

  register(user: any): Observable<any> {
    return this.http.post(`${this.apiUrl}register/`, user);
  }

  login(credentials: any): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${this.apiUrl}login/`, credentials).pipe(
      tap(response => {
        localStorage.setItem('access', response.access);
        localStorage.setItem('refresh', response.refresh);
        console.log("Line 41 auth service ts")
        this.authSubject.next(response);
        this.authUserNameSubject.next(response);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    this.authSubject.next(null);
    this.router.navigate(['/login']);
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access');
  }
}
