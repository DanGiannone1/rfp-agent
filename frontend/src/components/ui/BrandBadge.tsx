"use client";

interface BrandBadgeProps {
  label: string;
  variant?: "terracotta" | "sage" | "gold" | "muted";
  size?: "xs" | "sm";
  glow?: boolean;
}

/**
 * Atomic Badge component for status and priority indicators.
 */
export default function BrandBadge({
  label,
  variant = "terracotta",
  size = "xs",
  glow = false,
}: BrandBadgeProps) {
  const variants = {
    terracotta: "bg-brand-primary/10 border-brand-primary/30 text-brand-primary",
    sage: "bg-brand-success/10 border-brand-success/30 text-brand-success",
    gold: "bg-brand-secondary/10 border-brand-secondary/30 text-brand-secondary",
    muted: "bg-surface-2 border-border-subtle text-text-muted",
  };

  const sizes = {
    xs: "px-1.5 py-0.5 text-[9px]",
    sm: "px-2.5 py-1 text-[11px]",
  };

  const glowClass = glow ? "shadow-[0_0_12px_rgba(217,93,57,0.2)]" : "";

  return (
    <span className={`rounded-md border font-bold uppercase tracking-widest transition-all duration-300 ${variants[variant]} ${sizes[size]} ${glowClass}`}>
      {label}
    </span>
  );
}
