"use client";

interface WorkspaceSidebarProps {
  onNewChat?: () => void;
  disableNewChat?: boolean;
}

export default function WorkspaceSidebar({ onNewChat, disableNewChat = false }: WorkspaceSidebarProps) {
  return (
    <aside className="hidden w-80 shrink-0 border-r border-white/5 bg-surface-1/50 backdrop-blur-md p-4 lg:flex lg:flex-col lg:gap-5">
      <button
        type="button"
        data-testid="new-chat-button"
        onClick={onNewChat}
        disabled={disableNewChat}
        className="interactive-control inline-flex items-center justify-center gap-2 rounded-xl border border-brand/20 bg-brand/10 px-3 py-2 text-sm font-medium text-brand hover:bg-brand/15 disabled:cursor-not-allowed disabled:opacity-45"
      >
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        New chat
      </button>

      <section className="rounded-2xl border border-border-subtle bg-surface-2/40 p-3">
        <p className="inline-flex items-center gap-1.5 text-[11px] font-medium uppercase tracking-[0.14em] text-text-secondary">
          <span className="h-1.5 w-1.5 rounded-full bg-brand" />
          Session
        </p>
        <div className="mt-2 rounded-xl border border-border-subtle bg-surface-1 px-3 py-2 text-xs leading-relaxed text-text-secondary">
          One active workspace per chat. Start a new chat to reset context.
        </div>
      </section>
    </aside>
  );
}
