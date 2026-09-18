export type TaskStatus =
  | 'pending'
  | 'queued'
  | 'running'
  | 'verifying'
  | 'self_healing'
  | 'completed'
  | 'failed'
  | 'cancelled';

export interface TaskConstraints {
  max_iterations: number;
  strict_types: boolean;
  preserve_tests: boolean;
  timeout_seconds: number;
}

export interface TaskDefinition {
  task_id: string;
  title: string;
  intent_vibe: string;
  target_component: string;
  target_spec?: string;
  affected_files?: string[];
  assigned_agent: string;
  constraints?: TaskConstraints;
  acceptance_criteria: string[];
  verification_commands?: string[];
}

export interface VerificationResult {
  passed: boolean;
  command: string;
  exit_code: number;
  output: string;
  duration_ms: number;
}

export interface TaskResult {
  task_id: string;
  status: TaskStatus;
  definition: TaskDefinition;
  logs: string[];
  iterations_run: number;
  verification_results: VerificationResult[];
  error_message?: string;
  created_at: string;
  completed_at?: string;
}

export interface ComponentDefinition {
  id: string;
  name: string;
  path: string;
  type: string;
  description: string;
  runtime?: string;
  port?: number;
  dependencies?: string[];
  invariants?: string[];
}

export interface AgentProfile {
  id: string;
  cli_command: string;
  provider: string;
  strengths: string[];
  env_key?: string;
}

export interface SystemBlueprint {
  version: string;
  project: {
    name: string;
    description: string;
    owner?: string;
    repository?: string;
  };
  architecture: {
    paradigm: string;
    tagline: string;
    ports?: Record<string, number>;
  };
  components: ComponentDefinition[];
  agent_profiles: AgentProfile[];
}

export interface ToolStatus {
  name: string;
  command: string;
  installed: boolean;
  version?: string;
  purpose: string;
}

export interface SystemHealth {
  status: string;
  timestamp: string;
  tools: ToolStatus[];
  tools_installed_count: number;
  tools_total_count: number;
  metrics: {
    cpu_percent: number;
    memory_percent: number;
    disk_free_gb: number;
    platform: string;
    python_version: string;
  };
  environment: Record<string, boolean>;
}
