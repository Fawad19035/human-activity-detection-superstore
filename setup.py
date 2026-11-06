import os
import sys
import subprocess

requirements = [
    "flask",
    "opencv-python",
    "numpy",
    "ultralytics",
    "gunicorn",
    "python-dotenv"
]

def install_dependencies():
    for package in requirements:
        try:
            __import__(package.split('==')[0])
            print(f"{package} already installed")
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    install_dependencies()
    print("All dependencies installed successfully!")
    