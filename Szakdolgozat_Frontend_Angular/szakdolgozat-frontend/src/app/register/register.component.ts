import { Component } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatFormFieldModule, MatInputModule, MatButtonModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerForm: FormGroup;
  submitted = false;
  imgUrl: string;
  showPassword: boolean;

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) {
    this.registerForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      c_password: ['', [Validators.required, Validators.minLength(6)]]
    },
    {
      validators: this.passwordMatchValidator
    });
    this.imgUrl = "/assets/images/eye-close.png";
    this.showPassword = false;
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

  passwordMatchValidator(control: AbstractControl) {
    return control.get('c_password')?.value === control.get('password')?.value ? null : { mismatch: true };
  }

  onSubmit() {
    this.submitted = true;
    if (this.registerForm.valid) {
      this.authService.register(this.registerForm.value).subscribe(response => {
        this.router.navigate(['/login'], {
         
        });
      });
    }
  }

  hasError(field: string, error: string) {
    return this.registerForm.get(field)!.hasError(error) && this.submitted;
  }
}
