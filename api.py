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
    goal="Gather comprehensive, accurate, and up-to-date information on assigned topics from multiple authoritative sources",
    backstory="""You are an elite researcher with a PhD in information science and 15 years of experience in 
    investigative journalism. You have exceptional skills in finding high-quality, relevant information from 
    diverse sources. You're known for your ability to uncover unique insights, fact-check thoroughly, and 
    organize information in a way that reveals patterns and connections others miss. You always prioritize 
    credible sources and verify information across multiple references before including it in your research.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, scrape_tool]
)

content_writer = Agent(
    role="Content Writer",
    goal="Create engaging, informative, and highly valuable content based on thorough research",
    backstory="""You are an award-winning writer with over a decade of experience creating content that 
    captivates audiences and drives engagement. You've written for major publications like The New York Times, 
    Wired, and The Atlantic. Your content consistently achieves high engagement metrics because you understand 
    how to craft compelling narratives, use persuasive language, and structure information for maximum impact. 
    You excel at adapting your writing style to different audiences and formats while maintaining a clear, 
    authoritative voice that builds trust with readers.""",
    verbose=True,
    allow_delegation=True
)

editor = Agent(
    role="Content Editor",
    goal="Transform good content into exceptional content through meticulous editing and refinement",
    backstory="""You are a renowned editor who has worked with bestselling authors and top publications. 
    With your background in linguistics and psychology, you understand not just the mechanics of language 
    but how words influence readers' perceptions and decisions. You've edited content that has won industry 
    awards and consistently increased audience engagement metrics by at least 40%. You have an uncanny ability 
    to identify structural weaknesses, logical inconsistencies, and missed opportunities in content. Your 
    editing approach balances preserving the writer's unique voice while ensuring clarity, coherence, and 
    maximum impact.""",
    verbose=True,
    allow_delegation=False
)

seo_specialist = Agent(
    role="SEO Specialist",
    goal="Maximize content visibility and organic traffic through advanced SEO strategies",
    backstory="""You are a leading SEO strategist who has helped Fortune 500 companies and high-growth 
    startups achieve top search rankings in highly competitive industries. With certifications from Google 
    and over 8 years of experience, you stay ahead of algorithm changes and industry trends. You've developed 
    proprietary methods for keyword research and content optimization that consistently outperform standard 
    approaches. Your holistic approach to SEO integrates technical expertise, content strategy, and user 
    experience optimization. You're skilled at finding the perfect balance between search engine requirements 
    and creating content that resonates with human readers.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool]
)

@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    try:
        # Get content info from request
        content_info = request.json
        
        print(f"Received request to generate {content_info['contentType']} content about {content_info['topic']}")
        
        # Define the tasks
        research_task = Task(
            description=f"""
            Conduct comprehensive research on the topic: {content_info['topic']}
            
            Your mission is to gather in-depth, authoritative information specifically tailored for 
            {content_info['targetAudience']}. This is not a surface-level investigation - dig deep 
            and uncover insights that would not be immediately obvious to casual researchers.
            
            You must gather:
            1. Verified facts and current statistics with specific numbers and dates (minimum 5)
            2. Latest industry trends and developments from the past 6 months
            3. Common pain points, questions, and challenges faced by {content_info['targetAudience']} related to this topic
            4. At least 3 expert opinions or perspectives from recognized authorities in the field
            5. Counterintuitive insights or surprising information that challenges common assumptions
            6. Specific examples, case studies, or real-world applications
            7. Emerging research or future predictions from credible sources
            
            Research methodology requirements:
            - IMPORTANT: You MUST use the SerperDevTool (search_tool) to find current information from diverse sources
            - IMPORTANT: You MUST use the ScrapeWebsiteTool (scrape_tool) to extract detailed content from authoritative websites
            - For each subtopic, perform at least 2 separate searches with different search queries
            - For each important claim or statistic, verify it by scraping at least 2 different authoritative websites
            - Use specific search queries like "{content_info['topic']} latest statistics 2025" or "{content_info['topic']} expert opinions"
            - After finding a promising search result, use the scrape_tool to extract the full content from that webpage
            - Cross-verify all facts across multiple sources before including them
            - Prioritize primary sources and peer-reviewed research when available
            - Include direct quotes from experts when relevant
            - Note any contradictory information or debates within the field
            - Organize findings by subtopic with clear headings
            
            Your final research document must be comprehensive, well-structured, and include:
            - A summary of key findings
            - 7-10 specific, actionable insights organized by subtopic
            - Citations for all sources used (including URLs)
            - Specific recommendations for content angles that would resonate with {content_info['targetAudience']}
            """,
            expected_output=f"""A meticulously researched, fact-rich document on {content_info['topic']} containing:
            1. An executive summary of key findings
            2. 7-10 specific, actionable insights organized by clear subtopics
            3. Verified statistics and facts with specific numbers and dates
            4. Expert quotes and perspectives from recognized authorities
            5. Emerging trends and future predictions
            6. Specific examples and case studies
            7. Full citations for all sources with URLs
            8. Content angle recommendations tailored to {content_info['targetAudience']}""",
            agent=researcher
        )

        writing_task = Task(
            description=f"""
            Create exceptional {content_info['contentType']} content about {content_info['topic']} based on the comprehensive research provided.
            
            Content requirements:
            - Written in a {content_info['tone']} tone that perfectly resonates with {content_info['targetAudience']}
            - Incorporate all key insights from the research in a natural, flowing narrative
            - Use persuasive, engaging language that compels the reader to continue
            - Include specific facts, statistics, and expert quotes to build credibility
            - Address the specific pain points and questions of {content_info['targetAudience']}
            - Use storytelling techniques to make complex information relatable and memorable
            - Create a strong emotional connection with the reader
            
            Structural requirements:
            
            For a blog post:
            - Create 3-5 compelling headline options using proven formulas for high CTR
            - Write an attention-grabbing introduction that hooks the reader immediately
            - Develop 4-6 main sections with descriptive subheadings
            - Include a mix of paragraph lengths for readability (some short, some medium)
            - Use bullet points and numbered lists where appropriate
            - Add thought-provoking questions throughout to maintain engagement
            - Create a powerful conclusion with a clear takeaway and call to action
            
            For social media:
            - Create 5-7 distinct posts with varying lengths and approaches
            - Include attention-grabbing opening lines for each post
            - Craft compelling calls to action for each post
            - Suggest relevant hashtags (mix of popular and niche)
            - Include ideas for visual content to accompany each post
            - Tailor each post for the specific platform (Twitter, LinkedIn, Facebook, Instagram)
            
            For email:
            - Create 3-5 subject line options with high open-rate potential
            - Write a personalized, engaging greeting
            - Craft a concise, value-focused body with clear sections
            - Use persuasive language that drives specific action
            - Create a strong, urgent call to action
            - Include a P.S. section with additional value or urgency
            
            Your content must be:
            - Original and free from plagiarism
            - Factually accurate and well-supported
            - Structured for maximum readability and engagement
            - Tailored specifically to resonate with {content_info['targetAudience']}
            - Written in a {content_info['tone']} tone consistently throughout
            """,
            expected_output=f"""A exceptional, highly engaging {content_info['contentType']} piece about {content_info['topic']} 
            written in a perfect {content_info['tone']} tone specifically crafted for {content_info['targetAudience']}. 
            The content will incorporate all research insights in a compelling narrative structure with attention-grabbing headlines, 
            varied formatting for readability, specific facts and statistics, emotional storytelling elements, and strong calls to action.""",
            agent=content_writer,
            context=[research_task]
        )

        editing_task = Task(
            description=f"""
            Transform the {content_info['contentType']} content about {content_info['topic']} from good to exceptional through meticulous editing.
            
            Your editing process must include these comprehensive checks and improvements:
            
            Content Quality:
            - Verify all facts, statistics, and claims against the original research
            - Ensure all information is current, accurate, and properly contextualized
            - Identify and fill any information gaps that would leave readers with questions
            - Strengthen weak arguments with additional evidence or reasoning
            - Enhance the persuasiveness and impact of key points
            - Ensure the content delivers exceptional value to {content_info['targetAudience']}
            
            Structure and Flow:
            - Optimize the overall structure for logical progression and maximum impact
            - Ensure smooth transitions between paragraphs and sections
            - Verify that the introduction effectively hooks the reader and sets expectations
            - Confirm that the conclusion reinforces key points and drives desired action
            - Assess and improve the rhythm and pacing of the content
            
            Language and Style:
            - Refine language for precision, clarity, and impact
            - Eliminate redundancies, clichés, and weak phrasing
            - Enhance the {content_info['tone']} tone to perfectly match expectations of {content_info['targetAudience']}
            - Vary sentence structure and length for improved readability and engagement
            - Replace generic terms with more specific, vivid, and impactful language
            - Ensure consistent voice and perspective throughout
            
            Technical Quality:
            - Correct all grammar, spelling, and punctuation errors
            - Optimize paragraph length and structure for digital readability
            - Improve formatting for visual appeal and ease of scanning
            - Verify proper use of headings, subheadings, and formatting elements
            - Ensure consistent style (capitalization, abbreviations, number formatting, etc.)
            
            Engagement Factors:
            - Strengthen headlines, subheadings, and opening lines for maximum impact
            - Enhance storytelling elements and emotional appeal
            - Improve calls to action for higher conversion potential
            - Add rhetorical questions or provocative statements where appropriate
            - Ensure the content creates a connection with {content_info['targetAudience']}
            
            Provide detailed feedback on:
            1. Major structural changes made and why
            2. Content additions or removals and their purpose
            3. Stylistic improvements and their intended effect
            4. Any factual corrections or clarifications
            5. Overall assessment of the content's strengths and remaining opportunities
            
            Your edited version must maintain the writer's core message and unique voice while significantly 
            elevating the quality, impact, and effectiveness of the content.
            """,
            expected_output=f"""A dramatically improved version of the {content_info['contentType']} content with:
            1. Enhanced structure, flow, and readability
            2. Strengthened arguments and supporting evidence
            3. Refined language for maximum impact and engagement
            4. Perfect alignment with the {content_info['tone']} tone expected by {content_info['targetAudience']}
            5. Flawless grammar, spelling, and technical elements
            6. Optimized headlines, transitions, and calls to action
            
            Plus a detailed editorial report explaining:
            - Major changes made and their strategic purpose
            - Content strengths and how they were amplified
            - Weaknesses that were addressed and how
            - Overall assessment of the content's quality and effectiveness""",
            agent=editor,
            context=[writing_task]
        )

        seo_task = Task(
            description=f"""
            Develop and implement an advanced SEO strategy for the {content_info['contentType']} content about {content_info['topic']} 
            that will maximize its search visibility and organic traffic potential.
            
            Your comprehensive SEO optimization must include:
            
            Strategic Keyword Analysis:
            - IMPORTANT: You MUST use the SerperDevTool (search_tool) to conduct in-depth keyword research specific to {content_info['topic']}
            - Use specific search queries like:
              * "{content_info['topic']} keyword research"
              * "{content_info['topic']} SEO trends"
              * "best keywords for {content_info['topic']}"
              * "{content_info['topic']} search volume"
              * "{content_info['topic']} for {content_info['targetAudience']}"
            - Identify high-value primary and secondary keywords based on:
              * Search volume and trends (use specific numbers)
              * Competition difficulty (use specific metrics)
              * Relevance to {content_info['targetAudience']}
              * Commercial intent and conversion potential
              * Question-based searches and featured snippet opportunities
            - Analyze the top 5 ranking pages for target keywords to identify patterns and opportunities
            - Discover untapped keyword opportunities with lower competition
            
            Content Optimization Recommendations:
            - Create 3-5 highly optimized title options that include primary keywords naturally
            - Develop a compelling meta description with keywords and click-inducing language
            - Suggest strategic improvements to H1, H2, and H3 headings for keyword inclusion
            - Identify opportunities to naturally incorporate keywords in:
              * First and last paragraphs
              * Image alt text and captions
              * Anchor text for internal and external links
            - Recommend semantic keywords and related terms to enhance topical relevance
            
            Technical SEO Enhancements:
            - Suggest optimal content length based on SERP analysis for the target keywords
            - Recommend schema markup opportunities specific to this content type and topic
            - Identify opportunities for featured snippets, knowledge panels, or rich results
            - Suggest URL structure optimization if applicable
            
            User Experience & Engagement Optimization:
            - Recommend improvements to enhance dwell time and reduce bounce rate
            - Suggest formatting changes to improve readability and scannability
            - Identify opportunities to add engaging, shareable elements
            
            Strategic Link Building:
            - Recommend 5-7 specific high-authority websites for potential outreach
            - Suggest internal linking opportunities within the existing site
            - Identify specific anchor text recommendations for maximum SEO benefit
            
            Your SEO recommendations must be:
            - Data-driven with specific metrics where possible
            - Tailored specifically to {content_info['topic']} and {content_info['targetAudience']}
            - Designed to balance search optimization with user experience
            - Aligned with current search engine algorithms and best practices
            - Prioritized by potential impact and implementation difficulty
            
            Provide your recommendations in a clear, actionable format that can be implemented immediately.
            """,
            expected_output=f"""A comprehensive SEO optimization strategy for the {content_info['contentType']} content including:
            
            1. Detailed Keyword Analysis:
               - Primary keywords with search volumes and competition metrics
               - Secondary and long-tail keyword opportunities
               - Question-based search opportunities
               - Competitor keyword analysis insights
            
            2. On-Page Optimization Recommendations:
               - 3-5 optimized title options with primary keywords
               - Compelling meta description with keywords
               - Heading structure improvements (H1, H2, H3)
               - Keyword placement recommendations throughout content
               - Content length and structure recommendations
            
            3. Technical SEO Enhancements:
               - Schema markup recommendations
               - Featured snippet optimization opportunities
               - URL structure suggestions
            
            4. User Experience Improvements:
               - Readability and engagement enhancements
               - Formatting recommendations for improved metrics
            
            5. Link Building Strategy:
               - 5-7 specific outreach targets with rationale
               - Internal linking recommendations
               - Anchor text suggestions
            
            6. Implementation Roadmap:
               - Prioritized list of changes by impact
               - Before/after examples of key elements""",
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
        
        print("Content generation complete!")
        
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
        error_message = str(e)
        print(f"Error occurred: {error_message}")
        return jsonify({
            'status': 'error',
            'message': error_message
        }), 500

if __name__ == '__main__':
    print("Starting CrewAI Content Creation API on http://localhost:5000")
    app.run(debug=True, port=5000)
