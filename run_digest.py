#!/usr/bin/env python3
"""
AI/ML News Digest — session runner
Starts a Claude Managed Agent session and triggers the daily digest.

Usage:
    python run_digest.py

Environment variables required:
    ANTHROPIC_API_KEY   — your Anthropic API key
    AGENT_ID            — agent_011CaQoxTVTeDgbvAv6ZwwWu
    ENVIRONMENT_ID      — your aiml-news-digest-env environment ID
    VAULT_ID            — vlt_011CaQpHKbxxhiQko3rdLkGY
"""

import os
import time
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

AGENT_ID      = os.environ.get("AGENT_ID", "agent_011CaQoxTVTeDgbvAv6ZwwWu")
ENVIRONMENT_ID = os.environ["ENVIRONMENT_ID"]
VAULT_ID      = os.environ.get("VAULT_ID", "vlt_011CaQpHKbxxhiQko3rdLkGY")


def run_digest():
    print("Starting AI/ML digest session...")

    # Create session
    session = client.beta.sessions.create(
        agent={"type": "agent", "id": AGENT_ID},
        environment_id=ENVIRONMENT_ID,
        vault_ids=[VAULT_ID],
        title="Daily AI/ML Digest",
    )
    print(f"Session created: {session.id}")

    # Send trigger message
    client.beta.sessions.events.send(
        session_id=session.id,
        events=[{
            "type": "user.message",
            "content": [{"type": "text", "text": "Run the digest for today."}],
        }],
    )
    print("Trigger sent. Waiting for completion...")

    # Poll until idle
    poll_interval = 10
    max_wait = 600  # 10 minutes
    elapsed = 0

    while elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed += poll_interval

        events = client.beta.sessions.events.list(session_id=session.id)
        for event in events.data:
            if event.type == "session.status_idle":
                print(f"Digest complete after {elapsed}s.")
                return
            if event.type == "session.error":
                print(f"Session error: {event}")
                return

        print(f"  Still running... ({elapsed}s elapsed)")

    print("Timed out waiting for session to complete.")


if __name__ == "__main__":
    run_digest()
