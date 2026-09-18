import React, { useEffect, useState } from 'react';
import { Header } from './components/Header';
import { MissionControl } from './components/MissionControl';
import { ActiveMissions } from './components/ActiveMissions';
import { TerminalStream } from './components/TerminalStream';
import { BlueprintStudio } from './components/BlueprintStudio';
import { ToolchainHealth } from './components/ToolchainHealth';
import { TaskResult, SystemBlueprint, SystemHealth } from './types';
import { fetchTasks, fetchBlueprint, fetchSystemHealth } from './services/api';

export function App() {
  const [activeTab, setActiveTab] = useState('missions');
  const [tasks, setTasks] = useState<TaskResult[]>([]);
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
  const [blueprint, setBlueprint] = useState<SystemBlueprint | null>(null);
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const loadData = async () => {
    setIsRefreshing(true);
    try {
      const [tasksData, bpData, healthData] = await Promise.all([
        fetchTasks().catch(() => []),
        fetchBlueprint().catch(() => null),
        fetchSystemHealth().catch(() => null),
      ]);
      setTasks(tasksData);
      setBlueprint(bpData);
      setHealth(healthData);

      if (tasksData.length > 0 && !selectedTaskId) {
        setSelectedTaskId(tasksData[0].task_id);
      }
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(() => {
      fetchTasks().then((t) => {
        setTasks(t);
      }).catch(() => {});
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const selectedTask = tasks.find((t) => t.task_id === selectedTaskId) || null;

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex flex-col">
      <Header
        health={health}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onRefresh={loadData}
        isRefreshing={isRefreshing}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
        {activeTab === 'missions' && (
          <div className="space-y-6">
            <MissionControl
              blueprint={blueprint}
              onMissionDispatched={loadData}
            />

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-5">
                <ActiveMissions
                  tasks={tasks}
                  selectedTaskId={selectedTaskId}
                  onSelectTask={setSelectedTaskId}
                  onRefresh={loadData}
                />
              </div>
              <div className="lg:col-span-7">
                <TerminalStream task={selectedTask} />
              </div>
            </div>
          </div>
        )}

        {activeTab === 'blueprint' && (
          <BlueprintStudio blueprint={blueprint} />
        )}

        {activeTab === 'health' && (
          <ToolchainHealth health={health} />
        )}
      </main>

      <footer className="border-t border-slate-900 py-4 px-6 text-center text-xs text-slate-500 font-mono">
        Vibe Coder Next &bull; Hybrid Vibe Coding & SDD Framework &bull; Port 4040
      </footer>
    </div>
  );
}

export default App;
