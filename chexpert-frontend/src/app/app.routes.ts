import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: '',
        loadComponent: () => import('./components/evaluador/evaluador').then(m => m.Evaluador)
    },
    {
        path: '**',
        redirectTo: '' // Redirecciona cualquier ruta rota a la pantalla principal
    }
];