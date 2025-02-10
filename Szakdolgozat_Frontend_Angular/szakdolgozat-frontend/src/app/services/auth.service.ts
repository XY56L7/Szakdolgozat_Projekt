import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
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
    return this.http.post(`${this.apiUrl}register/`, user).pipe(
      catchError((error: HttpErrorResponse) => {
        let errorMsg = 'Valami hiba történt.';

        if (error?.error?.username) {
          errorMsg = error.error.username[0];
        }

        return throwError(() => errorMsg);
      })
    );
  }

  login(credentials: any): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${this.apiUrl}login/`, credentials).pipe(
      tap(response => {
        localStorage.setItem('access', response.access);
        localStorage.setItem('refresh', response.refresh);
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
