import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from group2_derivation import run_derivation

def test_group2_derivation():
    """
    Runs the Group 2 derivation script to verify it executes without error.
    Visual verification of images in 'draw/' is expected.
    """
    try:
        run_derivation()
        print("Group 2 Derivation executed successfully.")
    except Exception as e:
        print(f"Group 2 Derivation failed with error: {e}")
        raise e

if __name__ == "__main__":
    test_group2_derivation()
