type LogoMarkProps = {
  size?: number;
};

export const LogoMark = ({ size = 32 }: LogoMarkProps) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 64 64"
    aria-hidden="true"
    focusable="false"
  >
    <rect width="64" height="64" rx="16" fill="var(--color-primary)" />
    <path
      d="M10 34h10l5-12 8 22 6-16 4 6h11"
      fill="none"
      stroke="#ffffff"
      strokeWidth="5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <circle cx="54" cy="34" r="4" fill="var(--color-accent)" />
  </svg>
);
