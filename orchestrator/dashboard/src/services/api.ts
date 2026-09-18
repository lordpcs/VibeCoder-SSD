import {
  TaskResult,
  TaskDefinition,
  SystemBlueprint,
  SystemHealth,
} from '../types';

const API_BASE = window.location.origin.includes('5173')
  ? 'http://localhost:4040'
  : '';

export async function fetchTasks(): Promise<TaskResult[]> {
  const res = await fetch(`${API_BASE}/api/tasks`);
  if (!res.ok) throw new Error('Failed to fetch tasks');
  return res.json();
}

export async function submitTask(taskData: any): Promise<TaskResult> {
  const res = await fetch(`${API_BASE}/api/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData),
  });
  if (!res.ok) throw new Error('Failed to submit task');
  return res.json();
}

export async function cancelTask(taskId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/api/tasks/${taskId}/cancel`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to cancel task');
  return res.json();
}

export async function fetchBlueprint(): Promise<SystemBlueprint> {
  const res = await fetch(`${API_BASE}/api/specs/blueprint`);
  if (!res.ok) throw new Error('Failed to fetch blueprint');
  return res.json();
}

export async function validateSpecs(): Promise<any> {
  const res = await fetch(`${API_BASE}/api/specs/validate`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to validate specs');
  return res.json();
}

export async function compilePrompt(payload: {
  intent_vibe: string;
  target_component: string;
  assigned_agent: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/api/specs/compile-prompt`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to compile prompt');
  return res.json();
}

export async function fetchSystemHealth(): Promise<SystemHealth> {
  const res = await fetch(`${API_BASE}/api/agents/health`);
  if (!res.ok) throw new Error('Failed to fetch system health');
  return res.json();
}

export function createTerminalSocket(
  taskId: string,
  onMessage: (chunk: { task_id: string; stream: string; content: string }) => void
): WebSocket {
  const wsHost = window.location.origin.includes('5173')
    ? 'ws://localhost:4040'
    : window.location.origin.replace(/^http/, 'ws');

  const ws = new WebSocket(`${wsHost}/ws/terminal/${taskId}`);
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch {
      // raw text
    }
  };
  return ws;
}
