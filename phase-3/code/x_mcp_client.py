#!/usr/bin/env python3
"""
Twitter/X MCP Client - Phase 3 Gold Tier

This module provides integration with Twitter/X API for
creating and posting tweets with draft -> approve -> post workflow.

Functions:
- create_tweet_draft(): Create tweet draft
- post_tweet(): Post approved tweet
- generate_thread(): Create tweet thread for longer content
- generate_tweet_summary(): Generate summary after posting

Author: AI Employee - Phase 3 Gold Tier
Created: 2026-02-21
Platform: Twitter/X
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../secrets/.x_credentials'))

# Vault paths
VAULT_ROOT = Path(__file__).parent.parent.parent / "AI_Employee_Vault"
PENDING_APPROVAL_DIR = VAULT_ROOT / "Pending_Approval"
DONE_DIR = VAULT_ROOT / "Done"


class TwitterXMCPClient:
    """
    Twitter/X API Client for MCP Integration

    Provides methods for creating tweet drafts and posting to Twitter/X
    with human approval workflow.
    """

    def __init__(self):
        """Initialize Twitter/X client from environment variables"""
        self.bearer_token = os.getenv('X_BEARER_TOKEN', '')

        # API endpoints
        self.api_url = "https://api.twitter.com/2"
        self.tweet_length_limit = 280  # Twitter/X character limit

        if not self.bearer_token:
            print("[WARNING]  X_BEARER_TOKEN not set - using simulation mode")
        else:
            print("[OK] Twitter/X client initialized")

    def create_tweet_draft(self, content: str, business_context: str = "",
                          hashtags: list = None, reply_to: str = None) -> Dict:
        """
        Create tweet draft

        Args:
            content: Tweet content
            business_context: Business context for the tweet
            hashtags: List of hashtags to include
            reply_to: Optional tweet ID to reply to

        Returns:
            Dictionary with draft details
        """
        print(f"[NOTE] Creating tweet draft...")

        # Format content with hashtags
        formatted_content = content
        if hashtags:
            hashtag_string = " ".join(hashtags)
            formatted_content += f"\n\n{hashtag_string}"

        # Check character count
        char_count = len(formatted_content)
        if char_count > self.tweet_length_limit:
            print(f"[WARNING]  Tweet exceeds {self.tweet_length_limit} characters ({char_count})")
            print(f"   Consider splitting into a thread")

        # Create draft file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        draft_filename = f"x_tweet_{timestamp}.md"
        draft_path = PENDING_APPROVAL_DIR / draft_filename

        draft_content = f"""---
type: social_post_draft
platform: twitter_x
created_at: {datetime.now().isoformat()}
status: pending_approval
---

# Twitter/X Tweet Draft

**Business Context**: {business_context}
**Platform**: Twitter/X
**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Tweet Content

{formatted_content}

## Character Count

{char_count} / {self.tweet_length_limit}

{'[WARNING] OVER LIMIT' if char_count > self.tweet_length_limit else '[OK] Within limit'}

## Reply To

{reply_to if reply_to else 'None (original tweet)'}

## Approval

- [ ] **Approve** - Post to Twitter/X now
- [ ] **Reject** - Cancel this tweet
- [ ] **Edit** - Request changes before posting

## Metadata

- Hashtags: {len(hashtags) if hashtags else 0}
- Reply: {'Yes' if reply_to else 'No'}
- Estimated Impressions: N/A
"""

        # Write draft file
        with open(draft_path, 'w', encoding='utf-8') as f:
            f.write(draft_content)

        print(f"[OK] Tweet draft created: {draft_filename}")

        return {
            'platform': 'twitter_x',
            'draft_file': str(draft_path),
            'content': formatted_content,
            'status': 'pending_approval',
            'character_count': char_count,
            'within_limit': char_count <= self.tweet_length_limit,
            'hashtag_count': len(hashtags) if hashtags else 0,
            'is_reply': bool(reply_to)
        }

    def create_thread_draft(self, content: str, business_context: str = "",
                          hashtags: list = None) -> Dict:
        """
        Create tweet thread draft for longer content

        Args:
            content: Long content to split into thread
            business_context: Business context for the thread
            hashtags: List of hashtags (added to last tweet)

        Returns:
            Dictionary with thread draft details
        """
        print(f"[NOTE] Creating tweet thread draft...")

        # Split content into tweets
        tweets = self._split_into_tweets(content)

        # Add hashtags to last tweet
        if hashtags:
            tweets[-1] += "\n\n" + " ".join(hashtags)

        # Create thread draft
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        draft_filename = f"x_thread_{timestamp}.md"
        draft_path = PENDING_APPROVAL_DIR / draft_filename

        thread_content = f"""---
type: social_post_draft
platform: twitter_x
is_thread: true
created_at: {datetime.now().isoformat()}
status: pending_approval
---

# Twitter/X Thread Draft

**Business Context**: {business_context}
**Platform**: Twitter/X (Thread)
**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Total Tweets**: {len(tweets)}

## Thread Content

"""

        for i, tweet in enumerate(tweets, 1):
            thread_content += f"### Tweet {i}/{len(tweets)} ({len(tweet)} chars)\n\n{tweet}\n\n---\n\n"

        thread_content += f"""## Approval

- [ ] **Approve** - Post thread to Twitter/X now
- [ ] **Reject** - Cancel this thread
- [ ] **Edit** - Request changes before posting

## Thread Statistics

- Total Tweets: {len(tweets)}
- Total Characters: {sum(len(t) for t in tweets)}
- Average per Tweet: {sum(len(t) for t in tweets) // len(tweets)}
- Hashtags: {len(hashtags) if hashtags else 0}
"""

        # Write thread draft file
        with open(draft_path, 'w', encoding='utf-8') as f:
            f.write(thread_content)

        print(f"[OK] Thread draft created: {draft_filename} ({len(tweets)} tweets)")

        return {
            'platform': 'twitter_x',
            'draft_file': str(draft_path),
            'is_thread': True,
            'tweet_count': len(tweets),
            'content': tweets,
            'status': 'pending_approval'
        }

    def post_tweet(self, content: str, reply_to: str = None) -> Dict:
        """
        Post approved tweet

        WARNING: This posts to Twitter/X. Must have human approval first.

        Args:
            content: Tweet content
            reply_to: Optional tweet ID to reply to

        Returns:
            Dictionary with post result
        """
        print(f"📤 Posting to Twitter/X...")

        if not self.bearer_token:
            # Simulation mode
            print("[WARNING]  No bearer token - simulating tweet")
            tweet_id = f"{int(datetime.now().timestamp())}"

            return {
                'platform': 'twitter_x',
                'tweet_id': tweet_id,
                'status': 'posted',
                'posted_at': datetime.now().isoformat(),
                'url': f'https://twitter.com/x/status/{tweet_id}',
                'character_count': len(content),
                'simulation': True
            }

        try:
            # Real API call to Twitter/X
            import requests

            headers = {
                'Authorization': f'Bearer {self.bearer_token}',
                'Content-Type': 'application/json'
            }

            payload = {'text': content}
            if reply_to:
                payload['reply'] = {'in_reply_to_tweet_id': reply_to}

            response = requests.post(
                f"{self.api_url}/tweets",
                headers=headers,
                json=payload
            )
            result = response.json()

            if 'data' in result and 'id' in result['data']:
                tweet_id = result['data']['id']
                print(f"[OK] Posted to Twitter/X: {tweet_id}")
                return {
                    'platform': 'twitter_x',
                    'tweet_id': tweet_id,
                    'status': 'posted',
                    'posted_at': datetime.now().isoformat(),
                    'url': f"https://twitter.com/x/status/{tweet_id}",
                    'character_count': len(content)
                }
            else:
                print(f"[ERROR] Twitter/X API error: {result}")
                return {
                    'platform': 'twitter_x',
                    'status': 'failed',
                    'error': result
                }

        except Exception as e:
            print(f"[ERROR] Error posting to Twitter/X: {e}")
            return {
                'platform': 'twitter_x',
                'status': 'failed',
                'error': str(e)
            }

    def _split_into_tweets(self, content: str) -> List[str]:
        """
        Split long content into multiple tweets

        Args:
            content: Content to split

        Returns:
            List of tweet strings
        """
        words = content.split()
        tweets = []
        current_tweet = ""

        for word in words:
            test_tweet = f"{current_tweet} {word}".strip()

            if len(test_tweet) <= self.tweet_length_limit - 10:  # Leave room for "1/2", etc.
                current_tweet = test_tweet
            else:
                if current_tweet:
                    tweets.append(current_tweet.strip())
                current_tweet = word

        if current_tweet:
            tweets.append(current_tweet.strip())

        # Add thread indicators
        if len(tweets) > 1:
            for i, tweet in enumerate(tweets, 1):
                tweets[i - 1] = f"{i}/{len(tweets)} " + tweet

        return tweets

    def generate_tweet_summary(self, tweet_result: Dict,
                              business_context: str) -> str:
        """
        Generate summary after posting

        Args:
            tweet_result: Result from post call
            business_context: Original business context

        Returns:
            Summary file path
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        summary_filename = f"x_tweet_summary_{timestamp}.md"
        summary_path = DONE_DIR / summary_filename

        summary_content = f"""---
type: social_post_summary
platform: twitter_x
posted_at: {datetime.now().isoformat()}
---

# Twitter/X Tweet Summary

**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Business Context**: {business_context}

## Tweet Details

- **Tweet ID**: {tweet_result.get('tweet_id', 'N/A')}
- **Status**: {tweet_result.get('status', 'unknown')}
- **URL**: {tweet_result.get('url', 'N/A')}
- **Character Count**: {tweet_result.get('character_count', 'N/A')}

## Engagement

- Likes: 0 (will update)
- Retweets: 0 (will update)
- Replies: 0 (will update)
- Impressions: N/A (will update)

## Notes

Tweet created as part of {business_context}.

---
*Generated by AI Employee - Phase 3 Gold Tier*
"""

        # Write summary file
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)

        print(f"[OK] Tweet summary created: {summary_filename}")

        return str(summary_path)


# Convenience functions for common scenarios

def create_project_announcement_tweet(project_name: str,
                                     completion_status: str = "completed") -> Dict:
    """
    Create project announcement tweet

    Args:
        project_name: Name of project
        completion_status: Status of project

    Returns:
        Dictionary with draft result
    """
    business_context = f"Project {completion_status}: {project_name}"

    content = f"""[SUCCESS] Excited to announce that {project_name} has been {completion_status}!

Thank you to our amazing team and clients! 🙏

#AI #Innovation #Success"""

    client = TwitterXMCPClient()

    tweet_draft = client.create_tweet_draft(
        content=content,
        business_context=business_context,
        hashtags=["#AI", "#Innovation", "#Success"]
    )

    return tweet_draft


# Example usage
if __name__ == "__main__":
    print("=== Twitter/X MCP Client Test ===\n")

    client = TwitterXMCPClient()

    # Test 1: Create tweet draft
    print("Test 1: Creating tweet draft...")
    tweet_draft = client.create_tweet_draft(
        content="Excited to share our latest AI project completion! [ROCKET]",
        business_context="Project announcement",
        hashtags=["#AI", "#Innovation"]
    )
    print(f"  Draft: {tweet_draft['draft_file']}")
    print(f"  Characters: {tweet_draft['character_count']}/280\n")

    # Test 2: Create thread draft
    print("Test 2: Creating thread draft...")
    long_content = """This is a long thread about our AI Employee project.

We've been working on it for months and it's finally ready!

The system can now handle cross-domain tasks, manage Odoo accounting, and post to social media autonomously.

It's a game changer for business automation. More updates coming soon!"""

    thread_draft = client.create_thread_draft(
        content=long_content,
        business_context="Long form project update",
        hashtags=["#AI", "#Automation"]
    )
    print(f"  Thread: {thread_draft['draft_file']}")
    print(f"  Tweets: {thread_draft['tweet_count']}\n")

    # Test 3: Project announcement
    print("Test 3: Creating project announcement...")
    announcement = create_project_announcement_tweet("AI Employee Dashboard", "completed")
    print(f"  Announcement: {announcement['draft_file']}\n")

    print("[OK] All tests completed")
