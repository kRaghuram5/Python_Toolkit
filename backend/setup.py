"""
Quick setup script for PDF Toolkit
This script helps set up the application quickly
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'outputs', 'static', 'templates', 'utils']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Created necessary directories")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
        else:
            print("⚠️  .env.example not found, skipping .env creation")
    else:
        print("✅ .env file already exists")

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    print("=" * 60)
    print("  PDF Toolkit - Setup Script")
    print("=" * 60)
    print()

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Create directories
    create_directories()

    # Create .env file
    create_env_file()

    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Please install dependencies manually using:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  🎉 Setup completed successfully!")
    print("=" * 60)
    print("\n  To start the application, run:")
    print("    python app.py")
    print("\n  Then open your browser and navigate to:")
    print("    http://localhost:5000")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
