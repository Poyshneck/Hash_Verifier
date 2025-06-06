# Build Instructions for File Hash Verifier

This document provides detailed instructions for building the File Hash Verifier application from source code.

## Prerequisites

Before building the application, ensure you have the following installed:

1. **Python 3.6 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Required Python Packages**
   - All required packages are listed in `requirements.txt`
   - They will be automatically installed during the build process

## Build Process

### 1. Prepare the Environment

1. Open a command prompt in the project directory
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

### 2. Install Dependencies

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
   This will install:
   - tkinter (GUI framework)
   - reportlab (PDF generation)
   - pyinstaller (executable creation)

### 3. Build the Executable

1. Run the build script:
   ```bash
   build.bat
   ```

The build script will:
- Check for Python and required packages
- Create version information
- Build the executable using PyInstaller
- Create a standalone executable in the `dist` directory

### 4. Verify the Build

1. Check the `dist` directory for:
   - `FileHashVerifier.exe`
   - Required DLL files
   - Help documentation

2. Test the executable:
   - Double-click `FileHashVerifier.exe`
   - Verify all features work correctly
   - Check that help documentation is accessible

## Build Script Details

The `build.bat` script performs the following steps:

1. **Environment Check**
   - Verifies Python installation
   - Checks for required packages
   - Creates log file for build process

2. **Version File Creation**
   - Generates `version.txt` using `create_version.py`
   - Includes version information for the executable

3. **PyInstaller Configuration**
   - Uses `FHV.spec` for build configuration
   - Includes all necessary files and dependencies
   - Sets up proper file associations

4. **Build Process**
   - Creates standalone executable
   - Bundles all required files
   - Generates proper file structure

## Troubleshooting

### Common Issues

1. **Python Not Found**
   - Ensure Python is installed and added to PATH
   - Try running `python --version` to verify installation

2. **Missing Dependencies**
   - Run `pip install -r requirements.txt` manually
   - Check for any error messages in the build log

3. **Build Failures**
   - Check `build_log.txt` for detailed error messages
   - Verify all required files are present
   - Ensure sufficient disk space

4. **Executable Issues**
   - Verify antivirus isn't blocking the build
   - Check Windows Defender settings
   - Run as administrator if needed

### Build Log

The build process creates a `build_log.txt` file containing:
- Installation status of dependencies
- Version file creation details
- PyInstaller build output
- Any errors or warnings

Check this file if you encounter any issues during the build process.

## Distribution

After successful build:

1. The executable will be in the `dist` directory
2. Required files are automatically bundled
3. No additional installation is needed
4. The executable can be distributed to other Windows systems

## Notes

- The build process may take several minutes
- The resulting executable is standalone
- No Python installation is required on target systems
- The executable works on Windows 7 and later
- 32-bit/64-bit compatibility depends on the Python version used for building

## Support

If you encounter any issues during the build process:
1. Check the `build_log.txt` file
2. Verify all prerequisites are installed
3. Ensure you have proper permissions
4. Open an issue in the repository if problems persist 