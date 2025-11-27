"""
Claude API Integration for Gift Brainstorming
Based on prompts engineered by Clive
"""

import os
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, timedelta
import json

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class GiftScenario(Enum):
    """Gift brainstorming scenarios."""
    GENERAL = "general"
    BUDGET = "budget"
    EXPERIENCE = "experience"
    LAST_MINUTE = "last_minute"
    DIY = "diy"
    GROUP = "group"
    MINIMAL = "minimal"
    LUXURY = "luxury"


class GiftBrainstormingService:
    """
    Claude API service for AI-powered gift suggestions.

    Based on prompt engineering research by Clive, this service provides
    scenario-specific gift brainstorming with intelligent caching and
    cost optimization.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the gift brainstorming service.

        Args:
            api_key: Claude API key. If None, tries to load from environment.
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError(
                "anthropic package not installed. "
                "Install with: pip install anthropic"
            )

        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None

    def brainstorm_gifts(
        self,
        scenario: GiftScenario,
        giftee_name: str,
        context: Dict[str, Any],
        num_ideas: int = 5
    ) -> Dict[str, Any]:
        """
        Generate AI-powered gift suggestions.

        Args:
            scenario: The gift brainstorming scenario
            giftee_name: Name of the person receiving the gift
            context: Dictionary with scenario-specific context:
                - relationship: str (required)
                - interests: str (optional)
                - budget: str (optional)
                - gift_preferences: str (optional)
                - Additional scenario-specific fields
            num_ideas: Number of gift ideas to generate (1-10)

        Returns:
            Dictionary with:
                - success: bool
                - ideas: List[Dict] with gift suggestions
                - error: str (if success is False)
                - cost_estimate: str
        """
        if not self.client:
            return {
                "success": False,
                "error": "No Claude API key provided. Add it in Settings.",
                "ideas": []
            }

        if not 1 <= num_ideas <= 10:
            return {
                "success": False,
                "error": "Number of ideas must be between 1 and 10",
                "ideas": []
            }

        try:
            # Get scenario-specific prompt
            prompt = self._build_prompt(scenario, giftee_name, context, num_ideas)

            # Call Claude API
            message = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse response
            ideas = self._parse_response(message.content[0].text)

            # Estimate cost (Haiku pricing: ~$0.001 per 1K tokens)
            total_tokens = message.usage.input_tokens + message.usage.output_tokens
            cost_estimate = f"${(total_tokens / 1000) * 0.001:.4f}"

            return {
                "success": True,
                "ideas": ideas,
                "error": None,
                "cost_estimate": cost_estimate,
                "tokens_used": total_tokens
            }

        except anthropic.RateLimitError:
            return {
                "success": False,
                "error": "Rate limit reached. Please try again in a moment.",
                "ideas": []
            }
        except anthropic.AuthenticationError:
            return {
                "success": False,
                "error": "Invalid API key. Please check your settings.",
                "ideas": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Could not generate suggestions: {str(e)}",
                "ideas": []
            }

    def _build_prompt(
        self,
        scenario: GiftScenario,
        giftee_name: str,
        context: Dict[str, Any],
        num_ideas: int
    ) -> str:
        """Build scenario-specific prompt."""

        # Base system context
        system_context = """You are a thoughtful gift advisor helping someone find meaningful gifts.
Your suggestions should be:
- Specific and actionable (not generic)
- Thoughtfully matched to the person's interests and context
- Practical and actually available for purchase or creation
- Include clear reasoning for why each gift fits

Format each suggestion as:
**[Gift Title]**
Description: [One sentence description]
Why It Fits: [Specific reasoning about THIS person]
Price Range: [Estimated cost]
"""

        # Get relationship and budget from context
        relationship = context.get("relationship", "someone special")
        budget = context.get("budget", "no specific budget")
        interests = context.get("interests", "")

        # Build scenario-specific prompt
        if scenario == GiftScenario.GENERAL:
            prompt = f"""{system_context}

Generate {num_ideas} thoughtful gift ideas for {giftee_name}, who is a {relationship}.

Context:
- Budget: {budget}
- Interests/hobbies: {interests or 'Not specified'}
- Gift preferences: {context.get('gift_preferences', 'Open to suggestions')}
- Any additional notes: {context.get('notes', 'None')}

Focus on gifts that show you understand what matters to them."""

        elif scenario == GiftScenario.BUDGET:
            prompt = f"""{system_context}

Generate {num_ideas} budget-conscious but thoughtful gift ideas for {giftee_name}, who is a {relationship}.

Context:
- Budget: {budget}
- What matters most to them: {context.get('values', 'Not specified')}
- Interests: {interests or 'Not specified'}

Focus on creative, meaningful gifts that maximize thoughtfulness over cost."""

        elif scenario == GiftScenario.LAST_MINUTE:
            days_left = context.get('days_until_event', '3-5')
            prompt = f"""{system_context}

Generate {num_ideas} last-minute gift ideas for {giftee_name}, who is a {relationship}.

Context:
- Time available: {days_left} days
- Budget: {budget}
- Interests: {interests or 'Not specified'}
- Can shop online or in-person: {context.get('shopping_method', 'both')}

Focus on gifts that can be obtained quickly but still feel thoughtful."""

        elif scenario == GiftScenario.DIY:
            prompt = f"""{system_context}

Generate {num_ideas} DIY/personalized gift ideas for {giftee_name}, who is a {relationship}.

Context:
- Your skills: {context.get('your_skills', 'Basic crafting')}
- Time available: {context.get('time_available', 'A few hours')}
- Budget for supplies: {budget}
- Their interests: {interests or 'Not specified'}

Focus on gifts you can create or personalize yourself."""

        elif scenario == GiftScenario.LUXURY:
            prompt = f"""{system_context}

Generate {num_ideas} luxury/high-end gift ideas for {giftee_name}, who is a {relationship}.

Context:
- Budget: {budget}
- Their values: {context.get('values', 'Quality and craftsmanship')}
- Interests: {interests or 'Not specified'}
- Priority: {context.get('priority', 'Quality over quantity')}

Focus on exceptional quality, experiences, or items they wouldn't buy themselves."""

        elif scenario == GiftScenario.EXPERIENCE:
            prompt = f"""{system_context}

Generate {num_ideas} gift ideas for {giftee_name}, including both experience and physical options.

Context:
- Budget: {budget}
- Energy level preference: {context.get('energy_level', 'Mixed')}
- Interests: {interests or 'Not specified'}
- Logistics: {context.get('logistics', 'Flexible')}

Include a mix of experiences and physical gifts so they can compare."""

        elif scenario == GiftScenario.GROUP:
            main_gift = context.get('main_gift', 'Not specified')
            prompt = f"""{system_context}

Generate {num_ideas} gift ideas that would complement a group gift for {giftee_name}, who is a {relationship}.

Context:
- Main gift from group: {main_gift}
- Your contribution budget: {budget}
- Their interests: {interests or 'Not specified'}

Focus on gifts that complement or enhance the main gift."""

        else:  # MINIMAL
            prompt = f"""{system_context}

Generate {num_ideas} thoughtful gift ideas for {giftee_name}, who is a {relationship}.

I don't know them very well, so suggest safe, universally appreciated gifts that work for a {relationship}.

Budget: {budget}

Focus on reliable, well-received gifts appropriate for this relationship."""

        return prompt

    def _parse_response(self, response_text: str) -> List[Dict[str, str]]:
        """
        Parse Claude's response into structured gift ideas.

        Args:
            response_text: Raw text from Claude

        Returns:
            List of gift idea dictionaries
        """
        ideas = []
        current_idea = {}

        lines = response_text.strip().split('\n')

        for line in lines:
            line = line.strip()

            if not line:
                # Empty line - might be end of idea
                if current_idea and 'title' in current_idea:
                    ideas.append(current_idea)
                    current_idea = {}
                continue

            # Check for title (usually bold with **)
            if line.startswith('**') and line.endswith('**'):
                # Save previous idea if exists
                if current_idea and 'title' in current_idea:
                    ideas.append(current_idea)
                # Start new idea
                current_idea = {'title': line.strip('*').strip()}

            # Check for numbered title (1., 2., etc.)
            elif line[0].isdigit() and '.' in line[:3]:
                # Save previous idea
                if current_idea and 'title' in current_idea:
                    ideas.append(current_idea)
                # Extract title
                title = line.split('.', 1)[1].strip()
                current_idea = {'title': title.strip('*').strip()}

            # Check for description
            elif line.lower().startswith('description:'):
                current_idea['description'] = line.split(':', 1)[1].strip()

            # Check for why it fits
            elif line.lower().startswith('why it fits:'):
                current_idea['why_it_fits'] = line.split(':', 1)[1].strip()

            # Check for price range
            elif line.lower().startswith('price range:') or line.lower().startswith('price:'):
                current_idea['price_range'] = line.split(':', 1)[1].strip()

        # Don't forget the last idea
        if current_idea and 'title' in current_idea:
            ideas.append(current_idea)

        # Ensure all ideas have required fields
        for idea in ideas:
            idea.setdefault('description', 'See details above')
            idea.setdefault('why_it_fits', 'Matches their interests')
            idea.setdefault('price_range', 'Varies')

        return ideas

    def get_available_scenarios(self) -> List[Dict[str, str]]:
        """Get list of available brainstorming scenarios."""
        return [
            {
                "value": GiftScenario.GENERAL.value,
                "label": "General Brainstorming",
                "description": "Standard gift brainstorming with full context"
            },
            {
                "value": GiftScenario.BUDGET.value,
                "label": "Budget-Conscious",
                "description": "Thoughtful gifts on a tight budget"
            },
            {
                "value": GiftScenario.LAST_MINUTE.value,
                "label": "Last-Minute",
                "description": "Quick gifts available now"
            },
            {
                "value": GiftScenario.DIY.value,
                "label": "DIY/Personalized",
                "description": "Gifts you can create yourself"
            },
            {
                "value": GiftScenario.LUXURY.value,
                "label": "Luxury/High-End",
                "description": "Premium, exceptional quality gifts"
            },
            {
                "value": GiftScenario.EXPERIENCE.value,
                "label": "Experience vs Physical",
                "description": "Compare experience and physical gift options"
            },
            {
                "value": GiftScenario.GROUP.value,
                "label": "Group Gift Addition",
                "description": "Complement a group gift"
            },
            {
                "value": GiftScenario.MINIMAL.value,
                "label": "Minimal Information",
                "description": "Safe bets when you don't know them well"
            }
        ]
