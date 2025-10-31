"""
Prompt templates for LLM-based script generation
"""


class PromptTemplates:
    """Collection of prompt templates for different content types"""
    
    SCRIPT_GENERATION = """You are a viral YouTube Shorts scriptwriter. Create an ENGAGING, ENTHUSIASTIC script from this fact.

FACT: {fact}

YOUR TASK: Transform this dry fact into an EXCITING 30-second narration script.

IMPORTANT RULES:
1. Start with a question or shocking statement to hook viewers
2. Explain the fact in simple, conversational language
3. Add excitement with phrases like "Believe it or not!", "Get this:", "Here's the crazy part:"
4. End with "Follow for more amazing facts!"
5. Write EXACTLY as someone would SPEAK it out loud
6. Keep it under 50 words total
7. Make every word count!

EXAMPLE (for a different fact):
"Ever wondered how tall the biggest volcano is? Well, Olympus Mons on Mars is THREE times taller than Mount Everest! That's absolutely massive! Scientists are still studying why it got so huge. Follow for more space facts!"

Now write YOUR script based on the fact above.

Return ONLY valid JSON with no other text:
{{
    "hook": "Opening question or shocking statement",
    "script": "Your complete engaging narration script (40-50 words)",
    "title": "Catchy title (under 60 chars)",
    "description": "Brief description with hashtags",
    "hashtags": ["facts", "interesting", "shorts", "viral", "science"],
    "keywords": ["keyword1", "keyword2", "keyword3"]
}}"""

    TITLE_OPTIMIZATION = """Optimize this YouTube Shorts title for maximum engagement and clicks:

Original Title: {title}

Create 3 alternative titles that are:
- Max 60 characters
- Attention-grabbing
- Clear about the content
- Use power words
- Create curiosity without being clickbait

Return as JSON:
{{
    "titles": ["title1", "title2", "title3"]
}}"""

    HASHTAG_GENERATION = """Generate trending YouTube hashtags for this video topic:

Topic: {topic}
Keywords: {keywords}

Generate 10-15 relevant hashtags that:
- Are popular on YouTube Shorts
- Are relevant to the content
- Mix popular and niche hashtags
- Include general (#facts, #interesting) and specific hashtags

Return as JSON:
{{
    "hashtags": ["hashtag1", "hashtag2", ...]
}}"""

    DESCRIPTION_TEMPLATE = """Create an engaging YouTube video description:

Title: {title}
Script: {script}

Generate a description that:
- Summarizes the video in 1-2 sentences
- Includes relevant hashtags
- Has a call-to-action
- Is optimized for YouTube search

Return as plain text."""

    @staticmethod
    def format_script_prompt(fact: str) -> str:
        """Format the main script generation prompt"""
        return PromptTemplates.SCRIPT_GENERATION.format(fact=fact)
    
    @staticmethod
    def format_title_prompt(title: str) -> str:
        """Format the title optimization prompt"""
        return PromptTemplates.TITLE_OPTIMIZATION.format(title=title)
    
    @staticmethod
    def format_hashtag_prompt(topic: str, keywords: list) -> str:
        """Format the hashtag generation prompt"""
        keywords_str = ", ".join(keywords)
        return PromptTemplates.HASHTAG_GENERATION.format(
            topic=topic,
            keywords=keywords_str
        )
    
    @staticmethod
    def format_description_prompt(title: str, script: str) -> str:
        """Format the description generation prompt"""
        return PromptTemplates.DESCRIPTION_TEMPLATE.format(
            title=title,
            script=script
        )
