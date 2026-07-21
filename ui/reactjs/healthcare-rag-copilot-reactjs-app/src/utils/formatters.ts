export const percent = (value: number) => `${(value * 100).toFixed(1)}%`;
export const seconds = (value: number) => `${value.toFixed(2)}s`;
export const titleCase = (value: string) => value.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
