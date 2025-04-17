#!/usr/bin/env python3
"""
ask_gpt.py

Usage:
  ask_gpt.py -m MODEL "your prompt here"

Example:
  ./ask_gpt.py -m gpt-4o "Write a command that lists all the files in this directory and then deletes the ones starting with the letter a"
"""

import os
import argparse
import subprocess
import openai
from dotenv import load_dotenv

load_dotenv()

def ask_gpt(prompt: str, model: str = "gpt-4o") -> str:
    """
    Send `prompt` to OpenAI and return the assistant's response text.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("Please set the OPENAI_API_KEY environment variable")

    resp = openai.responses.create(
        model=model,
        instructions="You are a helpful assistant that outputs shell commands only that can be copied and pasted directly into a terminal. Add no additional formatting or markdown syntax.",
        input=prompt
    )
    # Grab the assistant’s reply
    text = resp.output_text.strip()
    return text

def main():
    parser = argparse.ArgumentParser(description="Generate and optionally run shell commands via GPT")
    parser.add_argument(
        "-m", "--model",
        default="gpt-4o",
        help="OpenAI model to use (e.g. gpt-4o, gpt-3.5-turbo)"
    )
    parser.add_argument(
        "prompt",
        nargs="+",
        help="The question or instruction for GPT (in quotes)"
    )
    args = parser.parse_args()
    full_prompt = " ".join(args.prompt)

    try:
        command = ask_gpt(full_prompt, args.model)
    except Exception as e:
        print(f"Failed to call OpenAI API: {e}")
        return

    print("\nThe command is:\n")
    print(f"  {command}\n")

    run_it = input("⚙️  Would you like to run it? [Y/n] ").strip().lower()
    if run_it in ("", "y", "yes"):
        print("Executing command…\n")
        # Note: shell=True lets you use pipes, redirects, etc.
        subprocess.run(command, shell=True)
    else:
        print("🚫 Aborted.")

if __name__ == "__main__":
    main()
