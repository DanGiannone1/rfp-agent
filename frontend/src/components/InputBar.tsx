"use client";

import { useState, FormEvent } from "react";

interface InputBarProps {
  onSend: (message: string) => void;
  disabled: boolean;
}

export default function InputBar({ onSend, disabled }: InputBarProps) {
  const [input, setInput] = useState("");

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setInput("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="glass border-t border-border-subtle"
    >
      <div className="mx-auto flex max-w-3xl gap-2 px-4 py-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Send a message..."
          disabled={disabled}
          className="flex-1 rounded-full border border-zinc-700/50 bg-zinc-800/50 px-4 py-2 text-sm text-zinc-100 outline-none placeholder:text-zinc-500 focus:border-indigo-500/50 focus:ring-2 focus:ring-indigo-500/20 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={disabled || !input.trim()}
          className="accent-gradient rounded-full px-4 py-2 text-sm font-medium text-white shadow-lg shadow-indigo-500/20 transition-all hover:brightness-110 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </form>
  );
}
