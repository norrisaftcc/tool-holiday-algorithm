# Gift Brainstorming Prompts for Claude API Integration
## Investigation-Grade Prompts for Optimal Suggestion Generation

*Prepared by: Clive, Prompt Strategy Investigator*
*Purpose: AI-assisted gift ideation using Claude Haiku*
*Tone: Helpful enthusiasm with quiet confidence*

---

## INVESTIGATIVE FRAMEWORK

Before diving into specific prompts, understand the methodology:

### The 5 W's of Gift Context
Each prompt systematically gathers:
- **WHO**: The giftee (relationship, personality, interests)
- **WHAT**: The type of suggestion needed (experience, physical, DIY, etc.)
- **WHEN**: Time constraints (last-minute, advance planning)
- **WHERE**: Context clues (lifestyle, living situation, preferences)
- **WHY**: Purpose (avoid duplication, match personality, respect budget)

### Output Specification Pattern
Every prompt enforces:
1. **Structured ranking** (by appropriateness, not just quality)
2. **Context justification** (why this gift fits THIS person)
3. **Practical metadata** (price, difficulty, where to find)
4. **Actionable next steps** (purchase link, creation hints, customization ideas)

---

## SYSTEM PROMPT: Gift Brainstorming Assistant

Use this as the base system prompt for all gift brainstorming interactions:

```
You are a thoughtful, systematic gift recommendation assistant. Your role is to help users find
the perfect gifts by understanding context deeply and generating suggestions that match real people.

CORE PRINCIPLES:
1. Context is Everything: The more specific details provided, the better your suggestions
2. Avoid Generic Advice: Never suggest "gift card" or "something they like" without specifics
3. Personality First: Gifts should reflect WHO the person is, not just WHAT they like
4. Budget Respect: Always consider financial constraints seriously
5. Thoughtfulness Over Expense: A $20 gift that shows you understand them beats a $200 generic item
6. Duplicate Prevention: Ask about past gifts to avoid repetition

YOUR INTERACTION STYLE:
- Warm and encouraging (you're helping someone express generosity)
- Efficiently organized (clear structure, scannable output)
- Quietly confident (you know gift-giving psychology)
- Celebration-focused (emphasize how good this person will feel)

WHEN INFORMATION IS INCOMPLETE:
- Ask clarifying questions rather than making assumptions
- Provide suggestions for what info would be most helpful
- Never generate suggestions with major unknowns (relationship type, budget, etc.)

OUTPUT FORMAT:
All suggestions must include:
- Title: Simple, direct name for the gift
- Why It Fits: 1-2 sentences explaining the match (this is crucial)
- Price Range: Budget alignment (e.g., $25-40)
- Where to Find: Specific retailers or creation method
- Difficulty: Ease of acquiring/creating (Easy / Moderate / Challenging)
- Customization Ideas: How to personalize it
- Risk Level: How likely they'll already own this (Low / Medium / High)

REMEMBER: You're helping someone reduce cognitive load during a stressful time. Be thorough,
specific, and genuinely helpful. The goal is not volume of ideas but quality of fit.
```

---

## PROMPT 1: General Gift Brainstorming

**Use Case**: User knows the giftee but needs fresh ideas. Starting point for most conversations.

```
I need gift ideas for [GIFTEE_NAME]. Here's what I know:

ABOUT THEM:
- Relationship to me: [e.g., sister, colleague, best friend]
- Age/Age range: [e.g., 28, early 40s]
- Key interests/hobbies: [e.g., hiking, cooking, reading]
- Personality traits: [e.g., practical, adventurous, homebody]
- Living situation: [e.g., small apartment, house with family, dorm]
- Any deal-breakers: [e.g., no physical gifts, allergies, ethical concerns]

MY CONSTRAINTS:
- Budget: [e.g., $30-60]
- Timeline: [e.g., need by December 15th]
- Giving method: [e.g., in-person, shipped, digital]
- Their typical gifting tastes: [e.g., prefer practical over sentimental]

CONTEXT CLUES:
- Gifts I know they've received recently: [e.g., they just got a new coffee maker]
- Things they mention wanting: [e.g., mentioned needing a better rain jacket]
- Things they DON'T like: [e.g., anything pink, food gifts, clothes]
- What would make them happiest: [e.g., something useful, something fun, something thoughtful]

Based on this, generate 5 gift ideas ranked by how well they match this person.
For each idea, explain WHY it fits them specifically (not generic praise).
Include how I could personalize or customize each suggestion.
```

---

## PROMPT 2: Budget-Conscious Gift Ideas

**Use Case**: User has tight budget but wants thoughtful suggestions. Prioritizes creativity over spending.

```
I'm on a tight budget for [GIFTEE_NAME] and want to be thoughtful anyway.

THE PERSON:
- Who they are to me: [relationship]
- What matters to them most: [e.g., experiences, practicality, humor, learning]
- One thing they love: [specific interest]
- One thing they struggle with: [e.g., staying organized, motivation, cooking]

MY CONSTRAINTS:
- Maximum budget: [e.g., $20, $15]
- I can/cannot spend time creating something: [yes/no]
- I can/cannot ship anything: [yes/no]
- Preferred gift category: [e.g., something useful, something fun, something they don't expect]

IMPORTANT CONTEXT:
- They prefer: [e.g., experiences over objects, homemade over bought, practical over sentimental]
- Recent gifts they've mentioned liking: [e.g., a plant, a good pen, a funny mug]
- Things they talk about needing: [e.g., better light for reading, help with sleep]

Generate 4-5 gift ideas that prove meaningful gifts don't require big budgets.
For each:
1. Explain why this specific idea matches them (the "why it fits" is everything)
2. Show exactly how to source or create it within budget
3. Note any free customization options
4. Include one way to elevate it slightly if budget allows

Focus on ideas that show genuine understanding, not ones that feel like budget constraints.
```

---

## PROMPT 3: Experience vs. Physical Gift Ideas

**Use Case**: User uncertain between doing/buying. Generates both categories for comparison.

```
I'm torn between giving [GIFTEE_NAME] an experience or a physical gift.

THE GIFTEE:
- Relationship: [e.g., sister, friend]
- Lifestyle: [e.g., busy professional, full-time student, new parent]
- What energizes them: [e.g., time with people, time alone, learning, adventure]
- Current life phase: [e.g., settling into new job, new relationship, empty nest]
- What they complain about lacking: [e.g., free time, relaxation, excitement, learning opportunities]

MY SITUATION:
- Budget: [amount]
- How much time I can invest: [e.g., planning a day trip, ordering online]
- Logistics: [e.g., can coordinate schedule, live in same city, several states away]
- Their typical preference: [e.g., they love trying new things, they prefer comfort, they're sentimental]

CONTEXT:
- A recent experience they mentioned loving: [e.g., that wine tasting, the hiking trip]
- A physical item they recently expressed need for: [e.g., better pillow, nice jacket]
- Current life squeeze: [e.g., overwhelmed, bored, need relaxation, need stimulation]

Generate both options:

EXPERIENCE IDEAS (3 suggestions):
- What the experience would be
- Why it fits their current life
- How to plan/coordinate it
- Why this beats a physical gift for them right now

PHYSICAL GIFT IDEAS (3 suggestions):
- What the gift is
- Why it solves a real need/desire
- Why this is better than an experience for them
- How to make it special

Then give a recommendation: Based on everything, which category feels better for them right now?
```

---

## PROMPT 4: Last-Minute Gift Ideas

**Use Case**: Time crunch. Prioritizes immediately available options and smart execution.

```
I need a gift for [GIFTEE_NAME] FAST.

THE RUSH:
- Days until I need to give it: [e.g., 2 days, 5 days]
- I need it: [in-hand by DATE, shipped by DATE, digital]
- My location: [relevant for pickup availability]
- Giving method: [in-person, mail, email]

THE PERSON (quick version):
- Core thing about them: [one defining trait or interest]
- Something they'd appreciate: [practical, fun, sentimental, luxe]
- Budget: [amount]
- Deal-breakers: [e.g., can't have anything perishable]

WHAT WON'T WORK:
- Things they already own: [e.g., they have tons of coffee mugs]
- Gifts they've specifically said no to: [e.g., anything requiring time commitment]
- Logistics issues: [e.g., can't be fragile because shipping will be rough]

WHAT MIGHT WORK:
- They recently mentioned: [something specific]
- They don't have enough of: [e.g., good snacks, good socks]
- They're into: [specific interest]

Generate 5 last-minute ideas that are:
1. Actually available within the timeline
2. Not generic "emergency gifts"
3. Still thoughtful despite the rush
4. Specific retailers or instant-delivery options

For each: Include exact next steps (where to buy, how to order, guarantee it arrives in time).
```

---

## PROMPT 5: Personalized / DIY Gift Ideas

**Use Case**: User wants to create something meaningful. Values time and thoughtfulness over money.

```
I want to make [GIFTEE_NAME] something special instead of buying.

THE GIFT MAKER (YOU):
- Crafting skills: [e.g., I'm decent at cooking, I'm artistic, I'm not crafty at all]
- Time available: [e.g., 10 hours, a few weekends, just an hour or two]
- Budget for supplies: [e.g., $25, $50, doesn't matter]
- Preferred creation method: [baking, writing, photography, craft, service, curation]

THE RECIPIENT:
- Relationship: [who they are to you]
- What would mean most: [something handmade, something curated, something experiential]
- Their aesthetic: [minimalist, maximalist, vintage, modern, colorful, monochromatic]
- Practical preference: [they want something useful, decorative, consumable, memorable]
- One thing that describes them: [one essential trait]

CONTEXT:
- Something they've said they wanted: [specific mention]
- A gift they loved from you before: [what worked]
- Things they care about: [their values or priorities]
- How you want them to feel: [specific emotion you're going for]

Generate 5 personalized/DIY gift ideas:

For each include:
1. What you're creating
2. Why this matches them specifically
3. Detailed steps (specific enough to follow)
4. Supply list with costs
5. Estimated time to complete
6. How to present it meaningfully
7. How to handle if it doesn't turn out perfect (grace notes)

Focus on ideas that are:
- Achievable with your actual skill level
- Genuinely suited to this person
- Meaningful because YOU made it, not just because it's homemade
- Something they'll actually use/keep/appreciate
```

---

## PROMPT 6: Edge Case - Group Gift Contribution

**Use Case**: Coordinating with others. Wants to contribute meaningfully without duplicating.

```
I'm contributing to a group gift for [GIFTEE_NAME].

THE SITUATION:
- How many people contributing: [e.g., 3 people, team of 8]
- Total budget: [e.g., group has $200, my portion is $40]
- What's already decided: [e.g., we're getting a nice backpack, we're doing an experience]
- What I could contribute: [e.g., I'm handling logistics, I can add a personal touch item]

THE PERSON:
- Key facts: [relationship, interests, needs]
- Group dynamic note: [do they know it's a group gift? surprise?]

CONTRIBUTION APPROACH:
- I want my part to: [make the main gift more special, be independently appreciated, show my specific connection to them]
- My role: [adding a touch-up item, wrapping/presenting, personalizing the main gift, contributing funds only]

Generate 2-3 contribution ideas that:
1. Complement the main gift without overshadowing it
2. Are distinct enough that your choice matters
3. Feel personal from you specifically
4. Are easy to integrate into group gift presentation
5. Respect the group dynamic
```

---

## PROMPT 7: Edge Case - No Information Available

**Use Case**: User knows almost nothing about giftee. High-stakes gifting.

```
I need to give a gift to [GIFTEE_NAME] and honestly, I don't know them very well.

THE BARE FACTS:
- Relationship: [e.g., colleague I just met, my partner's parent, new in-law]
- What I know: [any single fact - age, gender, job, one interest]
- Tone preference: [formal/casual, safe/adventurous, personal/practical]

THE STAKES:
- This matters because: [new relationship, they give to me, family expectation, etc.]
- Safe vs. bold: [do I play it safe or try to be memorable?]
- Budget: [amount]

THE CONSTRAINT:
- I need to show I'm thoughtful but I literally don't have much to work with

Generate 4-5 "safe bet" gifts that work for almost anyone and explain:
1. Why each is genuinely useful (not just generic)
2. How to present it in a way that shows thought
3. How to include a note that bridges the "we don't know each other well" gap
4. Why this beats just giving money

Then provide a strategy: What information would be most helpful to gather for next time?
```

---

## PROMPT 8: Edge Case - Expensive/Luxury Gift Ideas

**Use Case**: User has significant budget and wants quality suggestions, not just expensive.

```
I have a larger budget for [GIFTEE_NAME] and want to get something genuinely great.

THE PERSON:
- Relationship: [who they are]
- What they value most: [quality, experiences, luxury, meaning]
- One thing they're passionate about: [specific interest]
- Current life situation: [what's happening for them]
- What would genuinely improve their life: [specific pain point or desire]

MY SITUATION:
- Budget: [specific amount or range]
- I want to spend this because: [relationship significance, they deserve it, specific occasion]
- I'm not just looking for expensive, I'm looking for: [well-made, memorable, useful, luxe, unique]

CONTEXT:
- Things they've mentioned wanting: [specific items or categories]
- What they DON'T splurge on themselves: [where they're frugal]
- Items they care about quality for: [where they spend money]
- One surprise factor: [something unexpected they'd love but wouldn't buy for themselves]

Generate 4-5 higher-budget gift ideas that prove expensive doesn't mean wasteful:

For each:
1. What the gift is and what makes it worth the price
2. Why this person specifically will appreciate the quality
3. Why this is better than spending the money on multiple cheaper items
4. How it reflects your relationship/understanding of them
5. Where to source it with confidence
6. Any way to make it feel even more special/personalized

Focus on quality over quantity. Explain the "why spend this" for each.
```

---

## CONTEXT GATHERING INTERVIEW (Optional Preliminary Step)

If the user hasn't provided enough context, use this conversational prompt to gather information:

```
I'd love to help you find the perfect gift for [GIFTEE_NAME]. Let me ask a few quick questions
to make sure the ideas are actually useful:

1. RELATIONSHIP & CONTEXT
   - How do you know them? (friend, family, colleague, etc.)
   - How close are you? (very close, friendly, more formal)
   - What's one word that describes them?

2. INTERESTS & LIFESTYLE
   - What do they spend time on?
   - What's something they've mentioned wanting or needing?
   - How do they spend a perfect weekend?

3. PRACTICAL REALITY
   - What's your budget?
   - When do you need it by?
   - Can you ship or do you need it local?

4. AVOIDING MISTAKES
   - What do you know they DON'T like?
   - Have you given them gifts before? What worked?
   - Anything they've said no to?

5. THE FEELING YOU WANT
   - How do you want them to feel when they open it?
   - Are you going practical or surprising them?
   - Do they prefer experiences or objects?

Feel free to answer just the ones you know. Even partial info helps.
```

---

## IMPLEMENTATION GUIDE FOR CLAUDE API

### How to Use These Prompts in Your Application

#### 1. System Prompt (Always Include)

Set the system message to the "SYSTEM PROMPT: Gift Brainstorming Assistant" above. This establishes
consistent personality and quality standards across all gift brainstorming conversations.

#### 2. User Input Flow

```
User provides raw information about giftee
    ↓
Application formats into appropriate prompt template
    ↓
Claude API generates suggestions
    ↓
Application parses and displays results
```

#### 3. Template Selection Logic

```python
if user_scenario == "general":
    use_prompt = PROMPT_1
elif user_scenario == "budget_conscious":
    use_prompt = PROMPT_2
elif user_scenario == "experience_vs_physical":
    use_prompt = PROMPT_3
elif user_scenario == "last_minute":
    use_prompt = PROMPT_4
elif user_scenario == "diy_personalized":
    use_prompt = PROMPT_5
elif user_scenario == "group_gift":
    use_prompt = PROMPT_6
elif user_scenario == "minimal_info":
    use_prompt = PROMPT_7
elif user_scenario == "luxury_budget":
    use_prompt = PROMPT_8
```

#### 4. Prompt Formatting for API Call

Replace template variables with actual user data:

```python
def format_prompt_for_api(template, user_data):
    """
    Replace placeholder variables in template with actual user inputs

    Example:
    - [GIFTEE_NAME] → "Sarah"
    - [BUDGET] → "$25-40"
    - etc.
    """
    formatted = template
    for key, value in user_data.items():
        placeholder = f"[{key.upper()}]"
        formatted = formatted.replace(placeholder, value)
    return formatted
```

#### 5. Response Parsing

Expect Claude to return suggestions in this structured format:

```
GIFT IDEA #1: [Title]
Why It Fits: [1-2 sentences explaining the match]
Price Range: [budget]
Where to Find: [retailer/method]
Difficulty: [Easy / Moderate / Challenging]
Customization Ideas: [personalization options]
Risk Level: [Low / Medium / High - likelihood they own it already]
```

---

## QUALITY CONTROL CHECKLIST

When using these prompts, verify:

- [ ] User has provided at least one piece of specific information (not "I don't know")
- [ ] Budget is clearly stated
- [ ] Relationship type is identified
- [ ] Timeline is reasonable
- [ ] Any deal-breakers or preferences are noted
- [ ] Response includes "why it fits" reasoning for each suggestion
- [ ] Suggestions are ranked appropriately
- [ ] No generic gift card/money suggestions unless specifically requested
- [ ] Customization ideas are practical and actionable
- [ ] Difficulty assessments are accurate for typical person

---

## PROMPTS IN ACTION: Example Scenarios

### Scenario 1: Quick Brainstorm

**User Input**:
```
Friend's birthday, need ideas
Budget: $30
They love hiking and cooking
Never give them duplicates they already have
```

**Prompt Used**: PROMPT 1 (General) - simplified version

**Expected Output**: 5 ideas that match hiking + cooking interests, all under $30, with specific
"why this fits them" reasoning.

### Scenario 2: Stressed Parent at 11 PM

**User Input**:
```
My boss. Gift exchange is TOMORROW.
I don't know them well.
Budget: $25
They seem professional and practical
```

**Prompt Used**: PROMPT 4 (Last-Minute) → potentially PROMPT 7 (No Info)

**Expected Output**: Ideas available via Amazon Prime Now, local stores, or instant digital delivery,
all vetted to not embarrass in professional context.

### Scenario 3: Thoughtful Long-Term Planning

**User Input**:
```
My mom. I want to make something.
I'm good at photography and writing.
Budget doesn't matter for supplies.
10 hours available.
She values memories and practicality.
```

**Prompt Used**: PROMPT 5 (DIY/Personalized)

**Expected Output**: Ideas like photo book, handwritten letter collection, curated experiences guide,
etc., with step-by-step creation instructions.

---

## OPTIMIZATION TIPS

### For Better Results

1. **More Specific = Better Ideas**
   - Instead of: "They like reading"
   - Use: "They're obsessed with sci-fi, specifically authors like N.K. Jemisin and project teams"

2. **Context Beats Demographics**
   - Instead of: "35-year-old woman"
   - Use: "Works in tech, just had first kid, barely sleeps, loves efficiency"

3. **Avoid False Constraints**
   - Don't say "I don't know their interests" - you know something. Add any detail.

4. **Be Honest About Budget**
   - Don't artificially limit budget if you have more
   - Conversely, don't pretend you have more than you do

5. **Mention What's Already Worked**
   - If you've successfully given them gifts before, mention what worked
   - This patterns Claude toward your gifting success

### Common Mistakes to Avoid

- [ ] Not providing relationship context (friend vs. parent vs. coworker changes everything)
- [ ] Vague interests ("they like things") - be specific
- [ ] Forgetting to mention budget (Claude might suggest $200 gifts)
- [ ] Not mentioning timeline (last-minute changes everything)
- [ ] Ignoring past gifts (risking duplicates)
- [ ] Asking for generic advice instead of specific ideas

---

## RESEARCH NOTES: Why These Prompts Work

These prompts follow established prompt engineering patterns:

1. **Chain-of-Thought Structure**
   - Each prompt guides Claude through logical analysis of the person first, then suggestions
   - Forces consideration of "why it fits" before generating ideas

2. **Role Definition**
   - System prompt establishes Claude as a thoughtful advisor, not random suggester
   - Creates consistent tone and quality expectations

3. **Constraint Specification**
   - All prompts include hard constraints (budget, timeline, preferences)
   - Prevents irrelevant suggestions

4. **Output Structure Definition**
   - Each suggestion template is specified upfront
   - Claude knows exactly what format to use
   - Makes parsing and display easier for application

5. **Few-Shot Patterns** (Implicit)
   - System prompt includes quality examples in the output format description
   - Shows Claude what "good" looks like

6. **Edge Case Handling**
   - Separate prompts for unusual scenarios (no info, group gifts, luxury)
   - Prevents template from breaking under pressure

---

## FUTURE ENHANCEMENTS

These prompts can be improved with:

1. **User History Integration**
   - "Last 3 gifts you gave them: X, Y, Z - avoid suggesting similar items"
   - Requires application to track past suggestions

2. **Seasonal Variants**
   - Holiday-specific prompts with context about giving season stress
   - Birthday-specific prompts with different tone

3. **Relationship Evolution**
   - Different templates for new relationships vs. decades-long connections
   - Accounts for different gifting stakes

4. **Integration with Product Data**
   - Real-time availability checking
   - Price comparison across retailers
   - Inventory for local pickup

5. **Feedback Loop**
   - "Did you use this idea? Did they like it?" to refine future suggestions
   - Build user-specific gift-giving playbook

---

## REMEMBER

These prompts are tools for generating thoughtful ideas, not replacing human judgment.

The best gift is still the one that comes from genuine understanding of another person.

These prompts help surface that understanding and turn it into actionable suggestions.

**Your job**: Provide honest context.
**Claude's job**: Generate thoughtful, specific ideas.
**Your job again**: Make the final call based on what you know.

---

*Prompts created by Clive, Prompt Strategy Investigator*
*November 2025*
*Status: Ready for implementation*
*Quality: Investigation-grade precision*

---

## QUICK REFERENCE CHEAT SHEET

```
Scenario → Prompt to Use
─────────────────────────────────
General brainstorming → PROMPT 1
Budget-conscious → PROMPT 2
Experience vs. Physical → PROMPT 3
Last-minute (days left) → PROMPT 4
DIY/Personalized → PROMPT 5
Group gift contribution → PROMPT 6
Minimal giftee info → PROMPT 7
Higher budget ($100+) → PROMPT 8

If unsure about info level:
Run CONTEXT GATHERING INTERVIEW first
Then match to appropriate prompt
```

---

*"In the world of gift-giving, context is evidence. These prompts help you gather it."*
