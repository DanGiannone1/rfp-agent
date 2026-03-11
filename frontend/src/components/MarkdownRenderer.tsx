"use client";

import { useState, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import type { Components } from "react-markdown";

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

function CodeBlock({ children, ...props }: React.ComponentPropsWithoutRef<"pre">) {
  const [copied, setCopied] = useState(false);
  const codeChild = Array.isArray(children) ? children[0] : children;
  const codeClassName = (codeChild as any)?.props?.className || "";
  const langMatch = codeClassName.match(/language-(\w+)/);
  const language = langMatch ? langMatch[1] : "text";

  const handleCopy = useCallback(() => {
    const text = (codeChild as any)?.props?.children;
    if (typeof text === "string") {
      navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    }
  }, [codeChild]);

  return (
    <div className="code-block-wrapper">
      <div className="code-block-header">
        <span className="code-block-lang">{language}</span>
        <button type="button" onClick={handleCopy} className="code-block-copy">
          {copied ? "COPIED" : "COPY"}
        </button>
      </div>
      <pre {...props}>{children}</pre>
    </div>
  );
}

const markdownComponents: Components = {
  pre: CodeBlock,
};

export default function MarkdownRenderer({ content, className = "" }: MarkdownRendererProps) {
  return (
    <div className={`prose prose-message ${className}`}>
      <ReactMarkdown 
        remarkPlugins={[remarkGfm]} 
        rehypePlugins={[rehypeHighlight]} 
        components={markdownComponents}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
