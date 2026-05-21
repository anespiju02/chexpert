import { Component, output } from '@angular/core';

@Component({
  selector: 'app-header',
  standalone: true,
  templateUrl: './header.html',
  styleUrl: './header.scss'
})
export class Header {
  resetRequested = output<void>();

  onHomeClick(): void {
    this.resetRequested.emit();
  }
}