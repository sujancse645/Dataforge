export interface LevelMetric {
  extrapolation_distance: number;
  accuracy: number;
  error_rate: number;
  total: number;
}

export interface PredictionResult {
  task_id: string;
  complexity: number;
  extrapolation_distance: number;
  input_representation: string;
  prediction: string;
  ground_truth: string;
  correct: boolean;
  raw_output: string;
  correctness: string;
  evaluator_name: string;
  model_name: string | null;
}

export interface RunConfig {
  experiment_id: string;
  task_family: string;
  demonstration_count: number;
  demonstration_complexity: number;
  extrapolation_levels: number[];
  tasks_per_level: number;
  master_seed: number;
  evaluator: string;
}

export interface ExperimentResult {
  experiment_id: string;
  config: RunConfig;
  demonstration_coverage: number;
  tasks_evaluated: number;
  level_metrics: Record<string, LevelMetric>;
  raw_results: PredictionResult[];
  cliff_detected: boolean;
  cliff_type: string;
  estimated_cliff_location: number | null;
}

export interface ExperimentConfig {
  master_seed: number;
  demonstration_count: number;
  demonstration_complexity: number;
  extrapolation_levels: number[];
  tasks_per_level: number;
  evaluator_type: string;
}

export interface Demonstration {
  demo_id: string;
  input_representation: string;
  expected_output: boolean;
  complexity: number;
}

export type ExperimentStreamEvent =
  | { type: 'demo_generated'; index: number; total: number; demo: Demonstration }
  | { type: 'coverage_computed'; coverage: number }
  | {
      type: 'task_evaluated';
      level: number;
      task_index: number;
      tasks_per_level: number;
      completed: number;
      total: number;
      result: PredictionResult;
    }
  | { type: 'level_complete'; level: number; metrics: LevelMetric }
  | { type: 'done'; result: ExperimentResult }
  | { type: 'error'; message: string };
