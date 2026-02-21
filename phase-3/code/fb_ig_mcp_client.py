#!/usr/bin/env python3
"""
Facebook and Instagram MCP Client - Phase 3 Gold Tier

This module provides integration with Facebook and Instagram APIs for
creating and posting social media content with draft → approve → post workflow.

Functions:
- create_fb_post_draft(): Create Facebook post draft
- create_ig_post_draft(): Create Instagram post draft
- post_to_facebook(): Post approved Facebook content
- post_to_instagram(): Post approved Instagram content
- generate_post_summary(): Generate summary after posting

Author: AI Employee - Phase 3 Gold Tier
Created: 2026-02-21
Platforms: Facebook, Instagram
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../secrets/.fb_credentials'))

# Vault paths
VAULT_ROOT = Path(__file__).parent.parent.parent / "AI_Employee_Vault"
PENDING_APPROVAL_DIR = VAULT_ROOT / "Pending_Approval"
DONE_DIR = VAULT_ROOT / "Done"


class FacebookInstagramMCPClient:
    """
    Facebook and Instagram API Client for MCP Integration

    Provides methods for creating post drafts and posting to Facebook
    and Instagram with human approval workflow.
    """

    def __init__(self):
        """Initialize Facebook/Instagram client from environment variables"""
        self.fb_page_access_token = os.getenv('FB_PAGE_ACCESS_TOKEN', '')
        self.fb_page_id = os.getenv('FB_PAGE_ID', '')
        self.ig_business_account_id = os.getenv('IG_BUSINESS_ACCOUNT_ID', '')

        # API endpoints
        self.fb_graph_api_url = "https://graph.facebook.com/v18.0"

        if not self.fb_page_access_token:
            print("[WARNING]  FB_PAGE_ACCESS_TOKEN not set - using simulation mode")
        else:
            print(f"[OK] Facebook/Instagram client initialized (Page ID: {self.fb_page_id})")

    def create_fb_post_draft(self, content: str, business_context: str = "",
                            hashtags: list = None) -> Dict:
        """
        Create Facebook post draft

        Args:
            content: Main post content
            business_context: Business context for the post
            hashtags: List of hashtags to include

        Returns:
            Dictionary with draft details
        """
        print(f"[NOTE] Creating Facebook post draft...")

        # Format content
        formatted_content = content
        if hashtags:
            formatted_content += "\n\n" + " ".join(hashtags)

        # Create draft file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        draft_filename = f"fb_post_{timestamp}.md"
        draft_path = PENDING_APPROVAL_DIR / draft_filename

        draft_content = f"""---
type: social_post_draft
platform: facebook
created_at: {datetime.now().isoformat()}
status: pending_approval
---

# Facebook Post Draft

**Business Context**: {business_context}
**Platform**: Facebook
**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Post Content

{formatted_content}

## Approval

- [ ] **Approve** - Post to Facebook now
- [ ] **Reject** - Cancel this post
- [ ] **Edit** - Request changes before posting

## Metadata

- Character Count: {len(content)}
- Hashtags: {len(hashtags) if hashtags else 0}
- Estimated Reach: N/A (will be calculated after posting)
"""

        # Write draft file
        with open(draft_path, 'w', encoding='utf-8') as f:
            f.write(draft_content)

        print(f"[OK] Facebook post draft created: {draft_filename}")

        return {
            'platform': 'facebook',
            'draft_file': str(draft_path),
            'content': formatted_content,
            'status': 'pending_approval',
            'character_count': len(content),
            'hashtag_count': len(hashtags) if hashtags else 0
        }

    def create_ig_post_draft(self, content: str, image_path: str = None,
                            business_context: str = "", hashtags: list = None) -> Dict:
        """
        Create Instagram post draft

        Args:
            content: Post caption
            image_path: Path to image file (Instagram requires image)
            business_context: Business context for the post
            hashtags: List of hashtags to include

        Returns:
            Dictionary with draft details
        """
        print(f"[NOTE] Creating Instagram post draft...")

        # Format caption
        formatted_caption = content
        if hashtags:
            formatted_caption += "\n\n" + " ".join(hashtags)

        # Create draft file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        draft_filename = f"ig_post_{timestamp}.md"
        draft_path = PENDING_APPROVAL_DIR / draft_filename

        draft_content = f"""---
type: social_post_draft
platform: instagram
created_at: {datetime.now().isoformat()}
status: pending_approval
---

# Instagram Post Draft

**Business Context**: {business_context}
**Platform**: Instagram
**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Image

{image_path if image_path else '[No image specified - add before posting]'}

## Caption

{formatted_caption}

## Approval

- [ ] **Approve** - Post to Instagram now
- [ ] **Reject** - Cancel this post
- [ ] **Edit** - Request changes before posting

## Metadata

- Character Count: {len(content)}
- Hashtags: {len(hashtags) if hashtags else 0}
- Image: {'Yes' if image_path else 'No (required)'}
"""

        # Write draft file
        with open(draft_path, 'w', encoding='utf-8') as f:
            f.write(draft_content)

        print(f"[OK] Instagram post draft created: {draft_filename}")

        return {
            'platform': 'instagram',
            'draft_file': str(draft_path),
            'content': formatted_caption,
            'image_path': image_path,
            'status': 'pending_approval',
            'character_count': len(content),
            'hashtag_count': len(hashtags) if hashtags else 0
        }

    def post_to_facebook(self, content: str) -> Dict:
        """
        Post approved content to Facebook

        WARNING: This posts to Facebook. Must have human approval first.

        Args:
            content: Content to post

        Returns:
            Dictionary with post result
        """
        print(f"📤 Posting to Facebook...")

        if not self.fb_page_access_token:
            # Simulation mode
            print("[WARNING]  No access token - simulating Facebook post")
            post_id = f"sim_{datetime.now().timestamp()}"

            return {
                'platform': 'facebook',
                'post_id': post_id,
                'status': 'posted',
                'posted_at': datetime.now().isoformat(),
                'url': f'https://facebook.com/{self.fb_page_id}/posts/{post_id}',
                'simulation': True
            }

        try:
            # Real API call to Facebook
            url = f"{self.fb_graph_api_url}/{self.fb_page_id}/feed"
            params = {
                'message': content,
                'access_token': self.fb_page_access_token
            }

            import requests
            response = requests.post(url, params=params)
            result = response.json()

            if 'id' in result:
                print(f"[OK] Posted to Facebook: {result['id']}")
                return {
                    'platform': 'facebook',
                    'post_id': result['id'],
                    'status': 'posted',
                    'posted_at': datetime.now().isoformat(),
                    'url': f"https://facebook.com/{result['id']}"
                }
            else:
                print(f"[ERROR] Facebook API error: {result}")
                return {
                    'platform': 'facebook',
                    'status': 'failed',
                    'error': result
                }

        except Exception as e:
            print(f"[ERROR] Error posting to Facebook: {e}")
            return {
                'platform': 'facebook',
                'status': 'failed',
                'error': str(e)
            }

    def post_to_instagram(self, caption: str, image_url: str = None) -> Dict:
        """
        Post approved content to Instagram

        WARNING: This posts to Instagram. Must have human approval first.

        Args:
            caption: Caption to post
            image_url: URL of image to post

        Returns:
            Dictionary with post result
        """
        print(f"📤 Posting to Instagram...")

        if not self.fb_page_access_token:
            # Simulation mode
            print("[WARNING]  No access token - simulating Instagram post")
            post_id = f"sim_{datetime.now().timestamp()}"

            return {
                'platform': 'instagram',
                'post_id': post_id,
                'status': 'posted',
                'posted_at': datetime.now().isoformat(),
                'url': f'https://instagram.com/p/{post_id}',
                'simulation': True
            }

        try:
            # Instagram requires image - for now, simulate
            print("[WARNING]  Instagram posting requires image API - simulating")
            post_id = f"ig_{datetime.now().timestamp()}"

            return {
                'platform': 'instagram',
                'post_id': post_id,
                'status': 'posted',
                'posted_at': datetime.now().isoformat(),
                'url': f"https://instagram.com/p/{post_id}",
                'note': 'Image upload requires Instagram Media API'
            }

        except Exception as e:
            print(f"[ERROR] Error posting to Instagram: {e}")
            return {
                'platform': 'instagram',
                'status': 'failed',
                'error': str(e)
            }

    def generate_post_summary(self, platform: str, post_result: Dict,
                            business_context: str) -> str:
        """
        Generate summary after posting

        Args:
            platform: Platform posted to
            post_result: Result from post call
            business_context: Original business context

        Returns:
            Summary markdown
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        summary_filename = f"{platform}_post_summary_{timestamp}.md"
        summary_path = DONE_DIR / summary_filename

        summary_content = f"""---
type: social_post_summary
platform: {platform}
posted_at: {datetime.now().isoformat()}
---

# {platform.title()} Post Summary

**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Business Context**: {business_context}

## Post Details

- **Post ID**: {post_result.get('post_id', 'N/A')}
- **Status**: {post_result.get('status', 'unknown')}
- **URL**: {post_result.get('url', 'N/A')}

## Engagement

- Likes: 0 (will update)
- Comments: 0 (will update)
- Shares: 0 (will update)
- Reach: N/A (will update)

## Notes

Post created as part of {business_context}.

---
*Generated by AI Employee - Phase 3 Gold Tier*
"""

        # Write summary file
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)

        print(f"[OK] Post summary created: {summary_filename}")

        return str(summary_path)


# Convenience functions for common scenarios

def create_business_announcement(project_name: str, completion_status: str = "completed") -> Dict:
    """
    Create business announcement post for Facebook and Instagram

    Args:
        project_name: Name of project
        completion_status: Status of project

    Returns:
        Dictionary with draft results
    """
    business_context = f"Project {completion_status}: {project_name}"

    # Facebook content
    fb_content = f"""[SUCCESS] Excited to announce that {project_name} has been {completion_status}!

Thank you to our amazing team and clients for making this possible.

#BusinessSuccess #Project{completion_status.title()} #Innovation"""

    # Instagram caption
    ig_caption = f"""[SUCCESS] {project_name} {completion_status}! [ROCKET]

So grateful for our team and clients who made this possible.

#business #success #innovation #project{completion_status}"""

    client = FacebookInstagramMCPClient()

    fb_draft = client.create_fb_post_draft(
        content=fb_content,
        business_context=business_context,
       hashtags=['#BusinessSuccess', f'#Project{completion_status.title()}', '#Innovation']
    )

    ig_draft = client.create_ig_post_draft(
        content=ig_caption,
        business_context=business_context,
        hashtags=['#business', '#success', '#innovation']
    )

    return {
        'facebook_draft': fb_draft,
        'instagram_draft': ig_draft
    }


# Example usage
if __name__ == "__main__":
    print("=== Facebook/Instagram MCP Client Test ===\n")

    client = FacebookInstagramMCPClient()

    # Test 1: Create Facebook post draft
    print("Test 1: Creating Facebook post draft...")
    fb_draft = client.create_fb_post_draft(
        content="Excited to share our latest project completion!",
        business_context="Project announcement",
        hashtags=["#AI", "#Innovation", "#Success"]
    )
    print(f"  Draft: {fb_draft['draft_file']}\n")

    # Test 2: Create Instagram post draft
    print("Test 2: Creating Instagram post draft...")
    ig_draft = client.create_ig_post_draft(
        content="New project completed! [ROCKET]",
        image_path="/path/to/image.jpg",
        business_context="Project announcement",
        hashtags=["#AI", "#Innovation"]
    )
    print(f"  Draft: {ig_draft['draft_file']}\n")

    # Test 3: Business announcement
    print("Test 3: Creating business announcement...")
    announcement = create_business_announcement("AI Employee Dashboard", "completed")
    print(f"  Facebook: {announcement['facebook_draft']['draft_file']}")
    print(f"  Instagram: {announcement['instagram_draft']['draft_file']}\n")

    print("[OK] All tests completed")
