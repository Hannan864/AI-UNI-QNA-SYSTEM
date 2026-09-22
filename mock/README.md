# Mock Data Folder

Place university documents here for the Mock Data Assistant.

## Folder Structure
```
mock/
├── pdf/      ← PDF documents (policies, catalogs, brochures)
├── docx/     ← Word documents (course outlines, syllabi)
├── doc/      ← Legacy Word documents
├── txt/      ← Plain text files
├── csv/      ← Tabular data (courses, fees, schedules)
├── json/     ← Structured data
├── xlsx/     ← Excel spreadsheets
└── other/    ← Other file types
```

## Supported Formats
- PDF, DOCX, DOC, TXT, CSV, JSON, XLSX

## How Data Flows
```
Real documents → mock/ → extraction → Knowledge Base → NLP → ML → Mock Chatbot
```

## Adding Data
1. Place files in the appropriate subfolder
2. Use Admin Dashboard → Knowledge Base to add entries
3. Or import via the database init script

## Important
- Mock mode uses ONLY local data — never calls Live AI
- Live mode uses configured AI provider — never reads mock files
- Modes stay cleanly separated
