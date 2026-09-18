import React, { useState } from 'react';
import { Send, Eye, ShieldAlert, Cpu, Sparkles, CheckCircle2, ChevronRight } from 'lucide-react';
import { SystemBlueprint } from '../types';
import { submitTask, compilePrompt } from '../services/api';

interface MissionControlProps {
  blueprint: SystemBlueprint | null;
  onMissionDispatched: () => void;
}

export const MissionControl: React.FC<MissionControlProps> = ({
  blueprint,
  onMissionDispatched,
}) => {
  const [vibePrompt, setVibePrompt] = useState('');
  const [selectedComponent, setSelectedComponent] = useState(
    blueprint?.components[0]?.id || 'sdd-spec-engine'
  );
  const [selectedAgent, setSelectedAgent] = useState('claude-code');
  const [previewContent, setPreviewContent] = useState<string | null>(null);
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; msg: string } | null>(null);

  const handlePreview = async () => {
    if (!vibePrompt.trim()) return;
    setIsLoadingPreview(true);
    setFeedback(null);
    try {
      const res = await compilePrompt({
        intent_vibe: vibePrompt,
        target_component: selectedComponent,
        assigned_agent: selectedAgent,
      });
      setPreviewContent(res.compiled_prompt);
    } catch (err: any) {
      setFeedback({ type: 'error', msg: err.message || 'Failed to compile prompt preview' });
    } finally {
      setIsLoadingPreview(false);
    }
  };

  const handleDispatch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!vibePrompt.trim()) return;

    setIsSubmitting(true);
    setFeedback(null);

    try {
      // First compile prompt and get synthesized manifest
      const compiled = await compilePrompt({
        intent_vibe: vibePrompt,
        target_component: selectedComponent,
        assigned_agent: selectedAgent,
      });

      // Submit task with synthesized manifest
      await submitTask(compiled.synthesized_manifest);
      setFeedback({ type: 'success', msg: `Mission dispatched: ${compiled.task_id}` });
      setVibePrompt('');
      setPreviewContent(null);
      onMissionDispatched();
    } catch (err: any) {
      setFeedback({ type: 'error', msg: err.message || 'Error dispatching mission' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800/90 rounded-2xl p-6 shadow-xl relative overflow-hidden backdrop-blur-sm">
      {/* Decorative gradient orb */}
      <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-cyan-400" />
          <h2 className="text-base font-semibold text-white tracking-wide">
            Vibe Instruction Dispatcher
          </h2>
        </div>
        <span className="text-xs text-slate-400 font-mono">
          Structured SDD Compilation
        </span>
      </div>

      <form onSubmit={handleDispatch} className="space-y-4">
        {/* Natural Language Vibe Input */}
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1.5 flex items-center justify-between">
            <span>Natural Language Vibe / Feature Intent</span>
            <span className="text-[11px] text-slate-500 font-normal">Press Ctrl + Enter to dispatch</span>
          </label>
          <textarea
            value={vibePrompt}
            onChange={(e) => setVibePrompt(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                handleDispatch();
              }
            }}
            placeholder="e.g. Implement GitHub OAuth login endpoint with secure JWT tokens and encrypted session cookies..."
            rows={3}
            className="w-full bg-slate-950/80 border border-slate-800 rounded-xl p-3.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition font-mono"
          />
        </div>

        {/* Configuration Row: Component + Agent */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              Target SDD Component
            </label>
            <select
              value={selectedComponent}
              onChange={(e) => setSelectedComponent(e.target.value)}
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 transition"
            >
              {blueprint?.components.map((comp) => (
                <option key={comp.id} value={comp.id}>
                  {comp.name} ({comp.path})
                </option>
              )) || <option value="general">Default Component</option>}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              Assigned AI Agent Runner
            </label>
            <select
              value={selectedAgent}
              onChange={(e) => setSelectedAgent(e.target.value)}
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 transition"
            >
              <option value="claude-code">Claude Code CLI (@anthropic-ai/claude-code)</option>
              <option value="codex">OpenAI Codex CLI (@openai/codex)</option>
              <option value="autonomous-subagent">Native Autonomous Subagent</option>
              <option value="mock-runner">SDD Simulation Runner (Safe Test Mode)</option>
            </select>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between pt-2">
          <button
            type="button"
            onClick={handlePreview}
            disabled={!vibePrompt.trim() || isLoadingPreview}
            className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-medium text-slate-300 bg-slate-800 hover:bg-slate-700 hover:text-white border border-slate-700/60 transition disabled:opacity-50"
          >
            <Eye className="w-3.5 h-3.5" />
            {isLoadingPreview ? 'Compiling...' : 'Preview SDD Packet'}
          </button>

          <button
            type="submit"
            disabled={!vibePrompt.trim() || isSubmitting}
            className="flex items-center gap-2 px-5 py-2 rounded-xl text-xs font-semibold text-black bg-gradient-to-r from-cyan-400 to-sky-400 hover:from-cyan-300 hover:to-sky-300 transition shadow-lg shadow-cyan-500/20 disabled:opacity-50"
          >
            <Send className="w-3.5 h-3.5" />
            {isSubmitting ? 'Dispatching...' : 'Dispatch Mission'}
          </button>
        </div>
      </form>

      {/* Feedback Alert */}
      {feedback && (
        <div
          className={`mt-4 p-3 rounded-xl border text-xs flex items-center gap-2 ${
            feedback.type === 'success'
              ? 'bg-emerald-950/50 border-emerald-800 text-emerald-300'
              : 'bg-rose-950/50 border-rose-800 text-rose-300'
          }`}
        >
          {feedback.type === 'success' ? (
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          ) : (
            <ShieldAlert className="w-4 h-4 text-rose-400" />
          )}
          <span>{feedback.msg}</span>
        </div>
      )}

      {/* Compiled Prompt Preview Modal / Drawer */}
      {previewContent && (
        <div className="mt-4 p-4 rounded-xl bg-slate-950/90 border border-slate-800 text-xs font-mono">
          <div className="flex items-center justify-between mb-2 text-slate-400">
            <span>Compiled SDD Instruction Payload</span>
            <button
              onClick={() => setPreviewContent(null)}
              className="text-slate-500 hover:text-white"
            >
              ✕ Close
            </button>
          </div>
          <pre className="overflow-x-auto text-slate-300 whitespace-pre-wrap max-h-60 overflow-y-auto">
            {previewContent}
          </pre>
        </div>
      )}
    </div>
  );
};
