# Building File Hash Verifier Executable

This guide will help you create a standalone executable (.exe) file for the File Hash Verifier application.

## Prerequisites

1. Python 3.6 or higher installed
2. Windows operating system
3. Internet connection (for downloading PyInstaller)

## Build Instructions

### Method 1: Using the Build Script (Recommended)

1. Double-click `build.bat`
2. Wait for the build process to complete (this may take a few minutes)
3. Once finished, you'll find the executable at:
   ```
   dist\File Hash Verifier.exe
   ```

### Method 2: Manual Build

If the build script doesn't work, you can build manually:

1. Open Command Prompt
2. Navigate to the project directory
3. Run these commands:
   ```batch
   pip install pyinstaller
   pyinstaller --noconfirm --onefile --windowed --name "File Hash Verifier" file_hash_verifier.py
   ```

## After Building

1. The executable will be created in the `dist` folder
2. You can copy `File Hash Verifier.exe` to any location
3. Double-click to run the application

## Troubleshooting

If you encounter any issues:

1. Make sure Python is installed and added to PATH
2. Verify that tkinter is installed (it comes with Python)
3. Try running the build script as administrator
4. Check that all files are in the same directory

## Notes

- The executable is standalone and doesn't require Python to be installed
- The first run might be slow as Windows verifies the executable
- Antivirus software might flag the executable; you may need to add an exception

## Support

If you encounter any issues during the build process, please:
1. Check the error messages in the command prompt
2. Ensure all prerequisites are met
3. Try running the build script as administrator 