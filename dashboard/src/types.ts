export type Status = 'planned' | 'in_progress' | 'blocked' | 'ready_for_validation' | 'accepted';
export interface Source { path: string; label: string; url: string }
export interface Delivery { number: number; url: string; state: 'merged' | 'open' | 'closed' | 'unknown' }
export interface Review { scope: string; packet: Source; delivery: Delivery | null }
export interface Step { id: string; title: string; verification: string; status: Status; note: string; features: string[]; acceptance: { reviewer: string; date: string; evidence: string } | null; validation: Review | null }
export interface Phase { id: number; title: string; owner: string; sections: Record<string, string>; steps: Step[]; features: string[]; status: Status; url: string }
export type CapabilityStatus = 'planned' | 'prototype' | 'partial' | 'implemented';
export interface CapabilityImplementation { status: CapabilityStatus; category: 'product' | 'runtime_lab' | 'experiment' | 'engineering'; scope: string; implemented: string[]; missing: string[]; work_items: string[]; blockers: string[]; acceptance: { reviewer: string; date: string; evidence: string } | null }
export interface Feature { id: string; title: string; verification: string; url: string; requirements: string[]; supportingWork: string[]; implementation: CapabilityImplementation }
export interface Work { id: string; title: string; status: 'implemented'; kind: 'implementation' | 'design'; requirements: string[]; how: string; sources: Source[]; verification: string; limitations: string; problems: string[] }
export interface Problem { id: string; title: string; status: 'open' | 'resolved'; kind: string; phases: number[]; requirements: string[]; detail: string; resolution: string; next_action: string; sources: Source[]; provenance: string }
export interface Board { schemaVersion: number; buildRevision: string; focusPhase: number; focusSummary: string; phases: Phase[]; features: Feature[]; workItems: Work[]; problems: Problem[]; snapshot: { date: string; commit: string; ci_url: string; ci_result: string; checks_passed: number; note: string; pull_requests: { number: number; state: string; draft: boolean }[] } }
