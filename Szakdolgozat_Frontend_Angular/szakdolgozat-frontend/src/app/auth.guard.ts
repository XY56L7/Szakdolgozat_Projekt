import { CanActivateFn, Router } from '@angular/router';
import { inject, Injectable } from '@angular/core';
import { jwtDecode } from 'jwt-decode';

export const authGuard: CanActivateFn = (route, state) => {
    const token = localStorage.getItem('access');
    const router = inject(Router);

    if (token) {
      // Ha van token, hozzáférhet.
      const decodedToken = jwtDecode<{ exp: number }>(token);
      const isExpired = decodedToken.exp * 1000 < Date.now();

      if (isExpired){
        localStorage.removeItem('access');
        router.navigate(['/login']);
        return false
      }
      return true
    } else {
      router.navigate(['/login']);
      return false; // Ha nincs token, visszairányítjuk.
    }
}
