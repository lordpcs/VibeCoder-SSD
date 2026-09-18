import React from 'react';
import { Cpu, CheckCircle2, XCircle, Key, HardDrive, ShieldCheck, Server } from 'lucide-react';
import { SystemHealth } from '../types';

interface ToolchainHealthProps {
  health: SystemHealth | null;
}

export const ToolchainHealth: React.FC<ToolchainHealthProps> = ({ health }) => {
  if (!health) {
    return (
      <div className="py-12 text-center text-slate-500 font-mono text-xs">
        Loading system telemetry...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-1">
            <span>Tools Operational</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">
            {health.tools_installed_count} / {health.tools_total_count}
          </div>
          <div className="text-[11px] text-emerald-400 mt-1">
            {health.tools_installed_count === health.tools_total_count
              ? 'Complete 13/13 Toolchain'
              : 'Containerized Tools Available'}
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-1">
            <span>CPU Utilization</span>
            <Cpu className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">
            {health.metrics.cpu_percent}%
          </div>
          <div className="text-[11px] text-slate-400 mt-1 font-mono">
            {health.metrics.platform}
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-1">
            <span>Memory Usage</span>
            <Server className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">
            {health.metrics.memory_percent}%
          </div>
          <div className="text-[11px] text-slate-400 mt-1 font-mono">
            Python {health.metrics.python_version}
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-1">
            <span>Free Disk Space</span>
            <HardDrive className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">
            {health.metrics.disk_free_gb} GB
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            Docker Workspace Volume
          </div>
        </div>
      </div>

      {/* API Keys Configuration Status */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5">
        <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
          <Key className="w-4 h-4 text-cyan-400" />
          Agent Authentication & API Credentials
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {Object.entries(health.environment).map(([key, isSet]) => (
            <div
              key={key}
              className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between"
            >
              <div className="text-xs font-mono text-slate-300">{key}</div>
              {isSet ? (
                <span className="flex items-center gap-1 text-[11px] font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800">
                  <CheckCircle2 className="w-3 h-3" /> Configured
                </span>
              ) : (
                <span className="flex items-center gap-1 text-[11px] font-mono text-slate-500 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                  Unset (.env)
                </span>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 13/13 Tools Grid */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5">
        <h3 className="text-sm font-semibold text-white mb-4">
          Vibe Coder Complete Toolchain (13 CLI Tools)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {health.tools.map((tool) => (
            <div
              key={tool.name}
              className="p-3.5 rounded-xl bg-slate-950/50 border border-slate-800/80 hover:border-slate-700 transition flex flex-col justify-between"
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-semibold text-xs text-white">
                  {tool.name}
                </span>
                {tool.installed ? (
                  <span className="flex items-center gap-1 text-[10px] font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800">
                    <CheckCircle2 className="w-3 h-3" /> Ready
                  </span>
                ) : (
                  <span className="flex items-center gap-1 text-[10px] font-mono text-slate-500 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                    In Container
                  </span>
                )}
              </div>
              <p className="text-[11px] text-slate-400 mb-2">{tool.purpose}</p>
              <div className="text-[10px] font-mono text-slate-500 bg-slate-900/80 px-2 py-1 rounded truncate">
                {tool.version || `$ ${tool.command}`}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
