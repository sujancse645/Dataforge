import { ExperimentConfig, ExperimentResult, ExperimentStreamEvent } from './types';

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

/**
 * Runs the experiment engine in real time: the backend streams one NDJSON
 * event per line as demonstrations are generated and each task is evaluated,
 * and `onEvent` fires as each line arrives so the UI can render live progress.
 */
export async function runExperimentStream(
  config: ExperimentConfig,
  onEvent: (event: ExperimentStreamEvent) => void | Promise<void>,
  signal?: AbortSignal
): Promise<void> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE}/api/v1/experiments/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
      signal,
    });
  } catch (err) {
    if (err instanceof DOMException && err.name === 'AbortError') throw err;
    throw new Error(`Cannot reach the experiment backend at ${API_BASE}. Make sure the FastAPI server (uvicorn) is running.`);
  }

  if (!response.ok || !response.body) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || `Experiment backend returned HTTP ${response.status}.`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  const consumeLine = async (line: string) => {
    if (!line.trim()) return;
    let event: ExperimentStreamEvent;
    try {
      event = JSON.parse(line) as ExperimentStreamEvent;
    } catch {
      throw new Error('Received a malformed event from the experiment engine.');
    }
    await onEvent(event);
  };

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() ?? '';
    for (const line of lines) await consumeLine(line);
  }
  await consumeLine(buffer);
}
