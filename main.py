"""CLI for the RFP analysis agent.

Usage:
    uv run python main.py                        # interactive chat
    uv run python main.py "analyze the RFP docs" # one-shot
"""

import asyncio
import json
import os
import sys

from agent import AgentSession, run_analysis


def print_events(sse_line: str) -> bool:
    """Parse an SSE line and print it. Returns True if it was a terminal event."""
    text = sse_line.strip()
    if not text.startswith("data: "):
        return False

    event = json.loads(text.removeprefix("data: "))
    event_type = event.get("type")

    if event_type == "delta":
        print(event["content"], end="", flush=True)
    elif event_type == "tool_start":
        print(f"\n  [{event['tool']}] running...", flush=True)
    elif event_type == "tool_end":
        print(f"  [{event['tool']}] done", flush=True)
    elif event_type == "message":
        pass  # full message already streamed via deltas
    elif event_type == "done":
        print()
        return True
    elif event_type == "error":
        print(f"\n[Agent] Error: {event['message']}", file=sys.stderr)
        return True

    return False


async def one_shot(prompt: str, working_dir: str):
    """Run a single prompt and exit."""
    print(f"[Agent] Working directory: {working_dir}")
    print(f"[Agent] Prompt: {prompt}\n")

    async for sse_line in run_analysis(prompt, working_dir):
        print_events(sse_line)

    print("\n[Agent] Done.")


async def interactive(working_dir: str):
    """Run an interactive multi-turn chat session."""
    print(f"[Agent] Working directory: {working_dir}")
    print("[Agent] Interactive mode — type 'exit' or 'quit' to stop.\n")

    async with AgentSession(working_dir) as session:
        while True:
            try:
                prompt = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not prompt:
                continue
            if prompt.lower() in ("exit", "quit"):
                break

            async for sse_line in session.send(prompt):
                print_events(sse_line)
            print()

    print("[Agent] Session closed.")


def main():
    working_dir = os.getenv("WORKING_DIR", "./workspace")

    if len(sys.argv) >= 2:
        asyncio.run(one_shot(sys.argv[1], working_dir))
    else:
        asyncio.run(interactive(working_dir))


main()
