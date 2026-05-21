import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiResponse } from '../models/response/apiResponse.interface';

@Injectable({
  providedIn: 'root',
})
export class DiagnosticService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/predict';

  uploadAndPredict(file: File): Observable<ApiResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<ApiResponse>(this.apiUrl, formData);
  }
}
