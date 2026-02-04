
#!/usr/bin/env python3
##
## OwlMind Framework - experimentation environment for Generative Intelligence Systems.
## cli.py — Command-line interface.
##
# Copyright (c) 2025, The Generative Intelligence Lab
#    https://github.com/genilab/owlmind
#
# Disclosure:
# This framework was developed using a 'vibe coding' . AI-synthesized logic was 
# subjected to human review and manual refinement to guarantee functional 
# integrity and structural clarity.
#

import argparse
import os
import sys
import logging
from owlmind import __version__
from owlmind.models import Ollama


class Dispatcher:
    """Orchestrates components using the OwlMind Launch standards."""

    DEFAULT_LOG_LEVEL = Ollama.LOG_CRITICAL

    @staticmethod
    def load_env(filepath=".env"):
        """Manually parses a .env file and injects into os.environ."""
        if not os.path.exists(filepath):
            return
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key, value = key.strip(), value.strip().strip("'").strip('"')
                    if key not in os.environ:
                        os.environ[key] = value
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}", file=sys.stderr)

    @staticmethod
    def parse_params(raw_params: list) -> dict:
        """
        Parses parameters into a typed dictionary.
        Handles: -p k=v,k2=v2 AND -p k=v -p k2=v2
        """
        params = {}
        if not raw_params:
            return params

        tokens = []
        for item in raw_params:
            tokens.extend(item.split(","))

        for kv in tokens:
            if "=" not in kv:
                continue

            k, v = kv.split("=", 1)
            k, v = k.strip(), v.strip()

            if v.lower() == "true":
                v = True
            elif v.lower() == "false":
                v = False
            else:
                try:
                    v = int(v)
                except ValueError:
                    try:
                        v = float(v)
                    except ValueError:
                        pass

            params[k] = v

        return params

    @staticmethod
    def dispatch(args):
        # 1. Build initial context from argparse
        context = vars(args).copy()

        # 2. Resolve logging level (constants only)
        target_level = (
            Ollama.LOG_DEBUG if context.pop("debug", False)
            else Dispatcher.DEFAULT_LOG_LEVEL
        )

        logging.getLogger().setLevel(target_level)
        logging.getLogger("httpx").setLevel(target_level)

        context["log_level"] = target_level

        # 3. Dynamic Ollama parameters
        dynamic_params = Dispatcher.parse_params(context.pop("params", []))
        context.update(dynamic_params)

        # 4. Resolve payload (query only)
        if args.command == "query":
            payload = Dispatcher.resolve_prompt(args)
            if not payload:
                print("Error: No prompt provided.", file=sys.stderr)
                sys.exit(1)
            context["payload"] = payload

        # Remove argparse-only noise before passing context
        context.pop("command", None)
        context.pop("prompt", None)
        context.pop("input_file", None)

        # 5. Initialize Ollama with context
        api = Ollama(context=context)

        # 6. Obfuscate CLI plumbing
        api.obfuscate(["log_level"])

        # 7. Route command
        if args.command == "ping":
            Dispatcher.handle_ping(api)
        elif args.command == "info":
            Dispatcher.handle_info(api)
        elif args.command == "query":
            Dispatcher.handle_query(api)

    @staticmethod
    def resolve_prompt(args):
        if getattr(args, "input_file", None):
            return Dispatcher.load_file(args.input_file)
        prompt_val = getattr(args, "prompt", None)
        if prompt_val and prompt_val.startswith("@"):
            return Dispatcher.load_file(prompt_val[1:])
        return prompt_val

    @staticmethod
    def load_file(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error loading {filepath}: {e}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def handle_ping(api):
        status = "ONLINE" if api.ping() else "OFFLINE"
        print(f"Status: {status} (Host: {api.url})")

    @staticmethod
    def handle_info(api):
        data = api.info()

        print("-" * 40)
        print(f"Status  : {data['status']}")
        print(f"Host    : {api.url}")
        print(f"Model   : {api.model}")

        print("-" * 40)
        models_list = data.get("models", [])
        print(f"Available Models: {len(models_list)}")
        for m in models_list:
            print(f"  - {m}")

        print("-" * 40)
        params = data.get("parameters", [])
        print(f"Accepted Parameters ({len(params)}):")
        for p in params:
            print(f"  - {p}")

        print("-" * 40)


    @staticmethod
    def handle_query(api):
        if not api.ping():
            print(f"Error: Server {api.url} unreachable.", file=sys.stderr)
            sys.exit(1)

        if api.log_level == api.LOG_DEBUG:
            print(f"--- Inference: {api.model} ---")

        printed = False
        for chunk in api.step():
            print(chunk, end="", flush=True)
            printed = True

        # Always terminate output cleanly
        if printed:
            print()
        else:
            # Safety fallback: print payload if no chunks printed
            if api.payload:
                print(api.payload)


def get_parser():
    parser = argparse.ArgumentParser(prog="owlmind")

    param_list = ", ".join(Ollama.OLLAMA_PARAMS.keys())
    param_help = f"Supports k=v; (k1=v1,k2=v2), or multiple flags. Options: {param_list}"

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--debug", action="store_true", help="Enable verbose telemetry and internal logs")
    parser.add_argument("--url", default=os.environ.get("OLLAMA_HOST", Ollama.DEFAULT_SERVER))

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("ping")
    subparsers.add_parser("info")

    qp = subparsers.add_parser("query")
    qp.add_argument("prompt", nargs="?", default=None)
    qp.add_argument("--input", "-i", dest="input_file")
    qp.add_argument("--model", "-m", default=os.environ.get("OLLAMA_MODEL", Ollama.DEFAULT_MODEL))
    qp.add_argument("--params", "-p", action="append", dest="params", help=param_help)

    return parser


def main():
    Dispatcher.load_env()
    parser = get_parser()
    args = parser.parse_args()
    Dispatcher.dispatch(args)


if __name__ == "__main__":
    main()
