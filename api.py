"""
CrewAI Content Creation API

This script creates a Flask API that interfaces with the CrewAI content creation system.
It allows the React frontend to send requests to generate content.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Import CrewAI components
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Define the agents with tools
researcher = Agent(
    role="Research Specialist",
    goal="Gather comprehensive, accurate information on assigned topics",
    backstory="""You are an expert researcher with a talent for finding relevant, 
    accurate, and engaging information. You have years of experience researching 
    various topics and know how to identify credible sources and key insights.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, scrape_tool]
)

content_writer = Agent(
    role="Content Writer",
    goal="Create engaging, informative content based on research",
    backstory="""You are a skilled writer with experience creating compelling blog posts
    and marketing materials. You know how to structure content for readability and engagement,
    and you have a knack for adapting your tone to different audiences and purposes.""",
    verbose=True,
    allow_delegation=True
)

editor = Agent(
    role="Content Editor",
    goal="Refine and polish content for clarity, accuracy, and engagement",
    backstory="""You are a meticulous editor with an eye for detail and a commitment to quality.
    You can spot inconsistencies, awkward phrasing, and factual errors, and you know how to
    improve content without losing the writer's voice.""",
    verbose=True,
    allow_delegation=False
)

seo_specialist = Agent(
    role="SEO Specialist",
    goal="Optimize content for search engines while maintaining readability",
    backstory="""You are an SEO expert who understands how to make content discoverable
    without sacrificing quality. You know the latest SEO best practices and can identify
    valuable keywords and optimization opportunities.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool]
)

@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    try:
        # Get content info from request
        content_info = request.json
        
        # Define the tasks
        research_task = Task(
            description=f"""
            Research the topic: {content_info['topic']}
            
            Focus your research on information that would be relevant and valuable to 
            {content_info['targetAudience']}.
            
            Gather the following:
            1. Key facts and statistics about the topic
            2. Current trends or developments
            3. Common questions or pain points related to the topic
            4. Credible sources that could be cited
            5. Interesting angles or perspectives on the topic
            
            Use the search tool to find relevant information and the scrape tool to extract content from websites.
            Compile your findings in a structured format that can be used by the content writer.
            Include at least 5-7 key points that should be covered in the content.
            """,
            expected_output=f"""A comprehensive research document on {content_info['topic']} containing key facts, 
            statistics, trends, common questions, credible sources, and interesting perspectives. 
            The document should include 5-7 key points organized in a clear structure for the content writer to use.""",
            agent=researcher
        )

        writing_task = Task(
            description=f"""
            Create {content_info['contentType']} content about {content_info['topic']} based on the research provided.
            
            The content should:
            - Be written in a {content_info['tone']} tone
            - Target {content_info['targetAudience']}
            - Include the key points from the research
            - Be engaging and informative
            
            For a blog post: Create a compelling headline, introduction, 3-5 main sections with subheadings, and a conclusion.
            For social media: Create 3-5 posts with appropriate hashtags and calls to action.
            For email: Create a subject line and email body with a clear call to action.
            
            Make the content compelling and valuable to the target audience.
            """,
            expected_output=f"""A complete {content_info['contentType']} piece about {content_info['topic']} 
            written in a {content_info['tone']} tone for {content_info['targetAudience']}. 
            The content will incorporate all key research points in an engaging and structured format.""",
            agent=content_writer,
            context=[research_task]
        )

        editing_task = Task(
            description=f"""
            Edit and refine the {content_info['contentType']} content about {content_info['topic']}.
            
            Check for:
            1. Clarity and coherence
            2. Grammar and spelling errors
            3. Factual accuracy
            4. Appropriate tone for {content_info['targetAudience']}
            5. Logical flow and structure
            
            Make necessary improvements while preserving the writer's voice and the key messages.
            Provide specific feedback on what was changed and why.
            """,
            expected_output=f"""A polished and refined version of the {content_info['contentType']} content 
            with improved clarity, grammar, accuracy, tone, and structure. The output should include 
            both the edited content and specific feedback on the changes made.""",
            agent=editor,
            context=[writing_task]
        )

        seo_task = Task(
            description=f"""
            Optimize the {content_info['contentType']} content about {content_info['topic']} for search engines.
            
            Your optimization should:
            1. Identify 3-5 relevant keywords or phrases that the content should target
            2. Suggest improvements to the title/headline for SEO
            3. Recommend meta description text (if applicable)
            4. Suggest improvements to headings and subheadings
            5. Identify opportunities for internal or external links
            
            Use the search tool to research popular keywords and SEO trends related to the topic.
            Make sure your suggestions maintain readability and don't compromise the quality or tone of the content.
            The target audience is {content_info['targetAudience']}.
            """,
            expected_output=f"""An SEO optimization report for the {content_info['contentType']} content that includes 
            3-5 target keywords, improved title suggestions, meta description recommendations, heading improvements, 
            and link opportunities. The report should maintain the content's readability and quality while enhancing 
            its search engine visibility.""",
            agent=seo_specialist,
            context=[editing_task]
        )

        # Create the crew
        content_creation_crew = Crew(
            agents=[researcher, content_writer, editor, seo_specialist],
            tasks=[research_task, writing_task, editing_task, seo_task],
            verbose=True,
            process=Process.sequential
        )

        # Run the crew
        result = content_creation_crew.kickoff()
        
        # Format the result
        if hasattr(result, 'raw'):
            content = str(result.raw)
        elif hasattr(result, 'final_output'):
            content = str(result.final_output)
        else:
            content = str(result)
            
        # Create response
        response = {
            'status': 'success',
            'content': content,
            'metadata': {
                'contentType': content_info['contentType'],
                'topic': content_info['topic'],
                'targetAudience': content_info['targetAudience'],
                'tone': content_info['tone'],
                'timestamp': datetime.now().isoformat()
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
