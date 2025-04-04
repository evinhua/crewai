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

## Requirements

- Python 3.8+
- OpenAI API key
- SerperDev API key

## Setup

1. Clone the repository
2. Install dependencies: `pip install crewai langchain-openai python-dotenv crewai-tools`
3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SERPER_API_KEY=your_serper_api_key
   ```

## Usage

Run the script:
```
python content_creation_crew.py
```

Follow the prompts to specify:
- Content type (blog, social, email)
- Topic
- Target audience
- Desired tone

The system will generate the content and save it as a markdown file.

## License

MIT
