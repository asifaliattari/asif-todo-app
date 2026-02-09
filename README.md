# TaskFlow - AI-Powered Project Management System

**Created by Asif Ali AstolixGen for GIAIC Hackathon 2026**

## Overview

TaskFlow is a modern, feature-rich todo application built with Next.js 15, TypeScript, and Tailwind CSS. This project features a beautiful dark theme and includes advanced capabilities like voice commands, priority management, and smart filtering.

## Features

✅ **AI Chatbot Assistant** - Natural language task management with intelligent AI assistant
✅ **Task Management** - Add, delete, update, and view tasks with ease
✅ **Priority System** - Organize tasks by Low, Medium, and High priority
✅ **Status Tracking** - Track tasks as Pending, In Progress, or Completed
✅ **Search & Filter** - Find tasks quickly with powerful search and filtering
✅ **Voice Commands** - Add tasks using voice input (Speech Recognition)
✅ **Text-to-Speech** - Listen to your tasks read aloud
✅ **Due Dates** - Set deadlines for your tasks with date and time
✅ **Dark Theme** - Beautiful gradient dark theme for comfortable viewing
✅ **Local Storage** - All tasks are saved locally in your browser
✅ **Responsive Design** - Works perfectly on desktop, tablet, and mobile

### AI Chatbot Features

The integrated AI assistant can help you:
- Add tasks using natural language commands
- Get help with task management
- Learn about app features
- Manage priorities and deadlines through conversation
- Receive intelligent suggestions and guidance

## Technology Stack

- **Framework**: Next.js 15
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Date Handling**: date-fns
- **Voice Features**: Web Speech API

## Getting Started

### Prerequisites

- Node.js 18 or higher
- npm, yarn, or pnpm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3002](http://localhost:3002) in your browser

### Available Scripts

- `npm run dev` - Start development server on port 3002
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Usage

### Adding Tasks

1. Enter a task title in the input field
2. Optionally add a description
3. Select priority (Low, Medium, High)
4. Optionally set a due date and time
5. Click "Add Task" or press Enter

### Voice Input

Click the microphone icon to use voice recognition for adding tasks. The app will transcribe your speech into the task title field.

### Managing Tasks

- **Mark Complete**: Click the checkbox to toggle task completion
- **Delete**: Click the trash icon to remove a task
- **Listen**: Click the speaker icon to hear the task read aloud

### Filtering

Use the search bar and filter dropdowns to:
- Search by task title or description
- Filter by priority (All, High, Medium, Low)
- Filter by status (All, Pending, In Progress, Completed)

## Project Structure

```
asif_todo_app/
├── app/
│   ├── globals.css          # Global styles with dark theme
│   ├── layout.tsx            # Root layout component
│   └── page.tsx              # Main todo app page
├── public/                   # Static assets
├── package.json              # Dependencies and scripts
├── tsconfig.json             # TypeScript configuration
├── tailwind.config.ts        # Tailwind CSS configuration
├── next.config.ts            # Next.js configuration
└── README.md                 # This file
```

## Design Features

### Dark Theme

The app features a stunning dark theme with:
- Gradient backgrounds (gray-950 to black)
- Glass-morphism effects with backdrop blur
- Accent colors: Blue and Purple gradients
- Color-coded priorities and statuses

### Color Scheme

- **High Priority**: Red tones
- **Medium Priority**: Yellow/Amber tones
- **Low Priority**: Green tones
- **Completed Status**: Emerald tones
- **In Progress Status**: Blue tones
- **Pending Status**: Gray tones

## Browser Compatibility

- Chrome/Edge: Full support including voice features
- Firefox: Full support except voice features
- Safari 14.1+: Full support including voice features

## Author

**Asif Ali AstolixGen**

Created for GIAIC (Governor's Initiative for Artificial Intelligence and Computing) Hackathon 2026

## License

This project is created for educational purposes as part of the GIAIC Hackathon.

## Acknowledgments

- Original concept inspired by Sharmeen's TaskFlow project
- Built with Next.js and modern web technologies
- Designed for the GIAIC Hackathon competition
