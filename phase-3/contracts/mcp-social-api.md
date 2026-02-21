# MCP Social Platforms API Contract

**Version**: 1.0.0
**Platforms**: LinkedIn, Facebook/Instagram, Twitter/X
**Protocol**: REST APIs via MCP servers

---

## Overview

This document defines API contracts for three social platform MCP servers:
1. **mcp-social-linkedin** (Phase 2, referenced here)
2. **mcp-social-fb-ig** (Facebook + Instagram)
3. **mcp-social-x** (Twitter/X)

All platforms follow the **draft → approve → post** pattern:
1. Claude generates post content
2. Draft saved to vault
3. Approval request created in `/Pending_Approval/`
4. Human approves with `[x] Approved`
5. MCP posts to platform
6. Result logged to `/Logs/audit-YYYY-MM-DD.md`

---

## Facebook/Instagram MCP (mcp-social-fb-ig)

### Base URLs
- Facebook Graph API: `https://graph.facebook.com/v18.0`
- Instagram Graph API: `https://graph.instagram.com`

### Authentication
- **Type**: Page Access Token (Facebook)
- **Permissions**: `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`
- **Credentials**: `phase-3/secrets/.fb_credentials`

---

### 1. create_fb_post_draft

**Description**: Create draft Facebook post (saved to vault, not posted)

**Input**:
```json
{
  "content": "string (max 63,206 characters)",
  "hashtags": ["string array (max 30)"],
  "media_urls": ["string array (optional)"]
}
```

**Output**:
```json
{
  "post_id": "uuid",
  "platform": "facebook",
  "status": "draft",
  "content": "string",
  "created_at": "ISO-8601 timestamp"
}
```

**Vault File Format**:
```markdown
---
type: social_post_draft
id: POST-2025-xyz
platform: facebook
created_at: 2026-02-20T10:30:00Z
status: draft
---

# Facebook Post Draft

**Platform**: Facebook
**Created**: 2026-02-20

## Content

Excited to announce our new project launch! 🚀

#ProjectLaunch #Innovation #Tech

## Approval

- [ ] **Approve** - Post to Facebook now
- [ ] **Reject** - Cancel this post
```

---

### 2. post_to_facebook

**Description**: Post draft to Facebook (requires approval)

**Input**:
```json
{
  "post_id": "uuid"
}
```

**Output**:
```json
{
  "post_id": "uuid",
  "platform": "facebook",
  "status": "posted",
  "post_url": "https://www.facebook.com/123456789/posts/987654321",
  "posted_at": "ISO-8601 timestamp"
}
```

**API Call** (internal):
```http
POST https://graph.facebook.com/v18.0/{page-id}/feed
Headers: Authorization: Bearer {page_access_token}
Body: message={content}
```

---

### 3. create_ig_post_draft

**Description**: Create draft Instagram post (saved to vault, not posted)

**Input**:
```json
{
  "content": "string (max 2,200 characters)",
  "hashtags": ["string array"],
  "image_url": "string (required - Instagram must have image)"
}
```

**Output**:
```json
{
  "post_id": "uuid",
  "platform": "instagram",
  "status": "draft",
  "content": "string",
  "image_url": "string",
  "created_at": "ISO-8601 timestamp"
}
```

**Note**: Instagram requires at least one image. Video not supported in Gold Tier.

---

### 4. post_to_instagram

**Description**: Post draft to Instagram (requires approval)

**Input**:
```json
{
  "post_id": "uuid"
}
```

**Output**:
```json
{
  "post_id": "uuid",
  "platform": "instagram",
  "status": "posted",
  "post_url": "https://www.instagram.com/p/ABC123/",
  "posted_at": "ISO-8601 timestamp"
}
```

**API Calls** (internal):
```http
# Step 1: Create media container
POST https://graph.instagram.com/v18.0/{ig-business-account-id}/media
Body: image_url={image_url}, caption={content}

# Step 2: Publish container
POST https://graph.instagram.com/v18.0/{ig-business-account-id}/media_publish
Body: creation_id={container_id}
```

---

### 5. generate_fb_summary

**Description**: Generate engagement summary for Facebook post

**Input**:
```json
{
  "post_url": "string"
}
```

**Output**:
```json
{
  "post_url": "string",
  "platform": "facebook",
  "likes": 42,
  "comments": 5,
  "shares": 2,
  "summary_text": "Post performing well with 42 likes and 5 comments"
}
```

**API Call** (internal):
```http
GET https://graph.facebook.com/v18.0/{post-id}/insights
Metric: likes, comments, shares
```

---

## Twitter/X MCP (mcp-social-x)

### Base URL
- Twitter API v2: `https://api.twitter.com/2`

### Authentication
- **Type**: Bearer Token (App-only)
- **Rate Limit**: 300 tweets per 15 minutes
- **Credentials**: `phase-3/secrets/.x_credentials`

---

### 1. create_x_post_draft

**Description**: Create draft tweet (saved to vault, not posted)

**Input**:
```json
{
  "content": "string (max 280 characters)"
}
```

**Output**:
```json
{
  "post_id": "uuid",
  "platform": "twitter",
  "status": "draft",
  "content": "string",
  "character_count": 280,
  "created_at": "ISO-8601 timestamp"
}
```

**Validation**: Tweet MUST be <= 280 characters. Error if longer.

---

### 2. post_to_x

**Description**: Post draft to Twitter/X (requires approval)

**Input**:
```json
{
  "post_id": "uuid"
}
```

**Output**:
```json
{
  "post_id": "uuid",
  "platform": "twitter",
  "status": "posted",
  "tweet_id": "1234567890",
  "tweet_url": "https://twitter.com/user/status/1234567890",
  "posted_at": "ISO-8601 timestamp"
}
```

**API Call** (internal):
```http
POST https://api.twitter.com/2/tweets
Headers: Authorization: Bearer {bearer_token}
Body: {"text": "{content}"}
```

---

### 3. generate_x_summary

**Description**: Generate engagement summary for tweet

**Input**:
```json
{
  "tweet_url": "string"
}
```

**Output**:
```json
{
  "tweet_url": "string",
  "platform": "twitter",
  "likes": 15,
  "retweets": 3,
  "replies": 2,
  "summary_text": "Tweet has 15 likes, 3 retweets, 2 replies"
}
```

**API Call** (internal):
```http
GET https://api.twitter.com/2/tweets/{tweet_id}/metrics
Fields: public_metrics (like_count, retweet_count, reply_count)
```

---

## LinkedIn MCP (mcp-social-linkedin)

### Reference
- Implemented in Phase 2
- API contract in `phase-2/contracts/mcp-social-linkedin-api.md`
- Same pattern: draft → approve → post

---

## Cross-Platform Post Flow

### Scenario: Completed Project

**Trigger**: ActionItem in `/Needs_Action/` with "Project completed for ABC Corp"

**Claude Processing**:
```python
# 1. Detect business context
if "project completed" in action_item.content:
    business_context = "Project completion announcement"

    # 2. Generate platform-specific posts
    posts = [
        create_linkedin_post(business_context),
        create_facebook_post(business_context),
        create_instagram_post(business_context),
        create_x_post(business_context)
    ]

    # 3. Save drafts to vault
    for post in posts:
        save_draft_to_vault(post)

    # 4. Create approval requests
    for post in posts:
        create_approval_request(post)

    # 5. Add to Plan.md
    plan.add_tasks([
        "[ ] [Business] Post to LinkedIn",
        "[ ] [Business] Post to Facebook",
        "[ ] [Business] Post to Instagram",
        "[ ] [Business] Post to Twitter/X"
    ])
```

**Platform-Specific Content**:

**LinkedIn** (professional, detailed):
```
Excited to announce the successful completion of [Project Name] with [Client Name]!

🎯 Delivered:
✅ Feature implementation
✅ Testing and validation
✅ Documentation and handoff

Looking forward to our next collaboration!

#ProjectManagement #SoftwareDevelopment #ClientSuccess
```

**Facebook** (casual, medium length):
```
🚀 Great news! We just completed another successful project with ABC Corp!

Thanks to our amazing team for delivering excellence. More updates coming soon!

#ProjectSuccess #TeamWork #Tech
```

**Instagram** (visual, concise):
```
Another project in the books! 🎉

Successfully delivered for ABC Corp. Onwards and upwards! 💪

#ProjectComplete #StartupLife #Success #TechLife
[Image: Project screenshot or team photo]
```

**Twitter/X** (short, punchy):
```
🚀 Project completed for ABC Corp! Great teamwork, smooth delivery. Next challenge awaits! 💪

#ProjectComplete #StartupLife
```

---

## Error Handling

All social MCPs return errors in this format:

```json
{
  "error": {
    "code": "ErrorCode",
    "message": "Human-readable error",
    "platform": "facebook|instagram|twitter|linkedin",
    "details": {}
  }
}
```

**Common Error Codes**:
- `AuthenticationError`: Token expired or invalid
- `RateLimitError`: Too many requests (retry after delay)
- `ContentTooLongError`: Post exceeds character limit
- `MediaRequiredError`: Instagram post missing image
- `PermissionError`: Insufficient permissions
- `PostFailedError`: Platform rejected post

**Retry Strategy**:
- `RateLimitError`: Wait for retry-after header, then retry
- `AuthenticationError`: Do NOT retry (user must regenerate token)
- `PostFailedError`: Retry up to 3 times with exponential backoff

---

## Testing

### Multi-Platform Test Script

```python
# phase-3/code/test_social_mcps.py

from mcp_social_fb_ig import FacebookMCPClient, InstagramMCPClient
from mcp_social_x import TwitterXMCPClient
import os
from dotenv import load_dotenv

load_dotenv('phase-3/secrets/.fb_credentials')
load_dotenv('phase-3/secrets/.x_credentials')

# Test Facebook
fb_client = FacebookMCPClient(
    page_access_token=os.getenv('FB_PAGE_ACCESS_TOKEN'),
    page_id=os.getenv('FB_PAGE_ID')
)

print("Testing Facebook draft...")
fb_draft = fb_client.create_post_draft(
    content="Test Facebook post from AI Employee",
    hashtags=["#Test", "#Automation"]
)
print(f"Created draft: {fb_draft['post_id']}")

# Test Instagram
ig_client = InstagramMCPClient(
    page_access_token=os.getenv('FB_PAGE_ACCESS_TOKEN'),
    business_account_id=os.getenv('IG_BUSINESS_ACCOUNT_ID')
)

print("\nTesting Instagram draft...")
ig_draft = ig_client.create_post_draft(
    content="Test Instagram post from AI Employee 🚀",
    hashtags=["#Test", "#Automation"],
    image_url="https://example.com/test-image.jpg"
)
print(f"Created draft: {ig_draft['post_id']}")

# Test Twitter/X
x_client = TwitterXMCPClient(
    bearer_token=os.getenv('X_BEARER_TOKEN')
)

print("\nTesting Twitter/X draft...")
x_draft = x_client.create_post_draft(
    content="Test tweet from AI Employee #Test #Automation"
)
print(f"Created draft: {x_draft['post_id']} (chars: {x_draft['character_count']}/280)")

print("\n✅ All social MCP tests passed!")
```

---

## Approval Workflow Integration

All social posts follow the same approval pattern:

```markdown
---
type: approval_request
action_type: social_post
platform: facebook|instagram|twitter|linkedin
created_at: 2026-02-20T10:30:00Z
priority: medium
status: pending
---

# Approval Required: Social Media Post

**Platform**: Facebook
**Created**: 2026-02-20 10:30:00
**Priority**: Medium

## Draft Content

Excited to announce our new project launch! 🚀

#ProjectLaunch #Innovation #Tech

## Approval

- [ ] **Approve** - Post to Facebook now
- [ ] **Reject** - Cancel this post

## Rejection Reason (if rejecting)

[Space for explanation]
```

**After Approval**:
1. ApprovalPoller detects `[x] Approved`
2. Calls appropriate MCP post function
3. MCP posts to platform
4. Logs to audit: `[timestamp] mcp-social-facebook - post_to_facebook - success`
5. Updates draft status to `posted`
6. Moves Plan.md task to complete

---

**Status**: ✅ Social API contracts complete
**Implementation**: Phase 3 code/social_mcp_clients.py
