import torch
from transformers import CLIPProcessor, CLIPModel
import logging
from typing import List, Union
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

class CLIPImageEmbedder:
    
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        "Initialize CLIP model for image embedding"
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
        
    def embed_image(self, image: Union[str, np.ndarray, Image.Image]) -> np.ndarray:
        "Generate embeddings for image using CLIP model"
        try:
            # Handle different input types
            if isinstance(image, str):
                # Check if it's a URL or file path
                if image.startswith(('http://', 'https://')):
                    # Download image from URL
                    import requests
                    import io
                    response = requests.get(image)
                    response.raise_for_status()
                    image = Image.open(io.BytesIO(response.content))
                else:
                    # Load image from file path
                    image = Image.open(image)
            elif isinstance(image, np.ndarray):
                # Convert numpy array to PIL Image
                image = Image.fromarray(image)
            
            # Process image through CLIP
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embeddings
            with torch.no_grad():
                image_features = self.model.get_image_features(**inputs)
                # Normalize embeddings
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            
            # Convert to numpy and move to CPU
            embeddings = image_features.cpu().numpy()
            
            logger.info(f"Generated embeddings for image, shape: {embeddings.shape}")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating image embeddings: {e}")
            raise
        
    def embed_single_image(self, image: Union[str, np.ndarray, Image.Image]) -> np.ndarray:
        "Generate embedding for a single image"
        embeddings = self.embed_image(image)
        return embeddings[0]
    
    def get_embedding_dimension(self) -> int:
        "Get the dimension of the embeddings"
        return self.model.config.vision_config.hidden_size
    
# Global CLIP image embedder instance
clip_image_embedder = None

def get_clip_image_embedder() -> CLIPImageEmbedder:
    "Get or create global CLIP image embedder instance"
    global clip_image_embedder
    if clip_image_embedder is None:
        clip_image_embedder = CLIPImageEmbedder()
    return clip_image_embedder

def embed_image_data(image: Union[str, np.ndarray, Image.Image]) -> np.ndarray:
    "Convenience function to embed image data using CLIP"
    embedder = get_clip_image_embedder()
    return embedder.embed_image(image)

def embed_single_image_data(image: Union[str, np.ndarray, Image.Image]) -> np.ndarray:
    "Convenience function to embed a single image using CLIP"
    embedder = get_clip_image_embedder()
    return embedder.embed_single_image(image)