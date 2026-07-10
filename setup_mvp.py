# setup_mvp.py
"""
Setup script for AI SDLC Wizard MVP
Run this to initialize the environment and check dependencies
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50 + "\n")

def check_python_version():
    """Check if Python version is 3.8+"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} is supported")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.8+")
        return False

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = [
        "artifacts",
        "generated_code",
        "test_cases",
        "exports",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/")

def check_env_file():
    """Check if .env file exists"""
    print("Checking environment configuration...")
    if os.path.exists(".env"):
        print("✅ .env file found")
        
        # Check for GROQ_API_KEY
        with open(".env", "r") as f:
            content = f.read()
            if "GROQ_API_KEY" in content and "your_groq_api_key" not in content:
                print("✅ GROQ_API_KEY is configured")
            else:
                print("⚠️  GROQ_API_KEY needs to be set in .env file")
    else:
        print("❌ .env file not found. Creating template...")
        with open(".env", "w") as f:
            f.write("GROQ_API_KEY=your_groq_api_key_here\n")
            f.write("APP_ENV=development\n")
        print("✅ Created .env template. Please add your GROQ_API_KEY")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    # Core dependencies
    core_deps = [
        "streamlit",
        "plotly",
        "kaleido",
        "streamlit-extras",
        "humanize",
        "reportlab",
        "openpyxl",
        "python-docx",
        "python-dotenv",
        "langchain",
        "langchain-groq",
        "langgraph"
    ]
    
    try:
        # Install from requirements.txt if exists
        if os.path.exists("requirements.txt"):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Installed dependencies from requirements.txt")
        
        # Install additional MVP dependencies
        print("\nInstalling additional MVP dependencies...")
        for dep in ["plotly", "kaleido", "streamlit-extras", "humanize", "reportlab"]:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ Installed {dep}")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    
    return True

def create_sample_config():
    """Create a sample configuration file if not exists"""
    if not os.path.exists("config.py"):
        print("Creating sample configuration...")
        # Copy from the artifact or create a minimal version
        print("⚠️  config.py not found. Please ensure config.py is in the project directory")

def verify_imports():
    """Verify that all imports work correctly"""
    print("Verifying imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
        
        import plotly
        print("✅ Plotly imported successfully")
        
        import langchain
        print("✅ LangChain imported successfully")
        
        import langgraph
        print("✅ LangGraph imported successfully")
        
        from docx import Document
        print("✅ python-docx imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print_header("AI SDLC Wizard MVP Setup")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print()
    
    # Create directories
    create_directories()
    print()
    
    # Check environment file
    check_env_file()
    print()
    
    # Install dependencies
    print_header("Installing Dependencies")
    if not install_dependencies():
        print("\n⚠️  Some dependencies failed to install. Please check the errors above.")
    print()
    
    # Verify imports
    print_header("Verifying Installation")
    if verify_imports():
        print("\n✅ All imports verified successfully!")
    else:
        print("\n⚠️  Some imports failed. Please install missing dependencies.")
    
    # Final instructions
    print_header("Setup Complete!")
    print("Next steps:")
    print("1. Add your GROQ_API_KEY to the .env file")
    print("2. Ensure all Python files are in the project directory:")
    print("   - streamlit_app.py (MVP UI)")
    print("   - sdlc_graph.py (workflow logic)")
    print("   - ui_utils.py (UI utilities)")
    print("   - config.py (configuration)")
    print("3. Run the application: streamlit run streamlit_app.py")
    print("\nEnjoy your AI SDLC Wizard MVP! 🚀")

if __name__ == "__main__":
    main()