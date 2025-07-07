# Quick Commerce Medicine Delivery Frontend

This is the React frontend for the Quick Commerce Medicine Delivery platform.

## Features

- User authentication and profile management
- Medicine browsing and searching
- Prescription management
- Shopping cart functionality
- Order placement and tracking
- Quick delivery options

## Getting Started

### Prerequisites

- Node.js (v14.0.0 or later)
- npm (v6.0.0 or later)

### Installation

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

The application will be available at http://localhost:3000

## Available Scripts

In the project directory, you can run:

- `npm start`: Runs the app in development mode
- `npm test`: Launches the test runner
- `npm run build`: Builds the app for production
- `npm run eject`: Ejects from Create React App

## API Connection

The frontend connects to the FastAPI backend running on http://localhost:8000. This is configured in the `package.json` file with the proxy setting.

## Default Users

For testing, you can use these default users:

- Admin User:
  - Email: admin@quickcommerce.com
  - Password: admin123

- Delivery Partner:
  - Email: delivery@quickcommerce.com
  - Password: delivery123 