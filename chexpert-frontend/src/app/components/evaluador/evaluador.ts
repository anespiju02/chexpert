import { Component, inject, signal } from '@angular/core';
import { DiagnosticService } from '../../core/services/diagnostic.service';
import { DecimalPipe } from '@angular/common';
import { Prediction } from '../../core/models/response/prediction.interface';

@Component({
  selector: 'app-evaluador',
  standalone: true,
  imports: [DecimalPipe],
  templateUrl: './evaluador.html',
  styleUrl: './evaluador.scss'
})
export class Evaluador {
  private diagnosticService = inject(DiagnosticService);

  imagePreview = signal<string | null>(null);
  selectedFile = signal<File | null>(null);
  predictions = signal<Prediction[]>([]);
  isLoading = signal<boolean>(false);
  errorMessage = signal<string | null>(null);
  selectedGender = signal<string>('Male');
  
  // NUEVO: Signal para almacenar el feedback de metadatos del backend
  processedMetadata = signal<any>(null);

  onGenderChanged(event: Event): void {
    const selectElement = event.target as HTMLSelectElement;
    this.selectedGender.set(selectElement.value);
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      this.selectedFile.set(file);
      this.errorMessage.set(null);
      this.predictions.set([]);
      this.processedMetadata.set(null); // Limpiamos metadatos anteriores

      const reader = new FileReader();
      reader.onload = () => this.imagePreview.set(reader.result as string);
      reader.readAsDataURL(file);
    }
  }

  evaluateImage(): void {
    const file = this.selectedFile();
    if (!file) return;

    this.isLoading.set(true);
    this.errorMessage.set(null);
    this.predictions.set([]);
    this.processedMetadata.set(null);

    this.diagnosticService.uploadAndPredict(file, this.selectedGender()).subscribe({
      next: (res: any) => {
        this.isLoading.set(false);
        
        // ADAPTACIÓN DEL JSON: Validamos que el estatus sea "success"
        if (res && res.status === 'success' && res.predictions) {
          
          // Guardamos los metadatos de control (Género y valor numérico)
          this.processedMetadata.set(res.metadata_procesada);

          // MAPEADO DINÁMICO: Convertimos el objeto { "Cardiomegaly": 0.089, ... } en un Array []
          const mappedPredictions: Prediction[] = Object.keys(res.predictions).map(key => ({
            pathology: key,
            probability: res.predictions[key]
          }));

          // Ordenamos las predicciones de mayor a menor probabilidad para el informe clínico
          mappedPredictions.sort((a, b) => b.probability - a.probability);

          // Asignamos el array formateado al Signal que alimenta el HTML
          this.predictions.set(mappedPredictions);

        } else {
          this.errorMessage.set('La API no devolvió una estructura analítica válida.');
        }
      },
      error: () => {
        this.errorMessage.set('Fallo de comunicación con el nodo de inferencia Python.');
        this.isLoading.set(false);
      }
    });
  }
}