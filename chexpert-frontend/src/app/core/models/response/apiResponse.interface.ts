import { Prediction } from "./prediction.interface";

export interface ApiResponse {
    success: boolean;
    error?: string;
    predictions?: Prediction[];
}