#!/usr/bin/env python
"""
Quick start script for GuragChat
Run this to test your installation
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    modules = [
        "langchain",
        "langchain_core",
        "langchain_community",
        "sentence_transformers",
        "pypdf",
        "dotenv",
    ]
    
    missing = []
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ✗ {module} (missing)")
            missing.append(module)
    
    return missing

def test_ollama():
    """Test Ollama connectivity."""
    print("\nTesting Ollama...")
    sys.path.insert(0, '.')
    
    try:
        from guragchat.utils.ollama import is_ollama_running, get_installed_models
        
        if is_ollama_running():
            print("  ✓ Ollama is running")
            models = get_installed_models()
            if models:
                print(f"  ✓ Found {len(models)} model(s):")
                for model in models:
                    print(f"    - {model}")
            else:
                print("  ⚠ No models installed. Run: ollama pull gemma3:1b")
            return True
        else:
            print("  ✗ Ollama is not running")
            print("     Start it with: ollama serve")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_rag():
    """Test RAG chain loading."""
    print("\nTesting RAG module...")
    sys.path.insert(0, '.')
    
    try:
        from guragchat.rag.core import build_rag_chain
        print("  ✓ RAG module imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_cli():
    """Test CLI module loading."""
    print("\nTesting CLI module...")
    sys.path.insert(0, '.')
    
    try:
        from guragchat.cli.main import main
        print("  ✓ CLI module imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print(" GuragChat Installation Test")
    print("=" * 60 + "\n")
    
    # Test imports
    missing = test_imports()
    if missing:
        print(f"\n⚠ Missing modules: {', '.join(missing)}")
        print("Install with: pip install guragchat")
        return 1
    
    # Test Ollama
    ollama_ok = test_ollama()
    
    # Test modules
    rag_ok = test_rag()
    cli_ok = test_cli()
    
    # Summary
    print("\n" + "=" * 60)
    if ollama_ok and rag_ok and cli_ok:
        print(" ✓ All tests passed! GuragChat is ready to use.")
        print("\n Try it:")
        print("   guragchat --pdf document.pdf")
    else:
        print(" ⚠ Some tests failed. Check the output above.")
        if not ollama_ok:
            print("   - Start Ollama: ollama serve")
        if not rag_ok or not cli_ok:
            print("   - Install dependencies: pip install guragchat")
    print("=" * 60 + "\n")
    
    return 0 if (ollama_ok and rag_ok and cli_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
