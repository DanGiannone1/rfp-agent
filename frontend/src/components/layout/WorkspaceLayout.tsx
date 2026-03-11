"use client";

import { motion, AnimatePresence } from "framer-motion";
import { ReactNode } from "react";

interface WorkspaceLayoutProps {
  sidebar: ReactNode;
  main: ReactNode;
  canvas?: ReactNode;
  isCanvasOpen: boolean;
}

/**
 * Orchestrates the 3-pane spatial layout with fluid Framer Motion transitions.
 */
export default function WorkspaceLayout({
  sidebar,
  main,
  canvas,
  isCanvasOpen
}: WorkspaceLayoutProps) {
  return (
    <div className="relative flex h-screen w-full bg-app p-3 gap-3 text-text-primary font-sans overflow-hidden">
      {/* Background Decorations */}
      <div className="ambient-orb-1 animate-blob" />
      <div className="ambient-orb-2 animate-blob" />

      <motion.div layout className="relative z-10 flex h-full w-full gap-3">
        {/* Slot 1: Sidebar */}
        {sidebar}

        {/* Slot 2: Main Content (Chat) */}
        <motion.div 
          layout
          className={`flex flex-col gap-3 min-w-0 transition-all duration-500 ${
            isCanvasOpen ? "w-[40%] min-w-[380px] shrink-0" : "flex-1"
          }`}
        >
          {main}
        </motion.div>

        {/* Slot 3: Canvas (Optional) */}
        <AnimatePresence>
          {isCanvasOpen && canvas && (
            <motion.div
              initial={{ x: 100, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 100, opacity: 0 }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="flex flex-1 min-w-0 h-full"
            >
              {canvas}
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
