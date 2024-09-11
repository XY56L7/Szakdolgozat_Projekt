import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideHttpClient, withFetch } from "@angular/common/http"; // withFetch importálása
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthInterceptor } from './services/auth.interceptos';

export const appConfig: ApplicationConfig = {
  providers: [provideHttpClient(withFetch()), provideRouter(routes),    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ]  // withFetch() hozzáadása
};
