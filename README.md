# File Hash Verifier

A powerful and user-friendly application for verifying file integrity using various hash algorithms. This tool helps ensure that files haven't been tampered with by comparing their hash values against known good hashes.

## Features

- **Multiple Hash Algorithms**: Support for MD5, SHA-1, SHA-256, SHA-384, and SHA-512
- **User-Friendly Interface**: Clean and intuitive GUI built with tkinter
- **Batch Processing**: Verify multiple files at once
- **History Tracking**: Maintains a record of the last 30 verification attempts
- **Export Options**: Export verification history in multiple formats:
  - HTML
  - PDF
  - CSV
  - JSON
- **Clipboard Support**: Easy copy-paste functionality for hash values
- **Detailed Logging**: Comprehensive logging of all operations
- **Help Documentation**: Built-in help system with detailed instructions

## Requirements

- Python 3.6 or higher
- Windows operating system
- Required Python packages (automatically installed via requirements.txt):
  - tkinter (usually comes with Python)
  - reportlab (for PDF export)
  - pyinstaller (for building executable)

## Installation

1. Clone this repository:
   ```bash
   git clone [repository-url]
   cd Git-Hub-Hash
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running from Source

```bash
python file_hash_verifier.py
```

### Using the Executable

1. Build the executable using the provided build script:
   ```bash
   build.bat
   ```
2. Run the generated executable from the `dist` directory.

## Building the Executable

1. Ensure all requirements are installed
2. Run the build script:
   ```bash
   build.bat
   ```
3. The executable will be created in the `dist` directory

For detailed build instructions, see `BUILD_INSTRUCTIONS.md`.

## Features in Detail

### Hash Verification
- Select files individually or in batch
- Choose from multiple hash algorithms
- Compare against known hash values
- View detailed verification results

### History Management
- View last 30 verification attempts
- Export history in multiple formats
- Clear history when needed
- Automatic history updates

### Export Options
- **HTML**: Formatted report with color-coded results
- **PDF**: Professional document with detailed information
- **CSV**: Spreadsheet-friendly format
- **JSON**: Machine-readable format

## File Structure

- `file_hash_verifier.py`: Main application file
- `help.html`: Help documentation
- `requirements.txt`: Python package dependencies
- `build.bat`: Build script for creating executable
- `create_version.py`: Version file generator
- `BUILD_INSTRUCTIONS.md`: Detailed build process documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python and tkinter
- Uses ReportLab for PDF generation
- PyInstaller for executable creation

## Support

For issues, feature requests, or questions, please open an issue in the repository. 