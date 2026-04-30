# Agent Instructions for Invoice System

## Project Overview
This is a Python-based invoice generation system for a language school business. It creates professional PDF invoices with company branding, client information, and itemized charges.

## Key Files
- `invoice_generator.py` - Core PDF generation engine using ReportLab
- `gui.py` - Tkinter-based graphical user interface
- `language_schools.json` - Data file containing client information
- `school_manager.py` - CLI tool for managing school data
- `gui_fixed.py` - Enhanced GUI version

## Running the System
1. **Start GUI**: `python gui.py` or `python gui_fixed.py`
2. **Run school manager**: `python school_manager.py`
3. **Direct PDF generation**: `python invoice_generator.py` (uses sample data)

## Dependencies
- Python 3.x
- ReportLab library (`pip install reportlab`)
- tkinter (usually included with Python)
- Chinese fonts (NotoSerifTC-Bold.ttf) for proper display
- PNG images for logo (Lilaiireland_Logo_s.PNG) and signature (TzuYuChang_sign.png)

## Important Commands
- Generate sample invoice: `python invoice_generator.py`
- Launch GUI: `python gui.py`
- Manage schools: `python school_manager.py`

## Architecture Notes
- Uses ReportLab for PDF creation with custom fonts and styling
- Tkinter GUI handles user input and form management
- School data is managed in JSON format
- Multiple GUI versions exist (basic and enhanced)

## Environment Considerations
- Font files must be in the working directory for proper rendering
- Image files for logo and signature must be present
- All text processing assumes UTF-8 encoding
- PDF output is generated in A4 format

## Testing
- Run individual modules to verify functionality
- Test GUI interactions manually
- Verify PDF output visually
- Check that all required assets are present

## Development Workflow
1. Make changes to `invoice_generator.py` for PDF logic
2. Modify `gui.py` or `gui_fixed.py` for UI changes
3. Update `language_schools.json` for client data
4. Test by running the appropriate Python script
5. Validate PDF output with sample data