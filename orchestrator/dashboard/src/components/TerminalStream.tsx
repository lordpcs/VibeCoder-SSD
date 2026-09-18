import React, { useEffect, useState, useRef } from 'react';
import { Terminal as TerminalIcon, Copy, Trash2, ArrowDown, Check, AlertCircle } from 'lucide-react';
import { TaskResult } from '../types';
import { createTerminalSocket } from '../services/api';

interface TerminalStreamProps {
  task: TaskResult | null;
}

export const TerminalStream: React.FC<TerminalStreamProps> = ({ task }) => {
  const [logs, setLogs] = useState<string[]>([]);
  const [autoScroll, setAutoScroll] = useState(true);
  const [copied, setCopied] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!task) {
      setLogs([]);
      return;
    }

    setLogs([]);

    const ws = createTerminalSocket(task.task_id, (chunk) => {
      setLogs((prev) => [...prev, chunk.content]);
    });
    socketRef.current = ws;

    return () => {
      ws.close();
    };
  }, [task?.task_id]);

  useEffect(() => {
    if (autoScroll && bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs, autoScroll]);

  const handleCopy = () => {
    navigator.clipboard.writeText(logs.join(''));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!task) {
    return (
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-8 text-center text-slate-500 font-mono text-xs flex flex-col items-center justify-center min-h-[300px]">
        <TerminalIcon className="w-8 h-8 mb-2 stroke-1 text-slate-600" />
        Select or dispatch a mission to watch the real-time agent terminal stream.
      </div>
    );
  }

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl flex flex-col font-mono text-xs">
      {/* Terminal Titlebar */}
      <div className="bg-slate-900/90 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500/80" />
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
          </div>
          <span className="text-slate-400 font-semibold ml-2">
            Terminal Stream &bull; {task.task_id}
          </span>
          <span className="px-2 py-0.5 rounded text-[10px] bg-cyan-950 text-cyan-400 border border-cyan-800">
            {task.definition.assigned_agent}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setAutoScroll(!autoScroll)}
            className={`px-2 py-1 rounded text-[11px] border transition flex items-center gap-1 ${
              autoScroll
                ? 'bg-cyan-950/60 border-cyan-800 text-cyan-400'
                : 'bg-slate-800 border-slate-700 text-slate-400'
            }`}
          >
            <ArrowDown className="w-3 h-3" /> Auto-scroll
          </button>
          <button
            onClick={handleCopy}
            className="p-1 rounded bg-slate-800 text-slate-400 hover:text-white transition"
            title="Copy logs"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          </button>
          <button
            onClick={() => setLogs([])}
            className="p-1 rounded bg-slate-800 text-slate-400 hover:text-white transition"
            title="Clear terminal"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Verification Gates Summary Bar */}
      {task.verification_results && task.verification_results.length > 0 && (
        <div className="bg-slate-900/60 px-4 py-2 border-b border-slate-800/80 flex items-center gap-2 overflow-x-auto text-[11px]">
          <span className="text-slate-400 font-medium">Gates:</span>
          {task.verification_results.map((vr, i) => (
            <span
              key={i}
              className={`px-2 py-0.5 rounded font-mono border flex items-center gap-1 ${
                vr.passed
                  ? 'bg-emerald-950/60 border-emerald-800 text-emerald-300'
                  : 'bg-rose-950/60 border-rose-800 text-rose-300'
              }`}
            >
              {vr.passed ? '✓' : '✗'} {vr.command} ({vr.duration_ms}ms)
            </span>
          ))}
        </div>
      )}

      {/* Console output buffer */}
      <div className="p-4 overflow-y-auto max-h-[420px] min-h-[260px] text-slate-300 whitespace-pre-wrap leading-relaxed select-text">
        {logs.length === 0 ? (
          <span className="text-slate-600 animate-pulse">
            Connecting to agent output stream...
          </span>
        ) : (
          logs.map((line, index) => {
            let color = 'text-slate-300';
            if (line.includes('[SDD GATES]') || line.includes('[SDD CYCLE]')) {
              color = 'text-cyan-400 font-bold';
            } else if (line.includes('✅') || line.includes('PASSED') || line.includes('[SDD SUCCESS]')) {
              color = 'text-emerald-400';
            } else if (line.includes('❌') || line.includes('Failure') || line.includes('Error')) {
              color = 'text-rose-400';
            } else if (line.includes('[SELF-HEALING]')) {
              color = 'text-amber-400 font-semibold';
            }

            return (
              <span key={index} className={color}>
                {line}
              </span>
            );
          })
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};
