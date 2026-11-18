import type { Board } from './src/types';
export function jsonForHtml(value: unknown): string;
export function hash(value: string): string;
export function htmlFor(data: Board): Promise<string>;

export function textForHtml(value: string): string;
export function validateBundledInputs(inputs: Record<string, unknown>): void;
