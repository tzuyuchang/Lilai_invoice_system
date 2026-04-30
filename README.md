# Invoice System for Language School

A Python-based invoice generation system for language school business operations.

## Features

- Professional PDF invoice generation with company branding
- GUI interface for easy invoice creation
- Language school data management
- Support for multiple languages (Chinese/English)
- Automatic PDF saving with customizable filenames

## Project Structure

```
invoice_system/
├── src/                 # Source code
│   ├── invoice_generator.py  # PDF generation engine
│   ├── gui.py           # Basic GUI interface
│   └── gui_fixed.py     # Enhanced GUI interface
├── ref/                 # Reference files
│   ├── Lilaiireland_Logo_s.PNG  # Company logo
│   ├── TzuYuChang_sign.png      # Signature image
│   └── NotoSerifTC-Bold.ttf     # Chinese font
├── invoice_output/      # Generated PDF invoices
├── language_schools.json  # Client data
├── school_manager.py    # CLI tool for managing schools
└── AGENTS.md            # Developer instructions
```

## Prerequisites

- Python 3.x
- ReportLab library (`pip install reportlab`)
- tkinter (usually included with Python)

## Getting Started

### Running the GUI
```bash
python gui.py
```

### Managing Schools
```bash
python school_manager.py
```

### Generating Sample Invoice
```bash
python invoice_generator.py
```

## Usage

1. Launch the GUI application
2. Select a language school from the dropdown or enter information manually
3. Add invoice items using the table interface
4. Set tax/deduction amounts if applicable
5. Click "Generate PDF" to create your invoice

## Customization

To customize the invoice template:
1. Modify `invoice_generator.py` to change layout and styling
2. Update reference files in `ref/` directory for branding changes
3. Edit `language_schools.json` to manage client data

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.