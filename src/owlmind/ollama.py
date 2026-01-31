
import ollama
from .model import Model

class Ollama(Model):
    """
    Ollama implementation of the Model interface.
    Ensures parameters are correctly mapped to the 'options' dictionary.
    """
    def __init__(self, host: str):
        super().__init__(host)
        # The host is passed directly to the Client constructor
        self.client = ollama.Client(host=self.host)

    def ping(self) -> bool:
        """Checks connectivity by attempting to list models."""
        try:
            self.client.list()
            return True
        except Exception:
            return False

    def info(self) -> list:
        """Fetches the list of available model names from the local server."""
        try:
            response = self.client.list()
            # Extracts model names from the 'models' key in the response dictionary
            return [m['model'] for m in response.get('models', [])]
        except Exception:
            return []

    def query(self, model: str, prompt: str, **options):
        """
        Executes a generation request.
        Crucial: Parameters like temperature MUST be inside the 'options' dict.
        """
        # Map our generic CLI terms to Ollama API specific keys
        # num_predict = Max Tokens
        # num_ctx     = Context Window size
        ollama_params = {
            'temperature': options.get('temperature'),
            'top_k': options.get('top_k'),
            'top_p': options.get('top_p'),
            'num_predict': options.get('max_tokens'),
            'num_ctx': options.get('num_ctx'),
            'seed': options.get('seed') # Added for reproducibility testing
        }

        # Filter out None values so the Ollama server uses its internal defaults
        # for any parameter the user didn't explicitly set via CLI flags.
        clean_options = {k: v for k, v in ollama_params.items() if v is not None}

        # The generate method takes model and prompt as top-level args,
        # but all sampling/tuning parameters go into the 'options' keyword argument.
        return self.client.generate(
            model=model,
            prompt=prompt,
            stream=True,
            options=clean_options
        )


