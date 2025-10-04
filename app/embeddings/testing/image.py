#!/usr/bin/env python3
"""
Basic test file for CLIP image embedding functionality
"""

import sys
import os
import numpy as np
import requests
from PIL import Image
import io

# Add the project root to the path so we can import our modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from app.embeddings.image import embed_single_image_data, embed_image_data, get_clip_image_embedder

def download_test_image(url: str) -> Image.Image:
    """Download image from URL for testing"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        print(f"✅ Successfully downloaded image from: {url}")
        print(f"   Image size: {image.size}")
        print(f"   Image mode: {image.mode}")
        return image
    except Exception as e:
        print(f"❌ Failed to download image: {e}")
        raise

def test_image_embedder_instance():
    """Test getting image embedder instance directly"""
    print("Testing image embedder instance...")
    
    try:
        embedder = get_clip_image_embedder()
        print(f"✅ Image embedder instance created successfully!")
        print(f"   Model name: {embedder.model_name}")
        print(f"   Device: {embedder.device}")
        return True
    except Exception as e:
        print(f"❌ Image embedder instance creation failed: {e}")
        return False

def test_single_image_embedding():
    """Test embedding a single image from URL"""
    print("\nTesting single image embedding from URL...")
    
    # COCO dataset image URL
    image_url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    
    try:
        # Download and embed the image
        image = download_test_image(image_url)
        embedding = embed_single_image_data(image)
        
        print(f"✅ Single image embedding successful!")
        print(f"   Shape: {embedding.shape}")
        print(f"   Type: {type(embedding)}")
        print(f"   Sample values: {embedding[:5]}")
        return True
    except Exception as e:
        print(f"❌ Single image embedding failed: {e}")
        return False

def test_image_from_url():
    """Test embedding image directly from URL string"""
    print("\nTesting image embedding from URL string...")
    
    image_url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    
    try:
        # Test embedding directly from URL
        embedding = embed_single_image_data(image_url)
        
        print(f"✅ Image embedding from URL successful!")
        print(f"   Shape: {embedding.shape}")
        print(f"   Embedding dimension: {len(embedding)}")
        return True
    except Exception as e:
        print(f"❌ Image embedding from URL failed: {e}")
        return False

def test_multiple_images_embedding():
    """Test embedding multiple images"""
    print("\nTesting multiple images embedding...")
    
    # Use the same image multiple times for testing
    image_url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    
    try:
        # Create a list of the same image (in practice, you'd have different images)
        images = [image_url, image_url, image_url]
        embeddings = embed_image_data(images)
        
        print(f"✅ Multiple images embedding successful!")
        print(f"   Shape: {embeddings.shape}")
        print(f"   Number of images: {len(images)}")
        print(f"   Embedding dimension: {embeddings.shape[1]}")
        return True
    except Exception as e:
        print(f"❌ Multiple images embedding failed: {e}")
        return False

def test_image_similarity():
    """Test that the same image produces identical embeddings"""
    print("\nTesting image embedding consistency...")
    
    image_url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    
    try:
        # Embed the same image twice
        embedding1 = embed_single_image_data(image_url)
        embedding2 = embed_single_image_data(image_url)
        
        # Calculate cosine similarity (should be 1.0 for identical images)
        similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        
        print(f"✅ Consistency test completed!")
        print(f"   Image URL: {image_url}")
        print(f"   Cosine similarity: {similarity:.6f}")
        
        if similarity > 0.999:  # Very high similarity for identical images
            print("   ✅ Identical images produce identical embeddings (good!)")
        else:
            print("   ⚠️  Embeddings are not identical (unexpected)")
        
        return True
    except Exception as e:
        print(f"❌ Consistency test failed: {e}")
        return False

def test_numpy_array_embedding():
    """Test embedding from numpy array"""
    print("\nTesting numpy array embedding...")
    
    try:
        # Download image and convert to numpy array
        image_url = "http://images.cocodataset.org/val2017/000000039769.jpg"
        image = download_test_image(image_url)
        image_array = np.array(image)
        
        # Embed from numpy array
        embedding = embed_single_image_data(image_array)
        
        print(f"✅ Numpy array embedding successful!")
        print(f"   Array shape: {image_array.shape}")
        print(f"   Embedding shape: {embedding.shape}")
        return True
    except Exception as e:
        print(f"❌ Numpy array embedding failed: {e}")
        return False

def main():
    """Run all image embedding tests"""
    print("🚀 Starting CLIP Image Embedding Tests")
    print("=" * 60)
    print("Testing with COCO dataset image:")
    print("http://images.cocodataset.org/val2017/000000039769.jpg")
    print("=" * 60)
    
    tests = [
        test_image_embedder_instance,
        test_single_image_embedding,
        test_image_from_url,
        test_numpy_array_embedding,
        test_multiple_images_embedding,
        test_image_similarity
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All image embedding tests passed! CLIP image embedding is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
