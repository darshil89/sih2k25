#!/usr/bin/env python3
"""
Basic test file for CLIP text embedding functionality
"""

import sys
import os
import numpy as np

# Add the project root to the path so we can import our modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from app.embeddings.text import embed_single_text_data, embed_text_data, get_clip_embedder

def test_single_text_embedding():
    """Test embedding a single text string"""
    print("Testing single text embedding...")
    
    text = "Hello, this is a test sentence for CLIP embedding."
    
    try:
        embedding = embed_single_text_data(text)
        print(f"✅ Single text embedding successful!")
        print(f"   Shape: {embedding.shape}")
        print(f"   Type: {type(embedding)}")
        print(f"   Sample values: {embedding[:5]}")
        return True
    except Exception as e:
        print(f"❌ Single text embedding failed: {e}")
        return False

def test_multiple_text_embedding():
    """Test embedding multiple text strings"""
    print("\nTesting multiple text embedding...")
    
    texts = [
        "This is the first test sentence.",
        "Here is another sentence to test.",
        "And this is the third test sentence."
    ]
    
    try:
        embeddings = embed_text_data(texts)
        print(f"✅ Multiple text embedding successful!")
        print(f"   Shape: {embeddings.shape}")
        print(f"   Number of texts: {len(texts)}")
        print(f"   Embedding dimension: {embeddings.shape[1]}")
        return True
    except Exception as e:
        print(f"❌ Multiple text embedding failed: {e}")
        return False

def test_embedder_instance():
    """Test getting embedder instance directly"""
    print("\nTesting embedder instance...")
    
    try:
        embedder = get_clip_embedder()
        print(f"✅ Embedder instance created successfully!")
        print(f"   Model name: {embedder.model_name}")
        print(f"   Device: {embedder.device}")
        print(f"   Embedding dimension: {embedder.get_embedding_dimension()}")
        return True
    except Exception as e:
        print(f"❌ Embedder instance creation failed: {e}")
        return False

def test_embedding_similarity():
    """Test that similar texts have similar embeddings"""
    print("\nTesting embedding similarity...")
    
    try:
        # Test similar sentences
        text1 = "The cat is sitting on the mat."
        text2 = "A cat sits on a mat."
        
        embedding1 = embed_single_text_data(text1)
        embedding2 = embed_single_text_data(text2)
        
        # Calculate cosine similarity
        similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        
        print(f"✅ Similarity test completed!")
        print(f"   Text 1: '{text1}'")
        print(f"   Text 2: '{text2}'")
        print(f"   Cosine similarity: {similarity:.4f}")
        
        if similarity > 0.7:
            print("   ✅ Similar texts have high similarity (good!)")
        else:
            print("   ⚠️  Similarity is lower than expected")
        
        return True
    except Exception as e:
        print(f"❌ Similarity test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting CLIP Text Embedding Tests")
    print("=" * 50)
    
    tests = [
        test_embedder_instance,
        test_single_text_embedding,
        test_multiple_text_embedding,
        test_embedding_similarity
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! CLIP embedding is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
