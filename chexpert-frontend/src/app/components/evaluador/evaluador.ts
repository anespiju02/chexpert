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
  private readonly diagnosticService = inject(DiagnosticService);

  imagePreview = signal<string | null>(null);
  selectedFile = signal<File | null>(null);
  predictions = signal<Prediction[]>([]);
  isLoading = signal<boolean>(false);
  errorMessage = signal<string | null>(null);
  
  // NUEVO: Signal reactivo para almacenar el género seleccionado
  selectedGender = signal<string>('Masculino');

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

    // Modificación de la llamada al servicio: 
    // Recuerda actualizar la firma en diagnostic.service.ts para que reciba (file, genero)
    this.diagnosticService.uploadAndPredict(file, this.selectedGender()).subscribe({
      next: (res) => {
        this.isLoading.set(false);
        if (res.success && res.predictions) {
          this.predictions.set(res.predictions);
        } else {
          this.errorMessage.set(res.error || 'Error de validación analítica.');
        }
      },
      error: () => {
        this.errorMessage.set('Fallo de conexión con el nodo de inferencia Python.');
        this.isLoading.set(false);
      }
    });
  }
}