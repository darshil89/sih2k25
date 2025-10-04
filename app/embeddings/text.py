import torch
from transformers import CLIPProcessor, CLIPModel
import logging
from typing import List, Union
import numpy as np

logger = logging.getLogger(__name__)

class CLIPTextEmbedder:
    
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        "Initialize CLIP model for text embedding"
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        try:
            # Load CLIP model and processor
            self.model = CLIPModel.from_pretrained(model_name)
            self.processor = CLIPProcessor.from_pretrained(model_name)
            
            # Move model to device
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"CLIP model '{model_name}' loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Failed to load CLIP model: {e}")
            raise
    
    def embed_text(self, text: Union[str, List[str]]) -> np.ndarray:
        "Generate embeddings for text using CLIP model"
        try:
            # Ensure text is a list
            if isinstance(text, str):
                text = [text]
            
            # Process text through CLIP
            inputs = self.processor(text=text, return_tensors="pt", padding=True, truncation=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embeddings
            with torch.no_grad():
                text_features = self.model.get_text_features(**inputs)
                # Normalize embeddings
                text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            
            # Convert to numpy and move to CPU
            embeddings = text_features.cpu().numpy()
            
            logger.info(f"Generated embeddings for {len(text)} text(s), shape: {embeddings.shape}")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating text embeddings: {e}")
            raise
    
    def embed_single_text(self, text: str) -> np.ndarray:
        "Generate embedding for a single text string"
        embeddings = self.embed_text(text)
        return embeddings[0]
    
    def get_embedding_dimension(self) -> int:
        "Get the dimension of the embeddings"
        return self.model.config.text_config.hidden_size

# Global CLIP embedder instance
clip_embedder = None

def get_clip_embedder() -> CLIPTextEmbedder:
    "Get or create global CLIP embedder instance"
    global clip_embedder
    if clip_embedder is None:
        clip_embedder = CLIPTextEmbedder()
    return clip_embedder

def embed_text_data(text: Union[str, List[str]]) -> np.ndarray:
    "Convenience function to embed text data using CLIP"
    embedder = get_clip_embedder()
    return embedder.embed_text(text)

def embed_single_text_data(text: str) -> np.ndarray:
    "Convenience function to embed a single text string using CLIP"
    embedder = get_clip_embedder()
    return embedder.embed_single_text(text)
