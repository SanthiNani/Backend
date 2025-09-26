# models/health_llm.py
from transformers import (
    AutoModelForCausalLM,
    AutoModel,
    AutoTokenizer,
    pipeline,
    logging
)
from config import settings
import torch

# Suppress excessive warnings
logging.set_verbosity_error()

class HealthLLM:
    def __init__(self, model_name: str = None, api_key: str = None):
        self.model_name = model_name or settings.HUGGINGFACE_MODEL_NAME
        self.api_key = api_key or settings.HUGGINGFACE_API_KEY
        self.tokenizer = None
        self.model = None
        self.generator = None
        self.is_causal = False  # True if model is text-generation capable
        self._load_model()

    def _load_model(self):
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=self.api_key)

            # Detect model type for causal LM or embeddings
            if "gpt" in self.model_name.lower() or "lm" in self.model_name.lower():
                # Text-generation model
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name, token=self.api_key)
                self.generator = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    device=0 if torch.cuda.is_available() else -1
                )
                self.is_causal = True
                print(f"[INFO] Causal LM '{self.model_name}' loaded successfully for text generation.")
            else:
                # Embedding / masked model
                self.model = AutoModel.from_pretrained(self.model_name, token=self.api_key)
                self.is_causal = False
                print(f"[INFO] Embedding/masked model '{self.model_name}' loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to load model '{self.model_name}': {e}")

    def generate_response(self, prompt: str, max_length: int = 200, temperature: float = 0.7):
        if not self.is_causal or not self.generator:
            raise ValueError(
                f"Model '{self.model_name}' is not a text-generation model. "
                "Use an embedding model for NLP tasks instead."
            )
        try:
            responses = self.generator(prompt, max_length=max_length, temperature=temperature, do_sample=True)
            return responses[0]['generated_text']
        except Exception as e:
            print(f"[ERROR] Failed to generate response: {e}")
            return "Sorry, I couldn't generate a response at this time."

    def encode_text(self, text: str):
        """
        Returns embeddings for the input text.
        Works with masked/embedding models like DistilBERT.
        """
        if self.is_causal:
            raise ValueError("Text encoding is only supported for embedding models.")
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
            # Use mean of last hidden states as embedding
            embeddings = outputs.last_hidden_state.mean(dim=1)
            return embeddings.squeeze().numpy()
        except Exception as e:
            print(f"[ERROR] Failed to encode text: {e}")
            return None
