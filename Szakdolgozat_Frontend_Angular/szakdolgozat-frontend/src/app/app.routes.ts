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

export const routes: Routes = [
  { path: 'home', component: IntroductionComponent },
  { path: '', component: IntroductionComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'monitoring', component: MonitoringComponent },
  { path: 'evaluate', component: EvaluateComponent },
  { path: 'platform', component: ContentComponent },
  { path: '**', component: NotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes),HttpClientModule ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
