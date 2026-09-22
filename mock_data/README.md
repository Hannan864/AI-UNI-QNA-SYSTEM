# Mock Data Folder

This folder contains university data files for the IIUI Smart Chatbot.

## Supported File Types

- **PDF files** - University documents, brochures, policies
- **Word documents (.docx)** - Course outlines, syllabi
- **Text files (.txt)** - Extracted text content
- **JSON files** - Structured data
- **CSV files** - Tabular data

## How to Use

1. Place your scraped/collected university data files in this folder
2. The chatbot's Knowledge Base and FAQ system uses data from the database
3. To import data from files, use the Admin Dashboard Knowledge Base section
4. Or run the database init script: `python database/init_db.py`

## Current Data Sources

- Seed data is loaded via `database/init_db.py`
- Admin can add/edit/delete KB entries via the admin panel
- FAQ entries are managed similarly

## Adding New Data

### Manual Entry
Use the Admin Dashboard → Knowledge Base → Add Entry

### Bulk Import
Place CSV/JSON files here and use the import utility (coming in future phases)

### PDF/Word Processing
Place documents here for future NLP extraction (coming in future phases)
