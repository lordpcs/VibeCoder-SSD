import React from 'react';
import { Terminal, Shield, Cpu, Activity, Sparkles, RefreshCw } from 'lucide-react';
import { SystemHealth } from '../types';

interface HeaderProps {
  health: SystemHealth | null;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onRefresh: () => void;
  isRefreshing: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  health,
  activeTab,
  setActiveTab,
  onRefresh,
  isRefreshing,
}) => {
  const tabs = [
    { id: 'missions', label: 'Mission Control', icon: Sparkles },
    { id: 'blueprint', label: 'SDD Blueprint Studio', icon: Shield },
    { id: 'health', label: 'Toolchain & Health', icon: Cpu },
  ];

  return (
    <header className="border-b border-slate-800 bg-[#0c1222]/80 backdrop-blur-md sticky top-0 z-40 px-6 py-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Logo & Title */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 via-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Terminal className="w-5 h-5 text-black stroke-[2.5]" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-slate-400">
                Vibe Coder Next
              </span>
              <span className="px-2 py-0.5 text-[10px] font-mono tracking-wider uppercase bg-cyan-950/80 border border-cyan-800/80 text-cyan-300 rounded-full font-semibold">
                SDD Hybrid
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Agentic Orchestrator &bull; Spec on the Trunk, Vibe on the Leaves
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center bg-slate-900/90 p-1 rounded-xl border border-slate-800">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  active
                    ? 'bg-gradient-to-r from-cyan-500 to-sky-600 text-black font-semibold shadow-md shadow-cyan-500/20'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            );
          })}
        </nav>

        {/* Telemetry Status Pill & Refresh */}
        <div className="flex items-center gap-3">
          {health && (
            <div className="flex items-center gap-2 bg-slate-900/80 border border-slate-800 px-3 py-1.5 rounded-xl text-xs font-mono">
              <div className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-slate-300">Tools:</span>
                <span className="text-emerald-400 font-semibold">
                  {health.tools_installed_count}/{health.tools_total_count}
                </span>
              </div>
              <span className="text-slate-700">|</span>
              <div className="text-slate-400">
                CPU: <span className="text-cyan-400">{health.metrics.cpu_percent}%</span>
              </div>
            </div>
          )}

          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition"
            title="Refresh state"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-cyan-400' : ''}`} />
          </button>
        </div>
      </div>
    </header>
  );
};
