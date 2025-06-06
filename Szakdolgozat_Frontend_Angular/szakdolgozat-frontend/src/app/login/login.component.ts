import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common';
import { MatError } from '@angular/material/form-field';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatError],
    templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  loginForm: FormGroup;
  valid: boolean;
  imgUrl: string;
  showPassword: boolean;

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
    this.valid = true;
    this.imgUrl = "/assets/images/eye-close.png";
    this.showPassword = false;
  }

  hasError(controlName: string, errorName: string) {
    return this.loginForm.controls[controlName].hasError(errorName);
  }

  change(): void {
    if (this.imgUrl.endsWith("eye-close.png")){
      this.imgUrl = "/assets/images/eye-open.png";
      this.showPassword = true;
    }
    else{
      this.imgUrl = "/assets/images/eye-close.png";
      this.showPassword = false;
    }
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.value).subscribe(response => {
        this.valid = true;
        this.router.navigate(['/']);
      },
    err => {
      this.valid = false;
      this.loginForm.controls['password'].patchValue('');
    });
    }
  }
}
