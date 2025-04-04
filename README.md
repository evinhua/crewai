# CrewAI Content Creation System

A system that uses CrewAI to generate high-quality content with a team of AI agents working together.

## Overview

This project implements a content creation workflow using CrewAI, where multiple specialized AI agents collaborate to produce polished content. The crew includes:

- Research Specialist: Gathers comprehensive information on the topic
- Content Writer: Creates engaging content based on research
- Content Editor: Refines and polishes the content
- SEO Specialist: Optimizes content for search engines

## Features

- Generate blog posts, social media content, or email marketing materials
- Customizable content topics, target audience, and tone
- Web search integration using SerperDev API
- Web scraping capabilities for research
- Automated content refinement and SEO optimization
- React-based UI for easy content generation

## Project Structure

- `content_creation_crew.py` - Main script for CLI-based content generation
- `api.py` - Flask API for the React frontend
- `crewai-ui/` - React frontend application

## Requirements

- Python 3.8+
- Node.js and npm
- OpenAI API key
- SerperDev API key

## Setup

1. Clone the repository
2. Install Python dependencies: `pip install crewai langchain-openai python-dotenv crewai-tools flask flask-cors`
3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SERPER_API_KEY=your_serper_api_key
   ```
4. Install React dependencies:
   ```
   cd crewai-ui
   npm install
   ```

## Usage

### CLI Version
Run the script:
```
python content_creation_crew.py
```

### Web Version
1. Start the Flask API:
```
python api.py
```

2. Start the React development server:
```
cd crewai-ui
npm start
```

3. Open your browser to http://localhost:3000

Follow the prompts to specify:
- Content type (blog, social, email)
- Topic
- Target audience
- Desired tone

The system will generate the content and display it in the UI or save it as a markdown file.

## License

MIT
