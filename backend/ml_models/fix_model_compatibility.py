#!/usr/bin/env python3
"""
Fix NumPy compatibility issues with pickled ML models
Re-saves models in current environment format
"""
import pickle
import os
import json

def fix_model_compatibility():
    """
    Reload models and re-save them with current numpy/sklearn versions
    """
    save_dir = os.path.join(os.path.dirname(__file__), 'saved_models')
    model_path = os.path.join(save_dir, 'mahila_intent_model.pkl')
    vectorizer_path = os.path.join(save_dir, 'mahila_intent_model_vectorizer.pkl')
    info_path = os.path.join(save_dir, 'model_info.json')
    
    # Backup original files
    backup_dir = os.path.join(save_dir, 'backup')
    os.makedirs(backup_dir, exist_ok=True)
    
    import shutil
    if os.path.exists(model_path):
        shutil.copy2(model_path, os.path.join(backup_dir, 'mahila_intent_model.pkl.bak'))
        print(f"✓ Backed up model to {backup_dir}")
    
    try:
        print("📖 Reading model files with compatibility fixes...")
        
        # Try to load with numpy compatibility handling
        import warnings
        warnings.filterwarnings('ignore')
        
        # Patch numpy imports if needed
        import numpy
        if not hasattr(numpy, '_core'):
            # Create compatibility shim
            numpy._core = type('module', (), {})()
            
            # Copy needed modules
            if hasattr(numpy, 'core'):
                numpy._core.numeric = numpy.core.numeric
                numpy._core.multiarray = numpy.core.multiarray
                print("✓ NumPy compatibility shim created")
        
        # Load models
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            print(f"✓ Loaded model: {type(model).__name__}")
        
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
            print(f"✓ Loaded vectorizer: {type(vectorizer).__name__}")
        
        # Re-save with current environment
        with open(model_path, 'wb') as f:
            pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"✓ Re-saved model (protocol {pickle.HIGHEST_PROTOCOL})")
        
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(vectorizer, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"✓ Re-saved vectorizer")
        
        # Load info
        if os.path.exists(info_path):
            with open(info_path, 'r') as f:
                info = json.load(f)
                print(f"✓ Loaded model info: {info.get('model_type', 'unknown')}")
        
        print("\n✅ Model compatibility fix completed!")
        print(f"   Models are now compatible with current numpy/sklearn versions")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during fix: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = fix_model_compatibility()
    exit(0 if success else 1)
