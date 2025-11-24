# Movie Recommendation Frontend

Modern frontend for the Movie Recommendation API built with HTML and Sass.

## Features

- 🎨 Modern, responsive design
- 🔍 Movie search functionality
- ✨ AI-powered recommendations
- 📱 Mobile-friendly interface
- ⚡ Fast and lightweight

## Setup

### Install Dependencies

```bash
npm install
```

### Build CSS

Compile Sass to CSS:

```bash
npm run build:css
```

Or watch for changes:

```bash
npm run watch:css
```

### Build Everything

```bash
npm run build
```

## Development

### Watch Sass Files

```bash
npm run dev
```

This will watch for changes in `src/scss/` and automatically compile to `dist/css/`.

### Manual Setup (without npm)

If you prefer not to use npm, you can compile Sass manually:

```bash
# Install Sass globally (one time)
npm install -g sass

# Compile
sass src/scss/main.scss dist/css/main.css

# Watch mode
sass --watch src/scss/main.scss dist/css/main.css
```

## File Structure

```
frontend/
├── index.html          # Main HTML file
├── src/
│   ├── scss/          # Sass source files
│   │   ├── _variables.scss
│   │   ├── _mixins.scss
│   │   └── main.scss
│   └── js/            # JavaScript source
│       └── main.js
├── dist/              # Compiled files (generated)
│   ├── css/
│   │   └── main.css
│   └── js/
│       └── main.js
└── package.json       # npm configuration
```

## Usage

1. Make sure your FastAPI backend is running at `http://127.0.0.1:8000`
2. Open `index.html` in your browser
3. Search for movies or get recommendations!

## API Configuration

The frontend connects to the API at `http://127.0.0.1:8000` by default. To change this, edit the `API_BASE_URL` constant in `src/js/main.js`.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

