import argparse
import os
import sys
from .ollama import Ollama

class Dispatcher:
    """Orchestrates the execution of commands and resolves prompt sources."""

    @staticmethod
    def dispatch(args):
        """Primary router that handles prompt resolution before execution."""
        api = Ollama(host=args.host)

        if args.command == "ping":
            Dispatcher.handle_ping(api)
        elif args.command == "info":
            Dispatcher.handle_info(api, args)
        elif args.command == "query":
            # Resolve the prompt source (Raw text vs @file vs --input)
            final_prompt = Dispatcher.resolve_prompt(args)
            if not final_prompt:
                print("Error: No prompt provided. Use raw text, @file, or --input.", file=sys.stderr)
                sys.exit(1)
            
            # Update args with the loaded content for the handler
            args.prompt = final_prompt
            Dispatcher.handle_query(api, args)

    @staticmethod
    def resolve_prompt(args):
        """Determines the final prompt string based on priority."""
        # Priority 1: Explicit --input flag
        if getattr(args, 'input_file', None):
            return Dispatcher.load_file(args.input_file)
            
        # Priority 2: Shorthand @file syntax in the positional prompt
        if args.prompt and args.prompt.startswith("@"):
            return Dispatcher.load_file(args.prompt[1:]) # Strip '@'
            
        # Priority 3: Standard raw text
        return args.prompt

    @staticmethod
    def load_file(filepath):
        """Reads and returns file content safely."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Error: Prompt file not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file {filepath}: {e}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def handle_ping(api):
        status = "ONLINE" if api.ping() else "OFFLINE"
        print(f"Status: {status} ({api.host})")

    @staticmethod
    def handle_info(api, args):
        print("--- OwlMind Configuration ---")
        host_src = "ENV" if os.environ.get("OLLAMA_HOST") else "DEFAULT"
        model_src = "ENV" if os.environ.get("OLLAMA_MODEL") else "DEFAULT"
        active_model = getattr(args, 'model', os.environ.get("OLLAMA_MODEL", "llama3"))

        print(f"Active Host  : {args.host} ({host_src})")
        print(f"Active Model : {active_model} ({model_src})")
        print("-" * 30)

        if api.ping():
            models = api.info()
            print(f"Remote Models at {api.host}:")
            for m in models: print(f" - {m}")
        else:
            print("Remote Status: OFFLINE (Cannot fetch models)")

        print("-" * 30)
        print("HELP:")
        print("  To change model: export OLLAMA_MODEL=model_name")
        print("  To change host:  export OLLAMA_HOST=url")
        print("  To load prompt:  owlmind query @file.txt")
        print("-" * 30)

    @staticmethod
    def handle_query(api, args):
        if not api.ping():
            print(f"Error: Server {api.host} unreachable.", file=sys.stderr)
            sys.exit(1)

        stream = api.query(
            model=args.model,
            prompt=args.prompt,
            temperature=args.temperature,
            top_k=args.top_k,
            top_p=args.top_p,
            max_tokens=args.max_tokens,
            num_ctx=args.num_ctx
        )
        for chunk in stream:
            print(chunk['response'], end='', flush=True)
        print()

def get_parser():
    """Generates the argparse structure."""
    parser = argparse.ArgumentParser(prog="owlmind")
    parser.add_argument("--host", default=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))
    
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("ping")
    subparsers.add_parser("info")

    qp = subparsers.add_parser("query")
    qp.add_argument("prompt", nargs="?", default=None, help="Prompt text or @filename")
    qp.add_argument("--input", "-i", dest="input_file", help="Explicit path to a prompt file")
    
    # Model & Sampling Params
    qp.add_argument("--model", "-m", default=os.environ.get("OLLAMA_MODEL", "llama3"))
    qp.add_argument("--temp", "-t", type=float, default=0.8, dest="temperature")
    qp.add_argument("--top-k", "-k", type=int, default=40, dest="top_k")
    qp.add_argument("--top-p", "-p", type=float, default=0.9, dest="top_p")
    qp.add_argument("--max-tokens", "-n", type=int, default=128, dest="max_tokens")
    qp.add_argument("--ctx-size", "-c", type=int, default=2048, dest="num_ctx")

    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    Dispatcher.dispatch(args)

if __name__ == "__main__":
    main()


