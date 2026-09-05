import { ExperimentConfig, ExperimentResult } from './types';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

export async function runExperiment(config: ExperimentConfig): Promise<ExperimentResult> {
  const response = await fetch(`${API_BASE}/api/v1/experiments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config),
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || 'Experiment server is unavailable.');
  }
  
  return response.json();
}
