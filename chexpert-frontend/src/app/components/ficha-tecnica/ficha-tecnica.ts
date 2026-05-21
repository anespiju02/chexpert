import { Component, output } from '@angular/core';

@Component({
  selector: 'app-ficha-tecnica',
  standalone: true,
  templateUrl: './ficha-tecnica.html',
  styleUrl: './ficha-tecnica.scss',
})
export class FichaTecnica {
  actionTriggered = output<void>();
}