import { Component, signal, OnInit, computed } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  protected readonly title = signal('FastAPI Health Check');
  protected readonly healthStatus = signal<string>('Checking...');
  protected readonly isLoading = signal<boolean>(true);
  protected readonly error = signal<string | null>(null);

  protected readonly capitalizedHealthStatus = computed(() => {
    const status = this.healthStatus();
    return status.charAt(0).toUpperCase() + status.slice(1);
  });

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.checkHealth();
  }

  checkHealth() {
    this.isLoading.set(true);
    this.error.set(null);
    this.healthStatus.set('Checking...');

    // Using proxy configuration - /api maps to http://localhost:8000
    const backendUrl = '/api/health';

    this.http.get<{ status: string }>(backendUrl).subscribe({
      next: (response) => {
        this.healthStatus.set(response.status);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.error.set('Failed to connect to backend: ' + err.message);
        this.isLoading.set(false);
      }
    });
  }
}
