import React from 'react';
import {
  Play,
  CheckCircle2,
  XCircle,
  Clock,
  RotateCw,
  Ban,
  ShieldCheck,
  Terminal,
} from 'lucide-react';
import { TaskResult, TaskStatus } from '../types';
import { cancelTask } from '../services/api';

interface ActiveMissionsProps {
  tasks: TaskResult[];
  selectedTaskId: string | null;
  onSelectTask: (taskId: string) => void;
  onRefresh: () => void;
}

export const ActiveMissions: React.FC<ActiveMissionsProps> = ({
  tasks,
  selectedTaskId,
  onSelectTask,
  onRefresh,
}) => {
  const getStatusBadge = (status: TaskStatus) => {
    switch (status) {
      case 'running':
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-cyan-950/80 text-cyan-400 border border-cyan-800 animate-pulse">
            <RotateCw className="w-3 h-3 animate-spin" /> Running
          </span>
        );
      case 'verifying':
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-indigo-950/80 text-indigo-400 border border-indigo-800 animate-pulse">
            <ShieldCheck className="w-3 h-3" /> Verifying SDD
          </span>
        );
      case 'self_healing':
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-amber-950/80 text-amber-400 border border-amber-800 animate-pulse">
            <RotateCw className="w-3 h-3 animate-spin" /> Self-Healing
          </span>
        );
      case 'completed':
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-emerald-950/80 text-emerald-400 border border-emerald-800">
            <CheckCircle2 className="w-3 h-3" /> Passed
          </span>
        );
      case 'failed':
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-rose-950/80 text-rose-400 border border-rose-800">
            <XCircle className="w-3 h-3" /> Failed
          </span>
        );
      case 'cancelled':
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-slate-800 text-slate-400 border border-slate-700">
            <Ban className="w-3 h-3" /> Cancelled
          </span>
        );
      default:
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-slate-900 text-slate-400 border border-slate-800">
            <Clock className="w-3 h-3" /> Queued
          </span>
        );
    }
  };

  const handleCancel = async (e: React.MouseEvent, taskId: string) => {
    e.stopPropagation();
    try {
      await cancelTask(taskId);
      onRefresh();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800/90 rounded-2xl p-5 shadow-xl backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-white tracking-wide flex items-center gap-2">
          <span>Mission History & Queue</span>
          <span className="px-2 py-0.5 text-[10px] font-mono bg-slate-800 text-slate-300 rounded-full">
            {tasks.length}
          </span>
        </h3>
      </div>

      {tasks.length === 0 ? (
        <div className="py-12 text-center text-slate-500 text-xs font-mono">
          No missions dispatched yet. Enter a vibe above and click Dispatch!
        </div>
      ) : (
        <div className="space-y-2 max-h-[380px] overflow-y-auto pr-1">
          {tasks.map((task) => {
            const isSelected = selectedTaskId === task.task_id;
            const canCancel = ['running', 'verifying', 'self_healing'].includes(task.status);
            return (
              <div
                key={task.task_id}
                onClick={() => onSelectTask(task.task_id)}
                className={`p-3.5 rounded-xl border transition cursor-pointer flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 ${
                  isSelected
                    ? 'bg-slate-800/90 border-cyan-500/60 shadow-md shadow-cyan-500/10'
                    : 'bg-slate-950/40 border-slate-800/80 hover:bg-slate-800/40 hover:border-slate-700'
                }`}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    <span className="font-semibold text-xs text-slate-200 truncate">
                      {task.definition.title}
                    </span>
                    {getStatusBadge(task.status)}
                    <span className="text-[10px] font-mono text-slate-500 bg-slate-900/80 px-2 py-0.5 rounded border border-slate-800">
                      {task.definition.assigned_agent}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 truncate max-w-md">
                    {task.definition.intent_vibe}
                  </p>
                </div>

                <div className="flex items-center gap-2 text-xs">
                  {canCancel && (
                    <button
                      onClick={(e) => handleCancel(e, task.task_id)}
                      className="p-1.5 rounded-lg bg-rose-950/40 border border-rose-800 text-rose-400 hover:bg-rose-900/60 hover:text-white transition"
                      title="Cancel mission"
                    >
                      <Ban className="w-3.5 h-3.5" />
                    </button>
                  )}
                  <span className="text-[11px] font-mono text-slate-500">
                    {new Date(task.created_at).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
