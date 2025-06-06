# Create Version Script

This script (`create_version.py`) is a utility component of the File Hash Verifier build process. It generates the version information file required by PyInstaller to create a properly versioned Windows executable.

## Purpose

The script creates a `version.txt` file that contains:
- File version information
- Product version information
- Company details
- File description
- Copyright information
- Other metadata required for Windows executables

## Usage

The script is automatically called by the build process (`build.bat`), but can also be run manually:

```bash
python create_version.py
```

## Output

The script generates a `version.txt` file with the following structure:

```python
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Your Company'),
         StringStruct(u'FileDescription', u'File Hash Verifier'),
         StringStruct(u'FileVersion', u'1.0.0.0'),
         StringStruct(u'InternalName', u'FileHashVerifier'),
         StringStruct(u'LegalCopyright', u'Copyright (c) 2025'),
         StringStruct(u'OriginalFilename', u'FileHashVerifier.exe'),
         StringStruct(u'ProductName', u'File Hash Verifier'),
         StringStruct(u'ProductVersion', u'1.0.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

## Technical Details

### Version Information

- **File Version**: Current version is 1.0.0.0
- **Product Version**: Matches file version
- **File Type**: Windows Application (0x1)
- **OS**: Windows NT (0x40004)

### String Information

- **Company Name**: Your Company
- **File Description**: File Hash Verifier
- **Internal Name**: FileHashVerifier
- **Original Filename**: FileHashVerifier.exe
- **Product Name**: File Hash Verifier
- **Legal Copyright**: Copyright (c) 2025

### Language and Character Set

- **Language**: English (United States) - 1033
- **Character Set**: Unicode - 1200

## Integration with Build Process

1. The script is called by `build.bat` during the build process
2. The generated `version.txt` is used by PyInstaller to:
   - Set the executable's version information
   - Configure Windows file properties
   - Enable proper version checking

## Modifying Version Information

To update the version information:

1. Edit the version numbers in the script:
   ```python
   filevers=(1, 0, 0, 0),  # Change these numbers
   prodvers=(1, 0, 0, 0),  # to match your version
   ```

2. Update other metadata as needed:
   - Company name
   - Copyright information
   - File description

## Error Handling

The script includes error handling for:
- File permission issues
- Write access problems
- Invalid version number formats

## Dependencies

- Python 3.6 or higher
- No external Python packages required

## Notes

- The script must be run before PyInstaller
- The generated file is temporary and used only during build
- Version numbers should follow semantic versioning
- The script creates UTF-8 encoded output

## Troubleshooting

If you encounter issues:

1. **Permission Errors**
   - Run the script with appropriate permissions
   - Check write access to the directory

2. **Version Format Errors**
   - Ensure version numbers are valid
   - Check for proper tuple formatting

3. **Build Integration Issues**
   - Verify the script is called correctly in build.bat
   - Check the build log for specific errors

## Support

For issues or questions:
1. Check the build log for specific errors
2. Verify the script's output format
3. Ensure proper integration with the build process 