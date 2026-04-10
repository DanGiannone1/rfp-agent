"use client";

import { useRef, useCallback, useEffect, useState } from "react";
import { Plus, Box } from "lucide-react";
import BespokeIcon from "./ui/BespokeIcon";
import GlassPanel from "./ui/GlassPanel";
import WorkspaceLayout from "./layout/WorkspaceLayout";
import { useAgentSession } from "@/hooks/useAgentSession";
import { getFileContent } from "@/lib/api";
import { friendlyError } from "@/lib/utils";

import MessageList from "./MessageList";
import InputBar from "./InputBar";
import IntakeScreen from "./IntakeScreen";
import ArtifactsPanel from "./ArtifactsPanel";
import ArtifactCanvas from "./ArtifactCanvas";

export default function Chat() {
  const {
    state,
    statusMessage,
    isChatUploading,
    chatUploadName,
    handleIntakeUpload,
    handleSend,
    handleStop,
    handleChatUpload,
    doNewChat,
    startSession
  } = useAgentSession();

  const [artifact, setArtifact] = useState<{
    filename: string | null;
    content: string;
    mimeType: string | undefined;
    loading: boolean;
    error: string | null;
  }>({ filename: null, content: "", mimeType: undefined, loading: false, error: null });
  const [confirmNewChat, setConfirmNewChat] = useState(false);
  const lastAutoOpenedGenerated = useRef<string | null>(null);

  const uploadedFiles = state.files.filter(f => f.origin === "uploaded");
  const generatedFiles = state.files.filter(f => f.origin === "generated");
  const filesLoading = state.isInitializing;

  const handleOpenFile = useCallback(async (filename: string) => {
    if (!state.sessionId) return;
    setArtifact({ filename, content: "", mimeType: undefined, loading: true, error: null });
    try {
      let lastErr: unknown;
      for (let attempt = 0; attempt < 2; attempt++) {
        if (attempt > 0) await new Promise<void>((r) => setTimeout(r, 800));
        try {
          const data = await getFileContent(state.sessionId, filename);
          setArtifact(prev => ({ ...prev, content: data.content, mimeType: data.mime_type, loading: false }));
          return;
        } catch (err) { lastErr = err; }
      }
      setArtifact(prev => ({ ...prev, mimeType: undefined, loading: false, error: friendlyError(lastErr, "Could not load artifact.") }));
    } catch { }
  }, [state.sessionId]);

  useEffect(() => {
    if (state.isStreaming || generatedFiles.length === 0 || artifact.filename) return;
    const newest = generatedFiles[0]?.filename;
    if (!newest || lastAutoOpenedGenerated.current === newest) return;
    lastAutoOpenedGenerated.current = newest;
    queueMicrotask(() => {
      if (!state.isStreaming && !artifact.filename && generatedFiles[0]?.filename === newest) {
        void handleOpenFile(newest);
      }
    });
  }, [generatedFiles, state.isStreaming, artifact.filename, handleOpenFile]);

  const handleNewChat = useCallback(() => {
    if (state.messages.length > 0 || state.files.length > 0) { setConfirmNewChat(true); return; }
    void doNewChat();
  }, [state.messages.length, state.files.length, doNewChat]);

  const agentWorking = state.isStreaming || isChatUploading;

  if (state.stage === "intake") {
    return <IntakeScreen intake={state.intake} statusMessage={statusMessage} onUpload={handleIntakeUpload} onRetrySession={startSession} />;
  }

  const sidebar = (
    <ArtifactsPanel 
      uploadedFiles={uploadedFiles} 
      generatedFiles={generatedFiles} 
      loading={filesLoading} 
      onOpenFile={handleOpenFile} 
      disableActions={state.isStreaming} 
    />
  );

  const main = (
    <>
      <header className="h-16 flex items-center justify-between px-6 bg-surface-1/70 backdrop-blur-2xl rounded-3xl border border-border-subtle shadow-[0_8px_32px_rgba(0,0,0,0.5)]">
        <div className="flex items-center gap-3 font-bold tracking-wide">
          <div className={`p-1.5 rounded-lg bg-gradient-to-br from-brand-primary to-brand-warning shadow-[0_0_20px_rgba(217,93,57,0.4)] relative ${agentWorking ? "agent-working" : ""}`}>
            <div className="absolute inset-0 bg-white/20 rounded-lg blur-[2px]" />
            <BespokeIcon icon={Box} size={18} className="text-white" glowColor="rgba(255,255,255,0.5)" />
          </div>
          <span className="text-text-primary tracking-tighter">MERIDIAN</span>
        </div>

        <div className="hidden items-center gap-3 rounded-2xl border border-border-subtle bg-app/40 px-3 py-1.5 text-[11px] font-bold uppercase tracking-widest text-text-muted md:flex backdrop-blur-md">
          <span className={`h-1.5 w-1.5 rounded-full ${agentWorking ? "bg-brand-primary animate-pulse shadow-[0_0_10px_#D95D39]" : "bg-brand-success shadow-[0_0_10px_#7A9B76]"}`} />
          {agentWorking ? "Engine Active" : "Standby"}
          <span className="text-border-subtle">|</span>
          <span>{state.files.length} Unit{state.files.length === 1 ? "" : "s"}</span>
        </div>

        <button
          type="button"
          data-testid="new-chat-button"
          onClick={handleNewChat}
          disabled={state.isStreaming || state.isInitializing || isChatUploading}
          className="interactive-control inline-flex items-center justify-center rounded-xl bg-brand-primary px-4 py-2 text-[11px] font-bold uppercase tracking-widest text-white shadow-[0_4px_15px_rgba(217,93,57,0.3)] hover:bg-brand-warning transition-all disabled:opacity-45"
        >
          <Plus size={14} strokeWidth={3} className="mr-1" />
          New Session
        </button>
      </header>

      <GlassPanel variant="light" className="flex-1 flex flex-col min-h-0">
        <MessageList messages={state.messages} onSuggestion={state.isStreaming || state.isInitializing ? undefined : handleSend} />
        <InputBar
          onSend={handleSend}
          onUpload={handleChatUpload}
          disabled={state.isStreaming}
          isStreaming={state.isStreaming}
          onStop={handleStop}
          isUploadingFile={isChatUploading}
          uploadingFileName={chatUploadName}
        />
      </GlassPanel>
    </>
  );

  const canvas = (
    <ArtifactCanvas
      filename={artifact.filename}
      mimeType={artifact.mimeType}
      content={artifact.content}
      loading={artifact.loading}
      error={artifact.error}
      onClose={() => setArtifact(prev => ({ ...prev, filename: null }))}
    />
  );

  return (
    <>
      <WorkspaceLayout 
        sidebar={sidebar}
        main={main}
        canvas={canvas}
        isCanvasOpen={!!artifact.filename}
      />

      {confirmNewChat && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-app/80 backdrop-blur-md px-4" onClick={() => setConfirmNewChat(false)}>
          <div className="w-full max-w-sm rounded-[2rem] border border-border-subtle bg-surface-1 p-8 shadow-[0_32px_64px_rgba(0,0,0,0.6)] relative overflow-hidden" onClick={(e) => e.stopPropagation()}>
            <div className="absolute top-0 inset-x-0 h-1 bg-brand-warning" />
            <h2 className="text-lg font-bold text-text-primary uppercase tracking-wide">Reset Session?</h2>
            <p className="mt-3 text-sm text-text-muted leading-relaxed">This will purge current memory.</p>
            <div className="mt-8 flex flex-col gap-2">
              <button type="button" onClick={() => { setConfirmNewChat(false); void doNewChat(); }} className="interactive-control w-full rounded-xl bg-brand-warning py-3 text-xs font-bold uppercase tracking-widest text-white shadow-lg hover:brightness-110">Start new chat</button>
              <button type="button" onClick={() => setConfirmNewChat(false)} className="interactive-control w-full rounded-xl border border-border-subtle py-3 text-xs font-bold uppercase tracking-widest text-text-muted hover:bg-surface-2">Cancel</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
