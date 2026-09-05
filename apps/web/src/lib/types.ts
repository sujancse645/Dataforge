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
  prediction: string;
  ground_truth: string;
  correct: boolean;
  input_representation: string;
}

export interface ExperimentResult {
  experiment_id: string;
  task_family: string;
  demonstration_coverage: number;
  extrapolation_levels: number[];
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
