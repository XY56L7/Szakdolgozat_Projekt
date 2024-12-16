import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ContentComponent } from './content/content.component';
import { HttpClientModule } from '@angular/common/http';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { MonitoringComponent } from './monitoring/monitoring.component';
import { EvaluateComponent } from './evaluate/evaluate.component';
import { IntroductionComponent } from './introduction/introduction.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { authGuard } from './auth.guard';
import { ProtectedComponent } from './protected/protected.component';
import { MerchantSettingsComponent } from './merchant-settings/merchant-settings.component';


export const routes: Routes = [
  { path: 'home', component: IntroductionComponent },
  { path: '', component: IntroductionComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'monitoring', component: MonitoringComponent },
  { path: 'evaluate', component: EvaluateComponent },
  { path: 'platform', component: ContentComponent },
  { path: 'merchantSetting', component: MerchantSettingsComponent },
  { path: 'protected', component: ProtectedComponent, canActivate: [authGuard] },
  { path: '**', component: NotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes),HttpClientModule ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
