---
description: LinkedIn business posting automation for sales generation.
---

# COMMAND: LinkedIn Business Posting

## CONTEXT

The user needs to automatically post on LinkedIn about business to:

- Generate sales leads
- Share business updates
- Post industry insights
- Schedule content strategically

## YOUR ROLE

Act as a LinkedIn automation developer with expertise in:

- LinkedIn Marketing API
- B2B content strategy
- Lead generation tactics
- Professional networking

## Step 1: LinkedIn Content Generator

```python
#!/usr/bin/env python3
"""
LinkedIn Business Posting Agent

Generates and posts professional content on LinkedIn
to drive engagement and generate sales leads.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("linkedin_posting")


class LinkedInContentGenerator:
    """Generate business-focused LinkedIn content."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.drafts_dir = vault_path / "Pending_Approval"
        self.drafts_dir.mkdir(parents=True, exist_ok=True)

        # Content templates
        self.templates = {
            'announcement': self._announcement_template,
            'insight': self._insight_template,
            'case_study': self._case_study_template,
            'promotional': self._promotional_template,
            'behind_scenes': self._behind_scenes_template,
        }

    def _announcement_template(self, data: Dict) -> str:
        """Generate announcement post."""
        return f"""🚀 Exciting News!

We're thrilled to announce that {data['announcement']}!

This is a huge milestone for us and we couldn't have done it without the support of our amazing team and clients.

{data.get('details', '')}

What does this mean for you? {data.get('benefit', 'Better service and innovative solutions')}

We'd love to hear your thoughts! Drop a comment below.

#innovation #business #growth #{data.get('industry', 'technology')}"""

    def _insight_template(self, data: Dict) -> str:
        """Generate industry insight post."""
        return f"""💡 {data['hook']}

Here's something I've learned from {data.get('years', 10)+} years in {data.get('industry', 'business')}:

{data['insight']}

The key takeaway? {data['takeaway']}

This approach has helped us:
✅ {data.get('result1', 'Increase efficiency by 40%')}
✅ {data.get('result2', 'Improve customer satisfaction')}
✅ {data.get('result3', 'Drive revenue growth')}

What's your experience with this? Share in the comments!

#leadership #insights #professionaldevelopment #"""

    def _case_study_template(self, data: Dict) -> str:
        """Generate case study post."""
        return f"""📊 Case Study: How We Helped {data['client']} Achieve {data['result']}

The Challenge:
{data['challenge']}

The Solution:
{data['solution']}

The Results:
🎯 {data.get('metric1', '50% increase in leads')}
🎯 {data.get('metric2', '30% reduction in costs')}
🎯 {data.get('metric3', '2x ROI in 3 months')}

Here's what {data['client']} had to say:
"{data.get('quote', 'This partnership transformed our business.')}"

Want similar results? Let's talk!

#casestudy #success #businessgrowth #results"""

    def _promotional_template(self, data: Dict) -> str:
        """Generate promotional post."""
        return f"""✨ Transform Your {data.get('area', 'Business')} Today!

Are you struggling with {data['problem']}?

You're not alone. {data.get('stat', '70% of businesses face this challenge')}

Our solution helps you:
✔️ {data.get('benefit1', 'Save time')}
✔️ {data.get('benefit2', 'Reduce costs')}
✔️ {data.get('benefit3', 'Increase revenue')}

Special offer: {data.get('offer', 'Free consultation for first 10 connections')}

DM us or comment "INTERESTED" to learn more!

#business #solution #entrepreneur #"""

    def _behind_scenes_template(self, data: Dict) -> str:
        """Generate behind-the-scenes post."""
        return f"""🔥 Behind the Scenes at {data.get('company', 'Our Company')}

{data['story']}

{data.get('team_detail', 'Our team worked tirelessly to make this happen.')}

Some highlights:
• {data.get('highlight1', 'Late nights and big ideas')}
• {data.get('highlight2', 'Collaboration across departments')}
• {data.get('highlight3', 'Celebrating small wins')}

The result? {data['outcome']}

Big shoutout to our amazing team! {data.get('team_tags', '')}

#teamwork #culture #behindthescenes #"""

    def generate_content(self, content_type: str, data: Dict) -> str:
        """Generate content based on type and data."""
        template = self.templates.get(content_type, self._announcement_template)
        return template(data)

    def create_draft(self, content: str, scheduled_time: str = None) -> Path:
        """Create a draft post for approval."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_linkedin_draft.md"
        filepath = self.drafts_dir / filename

        draft_content = f"""# LinkedIn Post Draft

**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Status:** Pending Approval
{f'**Scheduled:** {scheduled_time}' if scheduled_time else ''}

## Post Content

{content}

## Approval Checklist
- [ ] Review content for accuracy
- [ ] Check grammar and spelling
- [ ] Verify hashtags are relevant
- [ ] Confirm no sensitive information
- [ ] Add any media (images/documents)

## Actions Required
- **To Approve:** Change status to "Approved"
- **To Edit:** Make changes directly in this file
- **To Post:** Use LinkedIn posting tool after approval

---
*Generated by LinkedInPostingAgent*
"""

        filepath.write_text(draft_content)
        logger.info(f"Created LinkedIn draft: {filepath}")
        return filepath


class LinkedInPostingScheduler:
    """Schedule and manage LinkedIn posts."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.content_generator = LinkedInContentGenerator(vault_path)
        self.schedule_file = vault_path / "Updates" / "linkedin_schedule.md"

    def create_weekly_schedule(self, topics: List[Dict]) -> Path:
        """Create a weekly posting schedule."""
        schedule_content = f"""# LinkedIn Weekly Schedule

**Week of:** {datetime.now().strftime("%Y-%m-%d")}

## Posting Schedule

### Monday - Industry Insight
**Topic:** {topics[0].get('topic', 'Market trends')}
**Time:** 9:00 AM
**Draft:** `{topics[0].get('draft_file', 'pending')}`

### Wednesday - Case Study
**Topic:** {topics[1].get('topic', 'Client success')}
**Time:** 12:00 PM
**Draft:** `{topics[1].get('draft_file', 'pending')}`

### Friday - Behind the Scenes
**Topic:** {topics[2].get('topic', 'Team culture')}
**Time:** 3:00 PM
**Draft:** `{topics[2].get('draft_file', 'pending')}`

## Best Practices
- Post when your audience is most active
- Engage with comments within 1 hour
- Share authentic, value-driven content
- Use 3-5 relevant hashtags
- Include media when possible

## Performance Tracking
Track engagement metrics:
- Likes
- Comments
- Shares
- Profile views
- Connection requests

---
*Generated by LinkedInPostingAgent*
"""

        self.schedule_file.parent.mkdir(parents=True, exist_ok=True)
        self.schedule_file.write_text(schedule_content)
        return self.schedule_file


# Content Ideas Generator

def generate_content_ideas(industry: str, company_type: str) -> List[Dict]:
    """Generate weekly content ideas based on industry and company type."""
    ideas = []

    # Industry-specific ideas
    industry_ideas = {
        'technology': [
            {'type': 'insight', 'topic': 'AI in business', 'hook': 'Is AI replacing or enhancing jobs?'},
            {'type': 'case_study', 'topic': 'Digital transformation', 'client': 'TechCorp Inc.'},
            {'type': 'announcement', 'topic': 'New feature launch', 'announcement': 'We are launching AI assistant'},
        ],
        'consulting': [
            {'type': 'insight', 'topic': 'Process optimization', 'hook': 'The #1 mistake businesses make'},
            {'type': 'case_study', 'topic': 'Client success story', 'client': 'Services Co.'},
            {'type': 'behind_scenes', 'topic': 'Consulting methodology', 'story': 'How we solve complex problems'},
        ],
        'finance': [
            {'type': 'insight', 'topic': 'Investment strategies', 'hook': 'Market outlook for Q2'},
            {'type': 'promotional', 'topic': 'Financial planning', 'problem': 'Managing cash flow'},
            {'type': 'announcement', 'topic': 'New service offering', 'announcement': 'We now offer wealth management'},
        ],
    }

    base_ideas = industry_ideas.get(industry, industry_ideas['technology'])

    for idea in base_ideas:
        ideas.append({
            'content_type': idea['type'],
            'topic': idea['topic'],
            'data': idea,
        })

    return ideas


# Example Usage

async def main():
    """Example: Generate weekly LinkedIn content."""
    vault_path = Path("./vault")
    scheduler = LinkedInPostingScheduler(vault_path)

    # Generate content ideas
    ideas = generate_content_ideas('technology', 'SaaS')

    # Create drafts
    for idea in ideas[:3]:
        content = scheduler.content_generator.generate_content(
            idea['content_type'],
            idea['data']
        )
        draft_path = scheduler.content_generator.create_draft(content)
        idea['draft_file'] = draft_path.name

    # Create schedule
    schedule_path = scheduler.create_weekly_schedule(ideas)

    print(f"✓ Generated {len(ideas)} LinkedIn drafts")
    print(f"✓ Created weekly schedule: {schedule_path}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Step 2: LinkedIn API Integration (Optional)

For automated posting via LinkedIn API:

```python
# linkedin_api.py
import requests
import os

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_PERSON_ID = os.getenv("LINKEDIN_PERSON_ID")  # URN ID

def post_to_linkedin(content: str) -> dict:
    """Post content to LinkedIn."""
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "author": LINKEDIN_PERSON_ID,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
```

## ACCEPTANCE CRITERIA

- Generates professional business content
- Creates drafts for approval
- Schedules posts strategically
- Supports multiple content types
- Includes relevant hashtags

## FOLLOW-UPS

- Add A/B testing for content
- Implement analytics tracking
- Create content calendar
- Add engagement monitoring
