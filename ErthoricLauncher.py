import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_python():
    """Check if Python is available"""
    try:
        subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
        return True
    except:
        return False

def check_requests():
    """Check if requests module is installed"""
    try:
        import requests
        return True
    except ImportError:
        return False

def install_requests():
    """Install requests module"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True, capture_output=True)
        return True
    except:
        return False

def launch_erthoric():
    """Launch the main Erthoric application"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        erthoric_script = os.path.join(script_dir, "erthoric.py")
        
        if not os.path.exists(erthoric_script):
            messagebox.showerror("Error", "Erthoric main script not found!")
            return False
        
        # Launch erthoric.py
        subprocess.Popen([sys.executable, erthoric_script])
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch Erthoric: {str(e)}")
        return False

def main():
    # Check Python
    if not check_python():
        messagebox.showerror(
            "Python Not Found", 
            "Python is not installed or not in PATH.\n\n"
            "Please install Python 3.6+ from python.org and try again."
        )
        return
    
    # Check and install requests
    if not check_requests():
        result = messagebox.askyesno(
            "Install Required Package",
            "The 'requests' package is required but not installed.\n\n"
            "Do you want to install it automatically?"
        )
        
        if result:
            messagebox.showinfo("Installing", "Please wait while installing required packages...")
            if install_requests():
                messagebox.showinfo("Success", "Package installed successfully!")
            else:
                messagebox.showerror("Error", "Failed to install required package.")
                return
        else:
            messagebox.showinfo(
                "Manual Installation", 
                "You can manually install the required package using:\n"
                "pip install requests"
            )
            return
    
    # Launch Erthoric
    launch_erthoric()

if __name__ == "__main__":
    # Hide the console window
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    main()