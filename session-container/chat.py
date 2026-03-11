"""Terminal chat loop — shows raw AG-UI events from the GitHub Copilot SDK.

Run from session-container/:
    uv run python chat.py [--working-dir /tmp/chat-workspace]

Each agent turn prints every raw SSE event as it arrives (including
reasoning/thinking tokens if the model emits them), then prints the
accumulated assistant text at the end of the turn.
"""

import argparse
import asyncio
import json
import tempfile
import uuid
from pathlib import Path

from ag_ui.core.events import (
    ReasoningMessageContentEvent,
    ReasoningMessageEndEvent,
    ReasoningMessageStartEvent,
)
from copilot.generated.session_events import SessionEventType

from agent import AgentSession, _sse_event


class DebugAgentSession(AgentSession):
    """AgentSession extended to surface reasoning/thinking tokens as AG-UI events."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._reasoning_message_id: str = ""
        self._reasoning_started: bool = False

    def _on_event(self, event) -> None:
        # Handle reasoning deltas before falling through to the base handler
        if event.type == SessionEventType.ASSISTANT_REASONING_DELTA:
            delta = getattr(event.data, "delta_content", None) or ""
            if not delta:
                return
            if not self._reasoning_started:
                self._reasoning_message_id = str(uuid.uuid4())
                self._reasoning_started = True
                self._enqueue(ReasoningMessageStartEvent(
                    message_id=self._reasoning_message_id,
                    role="assistant",
                ))
            self._enqueue(ReasoningMessageContentEvent(
                message_id=self._reasoning_message_id,
                delta=delta,
            ))
            return

        if event.type == SessionEventType.ASSISTANT_REASONING:
            # Reasoning phase complete — close the reasoning message if open
            if self._reasoning_started:
                self._enqueue(ReasoningMessageEndEvent(
                    message_id=self._reasoning_message_id,
                ))
                self._reasoning_started = False
                self._reasoning_message_id = ""
            return

        # All other events handled by the base class
        super()._on_event(event)

    async def send(self, prompt: str):
        # Reset reasoning state at the start of each turn
        self._reasoning_started = False
        self._reasoning_message_id = ""
        async for event in super().send(prompt):
            yield event


def _parse_event(raw: str) -> dict | None:
    line = raw.strip()
    if line.startswith("data: "):
        try:
            return json.loads(line[6:])
        except json.JSONDecodeError:
            return None
    return None


async def chat(working_dir: str) -> None:
    print(f"\n  Working dir : {working_dir}")
    print("  Type a message and press Enter. Ctrl-C or 'exit' to quit.\n")
    print("─" * 70)

    async with DebugAgentSession(working_dir) as session:
        while True:
            try:
                user_input = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye.")
                break

            if not user_input or user_input.lower() in ("exit", "quit"):
                print("Bye.")
                break

            print("\n── AG-UI events ──────────────────────────────────────────────────")
            accumulated_text: list[str] = []
            accumulated_reasoning: list[str] = []

            async for raw_event in session.send(user_input):
                evt = _parse_event(raw_event)
                if evt is None:
                    continue

                event_type = evt.get("type", "UNKNOWN")

                if event_type == "TEXT_MESSAGE_CONTENT":
                    delta = evt.get("delta", "")
                    accumulated_text.append(delta)
                    print(f"  TEXT          delta={repr(delta)}")

                elif event_type == "REASONING_MESSAGE_START":
                    print(f"  REASONING_START  id={evt.get('message_id','')[:8]}")

                elif event_type == "REASONING_MESSAGE_CONTENT":
                    delta = evt.get("delta", "")
                    accumulated_reasoning.append(delta)
                    print(f"  REASONING     delta={repr(delta)}")

                elif event_type == "REASONING_MESSAGE_END":
                    print(f"  REASONING_END    id={evt.get('message_id','')[:8]}")

                elif event_type == "TOOL_CALL_START":
                    print(f"  TOOL_START    name={evt.get('tool_call_name')}  id={evt.get('tool_call_id','')[:8]}")

                elif event_type == "TOOL_CALL_ARGS":
                    delta = evt.get("delta", "")
                    preview = delta[:120] + ("…" if len(delta) > 120 else "")
                    print(f"  TOOL_ARGS     {preview}")

                elif event_type == "TOOL_CALL_END":
                    print(f"  TOOL_END      id={evt.get('tool_call_id','')[:8]}")

                elif event_type == "RUN_FINISHED":
                    print(f"  RUN_FINISHED  thread={evt.get('thread_id','')[:8]}  run={evt.get('run_id','')[:8]}")

                elif event_type == "RUN_ERROR":
                    print(f"  RUN_ERROR     message={evt.get('message')}")

                else:
                    print(f"  {event_type:<20}  {json.dumps(evt)}")

            print("── End of turn ───────────────────────────────────────────────────")

            if accumulated_reasoning:
                print(f"\n<thinking>\n{''.join(accumulated_reasoning)}\n</thinking>")

            if accumulated_text:
                print(f"\nAssistant:\n{''.join(accumulated_text)}")
            else:
                print("\n(no text response)")

            print("─" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(description="Terminal chat with the RFP Agent")
    parser.add_argument(
        "--working-dir",
        default=None,
        help="Working directory for the agent (default: new temp dir)",
    )
    args = parser.parse_args()

    if args.working_dir:
        wd = args.working_dir
        Path(wd).mkdir(parents=True, exist_ok=True)
    else:
        wd = tempfile.mkdtemp(prefix="rfp-chat-")

    try:
        asyncio.run(chat(wd))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
