import { Component, signal } from '@angular/core';
import { Header } from './components/header/header';
import { FichaTecnica } from './components/ficha-tecnica/ficha-tecnica';
import { Evaluador } from './components/evaluador/evaluador';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [Header, FichaTecnica, Evaluador],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  // 'presentation' controla la ficha técnica, 'console' activa el laboratorio Rx
  currentStage = signal<'presentation' | 'console'>('presentation');

  navigateToConsole(): void {
    this.currentStage.set('console');
  }

  navigateToHome(): void {
    this.currentStage.set('presentation');
  }
}