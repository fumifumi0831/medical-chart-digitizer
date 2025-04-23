# Medical Chart Digitizer - Frontend Service

This is the Next.js frontend for the Medical Chart Digitizer system.

## Setup

### Using Docker

```bash
docker-compose up frontend
```

### Manual Setup

1. Install dependencies:

```bash
npm install
# or
yarn install
```

2. Set up environment variables (see .env.example)

3. Run the development server:

```bash
npm run dev
# or
yarn dev
```

The application will be available at http://localhost:3000.

## Components

- `ImageUploader` - Handles file selection and upload
- `ResultDisplay` - Shows the uploaded image and extracted text
- `StatusBar` - Displays processing status
- `CsvDownloader` - Provides CSV download functionality