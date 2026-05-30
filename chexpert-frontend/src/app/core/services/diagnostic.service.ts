import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiResponse } from '../models/response/apiResponse.interface';

@Injectable({
  providedIn: 'root',
})
export class DiagnosticService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000/predict';

  uploadAndPredict(file: File, generoEspanol: string): Observable<ApiResponse> {
    const formData = new FormData();
    formData.append('file', file);

    // Extract nested ternary into a separate statement for clarity
    let generoIngles: string;
    if (generoEspanol === 'Masculino') {
      generoIngles = 'Male';
    } else if (generoEspanol === 'Femenino') {
      generoIngles = 'Female';
    } else {
      generoIngles = 'Unknown';
    }

    formData.append('genero', generoIngles);
    return this.http.post<ApiResponse>(this.apiUrl, formData);
  }
}
