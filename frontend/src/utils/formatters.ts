export const formatNumber = (value: number): string =>
  new Intl.NumberFormat("en-US").format(value);

export const formatPercentage = (value: number): string => `${value.toFixed(2)}%`;

export const formatDate = (value: string): string =>
  new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(`${value}T00:00:00`));
