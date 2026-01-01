# 🚀 Smart File Organizer

A professional desktop application built with Python and Streamlit that automatically organizes files into categorized folders based on their extensions. Perfect for cleaning up messy directories like Downloads, Documents, or Desktop folders.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Usage Guide](#usage-guide)
- [Screenshots](#screenshots)
- [Folder Structure](#folder-structure)
- [Technical Details](#technical-details)
- [Safety Features](#safety-features)
- [Troubleshooting](#troubleshooting)

## 🔍 Overview

The Smart File Organizer is a powerful yet user-friendly tool that scans a selected directory and automatically moves files into organized, categorized subfolders. The application provides a complete preview before making any changes and includes comprehensive safety measures to protect your data.

### Supported Categories

- 📄 **Documents** - PDF, DOC, DOCX, TXT, RTF, ODT, XLS, XLSX, PPT, PPTX, CSV
- 🖼️ **Images** - JPG, JPEG, PNG, GIF, BMP, SVG, WEBP, TIFF, ICO, HEIC
- 🎥 **Videos** - MP4, AVI, MKV, MOV, WMV, FLV, WEBM, M4V, MPG, MPEG
- 🎵 **Audio** - MP3, WAV, FLAC, AAC, OGG, WMA, M4A, OPUS, AIFF
- 📦 **Archives** - ZIP, RAR, 7Z, TAR, GZ, BZ2, XZ, ISO
- 💻 **Code Files** - PY, JS, HTML, CSS, JAVA, CPP, C, H, PHP, RB, GO, RS, SWIFT, KT, SCALA
- 📁 **Others** - All other file types

## ✨ Features

### Core Functionality
- **Intelligent File Categorization** - Automatically sorts files by extension
- **Recursive Directory Scanning** - Scans all subdirectories
- **Preview Mode** - See exactly what will be organized before committing
- **Safe File Operations** - Handles duplicates by renaming files
- **Real-time Progress Tracking** - Visual progress bar during organization
- **Comprehensive Statistics** - Detailed analytics and file distribution charts

### User Interface
- **Modern Web Interface** - Clean, responsive design using Streamlit
- **Interactive Dashboard** - Real-time statistics and metrics
- **Progress Visualization** - Live progress bars and status updates
- **Error Reporting** - Clear, user-friendly error messages
- **Mobile Responsive** - Works on desktop and mobile devices

### Safety & Security
- **Directory Validation** - Prevents accidental system directory organization
- **Permission Checking** - Validates write access before operations
- **Hidden File Protection** - Ignores system and hidden files
- **Safe File Moving** - Uses shutil.move for reliable file operations
- **Duplicate Handling** - Automatically renames duplicate files
- **Error Recovery** - Continues operation even if individual files fail

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Step-by-Step Installation

1. **Clone or download the project files**
   ```bash
   # If you have the project files, navigate to the project directory
   cd smart-file-organizer
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
   ```

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: Minimum 2GB (4GB recommended for large directories)
- **Storage**: At least 50MB free space for the application
- **Network**: Internet connection required for initial dependency installation

## 🚀 How to Run

### Method 1: Command Line

1. **Navigate to the project directory**
   ```bash
   cd /path/to/smart-file-organizer
   ```

2. **Run the application**
   ```bash
   streamlit run app.py
   ```

3. **Access the application**
   - The terminal will display a local URL (usually `http://localhost:8501`)
   - Open this URL in your web browser

### Method 2: Create a Launch Script

**For Windows (create `run.bat`):**
```batch
@echo off
streamlit run app.py
pause
```

**For macOS/Linux (create `run.sh`):**
```bash
#!/bin/bash
streamlit run app.py
```

Make the script executable:
```bash
chmod +x run.sh
```

### Method 3: Python Script

Create a `launch.py` file:
```python
import subprocess
import sys

def main():
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

Run with:
```bash
python launch.py
```

## 📖 Usage Guide

### Step 1: Launch the Application
- Open your terminal or command prompt
- Navigate to the project directory
- Run `streamlit run app.py`
- Open the provided URL in your web browser

### Step 2: Select a Directory
- Enter the full path to the directory you want to organize
- Examples:
  - Windows: `C:\Users\YourName\Downloads`
  - macOS: `/Users/YourName/Downloads`
  - Linux: `/home/yourname/Downloads`

### Step 3: Scan the Directory
- Click the "🔍 Scan Directory" button
- Wait for the scan to complete
- Review the number of files found

### Step 4: Preview Results
- Click "📊 Preview Results" to see detailed information
- Review:
  - Total files and categories
  - File distribution by category
  - Individual file details
  - Target organization structure

### Step 5: Organize Files
- Click "⚡ Organize Files" to start the organization process
- Monitor the progress bar
- Review the completion summary
- Check for any errors or issues

### Step 6: Verify Results
- Navigate to your organized directory
- Verify files are in appropriate category folders
- Check the application summary for success metrics

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/main_interface.png)
*Clean, intuitive interface with directory selection and action buttons*

### Scan Results
![Scan Results](screenshots/scan_results.png)
*Comprehensive preview showing file distribution and statistics*

### File Organization
![File Organization](screenshots/organization.png)
*Real-time progress tracking during file organization*

### Completion Summary
![Completion Summary](screenshots/completion.png)
*Detailed summary with success metrics and error reporting*

## 📁 Folder Structure

```
smart-file-organizer/
│
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This documentation file
├── screenshots/          # Application screenshots
│   ├── main_interface.png
│   ├── scan_results.png
│   ├── organization.png
│   └── completion.png
└── venv/                 # Virtual environment (after installation)
```

### File Descriptions

- **`app.py`** - Main Streamlit application containing all functionality
  - FileOrganizer class with core logic
  - Streamlit UI components
  - Session state management
  - Error handling and validation

- **`requirements.txt`** - Python package dependencies
  - streamlit==1.28.1
  - pandas==2.1.3

- **`README.md`** - Comprehensive documentation
  - Installation instructions
  - Usage guide
  - Technical details
  - Troubleshooting

## 🔧 Technical Details

### Architecture

The application follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI Layer                        │
│  (User Interface, Session Management, Event Handling)       │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  FileOrganizer Class                         │
│    (Business Logic, File Operations, Validation)            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│              Python Standard Libraries                       │
│    (os, shutil, pathlib, collections, typing)              │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

#### FileOrganizer Class
- **`__init__()`** - Initializes data structures
- **`validate_directory()`** - Validates directory safety and permissions
- **`scan_directory()`** - Recursively scans for files
- **`_categorize_file()`** - Determines file category based on extension
- **`_format_file_size()`** - Converts bytes to human-readable format
- **`organize_files()`** - Performs the actual file organization

#### Streamlit Integration
- **Session State** - Maintains application state across interactions
- **Callbacks** - Real-time progress updates during file operations
- **Progress Bars** - Visual feedback for long-running operations
- **Error Handling** - User-friendly error messages and recovery

### Supported File Extensions

The application recognizes 60+ file extensions across 7 categories:

| Category | Extensions |
|----------|------------|
| Documents | .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx, .csv |
| Images | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .tiff, .ico, .heic |
| Videos | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v, .mpg, .mpeg |
| Audio | .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a, .opus, .aiff |
| Archives | .zip, .rar, .7z, .tar, .gz, .bz2, .xz, .iso |
| Code Files | .py, .js, .html, .css, .java, .cpp, .c, .h, .php, .rb, .go, .rs, .swift, .kt, .scala |

## 🛡️ Safety Features

### Directory Protection
- **System Directory Prevention** - Blocks organization of critical system directories
- **Permission Validation** - Checks write access before operations
- **Path Traversal Protection** - Validates directory paths

### File Safety
- **Hidden File Protection** - Ignores system and hidden files
- **Duplicate Handling** - Automatically renames duplicate files
- **Safe Moving** - Uses shutil.move for reliable operations
- **Error Recovery** - Continues operation if individual files fail

### Data Protection
- **Preview Mode** - Shows all changes before execution
- **No Overwriting** - Never overwrites existing files
- **Rollback Capability** - Manual recovery instructions provided

### Error Handling
- **Graceful Degradation** - Continues operation despite errors
- **User Feedback** - Clear error messages and suggestions
- **Error Logging** - Comprehensive error tracking and reporting

## 🔍 Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

#### "Directory does not exist"
**Solution:** Verify the path exists and check spelling
- Windows: Use double backslashes `C:\\Users\\Name\\Downloads`
- macOS/Linux: Use forward slashes `/Users/Name/Downloads`

#### "No write permission for this directory"
**Solution:** Run with appropriate permissions or choose a different directory
- Windows: Run as administrator if necessary
- macOS/Linux: Check directory permissions with `ls -la`

#### "Cannot organize system directories"
**Solution:** Choose a user directory (Documents, Downloads, Desktop, etc.)

#### Application won't start
**Solutions:**
1. Verify Python 3.9+ is installed: `python --version`
2. Check virtual environment is activated
3. Verify all dependencies are installed: `pip list`

### Performance Tips

#### Large Directories
- **Issue:** Scanning takes a long time
- **Solution:** Be patient, progress is shown in real-time
- **Optimization:** Close other applications to free up system resources

#### Memory Usage
- **Issue:** High memory usage with many files
- **Solution:** The application handles this efficiently, but consider organizing in batches for 10,000+ files

### Error Recovery

#### If Organization Goes Wrong
1. **Don't panic** - Your original files are safe
2. **Check the summary** - Review what was moved where
3. **Manual recovery** - Files are in clearly labeled category folders
4. **Contact support** - Provide error messages for assistance

#### Reporting Issues
When reporting issues, include:
- Operating system and version
- Python version
- Error messages (screenshots helpful)
- Steps to reproduce the issue
- Directory path type (local, network, external drive)

### Getting Help

1. **Check this README** - Most common issues are covered here
2. **Review error messages** - The app provides helpful error descriptions
3. **Check the application logs** - Error details are displayed in the interface
4. **Test with a small directory first** - Verify the app works on your system

## 📝 License

This project is provided as-is for educational and personal use. Please use responsibly and always backup important data before organizing.

## 🤝 Contributing

This is a standalone application, but suggestions for improvements are welcome! Consider:
- Adding new file categories
- Improving the user interface
- Adding more safety features
- Enhancing error handling

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - The framework for creating the web interface
- Python Standard Library - For all file operations and data handling
- The open-source community for inspiration and best practices

---

**Happy Organizing! 📁✨**
