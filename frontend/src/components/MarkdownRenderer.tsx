"use client";

import { useState, useCallback } from "react";
import { isValidElement, ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import type { Components } from "react-markdown";

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

type CodeElementProps = {
  className?: string;
  children?: ReactNode;
};

function getNodeText(node: ReactNode): string {
  if (typeof node === "string") return node;
  if (typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(getNodeText).join("");
  if (isValidElement<CodeElementProps>(node)) return getNodeText(node.props.children);
  return "";
}

function CodeBlock({ children, ...props }: React.ComponentPropsWithoutRef<"pre">) {
  const [copied, setCopied] = useState(false);
  const codeChild = Array.isArray(children) ? children[0] : children;
  const codeNode = isValidElement(codeChild) ? codeChild : null;
  const codeProps = isValidElement(codeNode) ? (codeNode.props as CodeElementProps) : {};
  const codeClassName = codeProps.className || "";
  const codeText = getNodeText(codeProps.children);
  const langMatch = codeClassName.match(/language-(\w+)/);
  const language = langMatch ? langMatch[1] : "text";

  const handleCopy = useCallback(() => {
    if (codeText) {
      navigator.clipboard.writeText(codeText);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    }
  }, [codeText]);

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
