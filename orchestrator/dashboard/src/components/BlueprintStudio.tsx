import React, { useState } from 'react';
import { Shield, Layers, FileCode, CheckCircle2, AlertTriangle, RefreshCw, ArrowRight } from 'lucide-react';
import { SystemBlueprint } from '../types';
import { validateSpecs } from '../services/api';

interface BlueprintStudioProps {
  blueprint: SystemBlueprint | null;
}

export const BlueprintStudio: React.FC<BlueprintStudioProps> = ({ blueprint }) => {
  const [validationResult, setValidationResult] = useState<any>(null);
  const [isValidating, setIsValidating] = useState(false);

  const handleValidate = async () => {
    setIsValidating(true);
    try {
      const res = await validateSpecs();
      setValidationResult(res);
    } catch (err: any) {
      setValidationResult({ valid: false, errors: [{ file: 'specs/', message: err.message }] });
    } finally {
      setIsValidating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Shield className="w-5 h-5 text-cyan-400" />
            <h2 className="text-base font-semibold text-white">
              System-Driven Development (SDD) Blueprint Studio
            </h2>
          </div>
          <p className="text-xs text-slate-400">
            Authoritative source of truth for components, schemas, API contracts, and quality invariants.
          </p>
        </div>

        <button
          onClick={handleValidate}
          disabled={isValidating}
          className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 transition shadow-sm"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isValidating ? 'animate-spin text-cyan-400' : ''}`} />
          {isValidating ? 'Validating Specs...' : 'Validate All Specs & Contracts'}
        </button>
      </div>

      {/* Validation Result Alert if available */}
      {validationResult && (
        <div
          className={`p-4 rounded-xl border text-xs ${
            validationResult.valid
              ? 'bg-emerald-950/40 border-emerald-800/80 text-emerald-300'
              : 'bg-rose-950/40 border-rose-800/80 text-rose-300'
          }`}
        >
          <div className="flex items-center gap-2 font-semibold mb-1">
            {validationResult.valid ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-rose-400" />
            )}
            <span>
              {validationResult.valid
                ? 'All SDD specifications, blueprints, and contracts are 100% valid.'
                : 'Validation errors detected in specification files:'}
            </span>
          </div>
          {validationResult.errors?.length > 0 && (
            <ul className="list-disc list-inside space-y-1 mt-2 text-rose-200">
              {validationResult.errors.map((err: any, i: number) => (
                <li key={i}>
                  <strong className="font-mono">{err.file}</strong>: {err.message}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* System Components Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {blueprint?.components.map((comp) => (
          <div
            key={comp.id}
            className="bg-slate-900/50 border border-slate-800/90 rounded-2xl p-5 hover:border-slate-700 transition flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-sm text-white flex items-center gap-2">
                  <Layers className="w-4 h-4 text-cyan-400" />
                  {comp.name}
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase bg-slate-800 text-slate-300 border border-slate-700">
                  {comp.type}
                </span>
              </div>

              <p className="text-xs text-slate-400 mb-4">{comp.description}</p>

              <div className="space-y-2 text-xs font-mono">
                <div className="flex items-center justify-between text-slate-500">
                  <span>Path:</span>
                  <span className="text-slate-300">{comp.path}</span>
                </div>
                {comp.runtime && (
                  <div className="flex items-center justify-between text-slate-500">
                    <span>Runtime:</span>
                    <span className="text-slate-300">{comp.runtime}</span>
                  </div>
                )}
                {comp.port && (
                  <div className="flex items-center justify-between text-slate-500">
                    <span>Port:</span>
                    <span className="text-cyan-400">{comp.port}</span>
                  </div>
                )}
              </div>
            </div>

            {comp.invariants && comp.invariants.length > 0 && (
              <div className="mt-4 pt-3 border-t border-slate-800/80">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                  Enforced Invariants
                </span>
                <ul className="text-xs text-slate-300 space-y-1">
                  {comp.invariants.map((inv, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <span className="text-cyan-400 font-bold">&bull;</span>
                      <span>{inv}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
