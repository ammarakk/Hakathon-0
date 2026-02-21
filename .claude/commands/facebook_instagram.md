---
description: Facebook and Instagram integration for posting messages with draft and approval workflow.
---

# COMMAND: Facebook & Instagram Integration

## CONTEXT

The user needs to integrate with Facebook and Instagram to:

- Post messages and updates
- Generate summaries for social media
- Handle drafts and approval workflows
- Integrate with watchers for automated posting

## YOUR ROLE

Act as a social media integration developer with expertise in:

- Facebook Graph API
- Instagram Basic Display API
- Content generation
- Approval workflow design

## Step 1: MCP Server for Social Media

```javascript
// social-media-mcp/package.json
{
  "name": "social-media-mcp",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "axios": "^1.6.0",
    "dotenv": "^16.3.0"
  }
}
```

```javascript
// social-media-mcp/server.js
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

// Configuration
const FACEBOOK_PAGE_ID = process.env.FACEBOOK_PAGE_ID;
const FACEBOOK_ACCESS_TOKEN = process.env.FACEBOOK_ACCESS_TOKEN;
const INSTAGRAM_BUSINESS_ID = process.env.INSTAGRAM_BUSINESS_ID;

// MCP Server
const server = new Server(
  {
    name: 'social-media-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tools List
server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'create_facebook_draft',
        description: 'Create a draft Facebook post (requires approval)',
        inputSchema: {
          type: 'object',
          properties: {
            message: {
              type: 'string',
              description: 'Post content/message',
            },
            scheduled_time: {
              type: 'string',
              description: 'ISO datetime for scheduled post (optional)',
            },
            media_urls: {
              type: 'array',
              items: { type: 'string' },
              description: 'Array of image/video URLs (optional)',
            },
          },
          required: ['message'],
        },
      },
      {
        name: 'post_to_facebook',
        description: 'Post a message to Facebook (after approval)',
        inputSchema: {
          type: 'object',
          properties: {
            message: {
              type: 'string',
              description: 'Post content/message',
            },
            link: {
              type: 'string',
              description: 'URL to share (optional)',
            },
            published: {
              type: 'boolean',
              description: 'Whether to publish immediately (default: true)',
            },
          },
          required: ['message'],
        },
      },
      {
        name: 'create_instagram_draft',
        description: 'Create a draft Instagram post (requires approval)',
        inputSchema: {
          type: 'object',
          properties: {
            caption: {
              type: 'string',
              description: 'Post caption',
            },
            image_url: {
              type: 'string',
              description: 'Image URL for the post',
            },
          },
          required: ['caption', 'image_url'],
        },
      },
      {
        name: 'generate_social_summary',
        description: 'Generate a social media summary from content',
        inputSchema: {
          type: 'object',
          properties: {
            content: {
              type: 'string',
              description: 'Content to summarize',
            },
            platform: {
              type: 'string',
              enum: ['facebook', 'instagram', 'linkedin', 'twitter'],
              description: 'Target platform',
            },
            tone: {
              type: 'string',
              enum: ['professional', 'casual', 'enthusiastic', 'urgent'],
              description: 'Tone of the post',
            },
            include_hashtags: {
              type: 'boolean',
              description: 'Include relevant hashtags',
            },
          },
          required: ['content', 'platform'],
        },
      },
    ],
  };
});

// Tool Handlers
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === 'create_facebook_draft') {
      return await createFacebookDraft(args);
    } else if (name === 'post_to_facebook') {
      return await postToFacebook(args);
    } else if (name === 'create_instagram_draft') {
      return await createInstagramDraft(args);
    } else if (name === 'generate_social_summary') {
      return await generateSocialSummary(args);
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// Facebook Functions
async function createFacebookDraft(args) {
  const { message, scheduled_time, media_urls } = args;

  // Create draft file in vault
  const draft = {
    platform: 'facebook',
    type: 'post',
    content: message,
    scheduled_time,
    media_urls,
    status: 'draft',
    created_at: new Date().toISOString(),
  };

  // In a real implementation, write to vault/Pending_Approval
  return {
    content: [
      {
        type: 'text',
        text: `✓ Facebook draft created

**Message:**
${message}

${scheduled_time ? `**Scheduled:** ${scheduled_time}` : ''}
${media_urls ? `**Media:** ${media_urls.length} attachment(s)` : ''}

The draft has been saved to Pending_Approval. Please review and approve before posting.

To post this draft, use the 'post_to_facebook' tool after approval.`,
      },
    ],
  };
}

async function postToFacebook(args) {
  const { message, link, published = true } = args;

  if (!FACEBOOK_PAGE_ID || !FACEBOOK_ACCESS_TOKEN) {
    throw new Error('Facebook credentials not configured');
  }

  try {
    const url = `https://graph.facebook.com/v19.0/${FACEBOOK_PAGE_ID}/feed`;

    const response = await axios.post(url, {
      message,
      link,
      published,
      access_token: FACEBOOK_ACCESS_TOKEN,
    });

    const postId = response.data.id;

    return {
      content: [
        {
          type: 'text',
          text: `✓ Facebook post created successfully!

**Post ID:** ${postId}
**Published:** ${published ? 'Yes' : 'No (scheduled)'}

View at: https://facebook.com/${postId}`,
        },
      ],
    };
  } catch (error) {
    throw new Error(`Facebook API error: ${error.message}`);
  }
}

// Instagram Functions
async function createInstagramDraft(args) {
  const { caption, image_url } = args;

  return {
    content: [
      {
        type: 'text',
        text: `✓ Instagram draft created

**Caption:**
${caption}

**Image:** ${image_url}

The draft has been saved to Pending_Approval. Please review and approve before posting.

Note: Instagram posts must be posted through the Instagram Mobile App or Facebook Creator Studio after approval.`,
      },
    ],
  };
}

// Content Generation
async function generateSocialSummary(args) {
  const { content, platform, tone = 'professional', include_hashtags = false } = args;

  // Platform-specific limits
  const limits = {
    facebook: { chars: 63206, hashtags: true },
    instagram: { chars: 2200, hashtags: true },
    linkedin: { chars: 3000, hashtags: false },
    twitter: { chars: 280, hashtags: true },
  };

  const limit = limits[platform];

  // Generate summary based on tone
  let summary = content.slice(0, limit.chars - 100);

  // Tone adjustments
  const tonePrefixes = {
    professional: ['📢 Update:', '🔔 Announcement:', '✨ News:'],
    casual: ['Hey! 👋', 'Check this out:', 'Just sharing:'],
    enthusiastic: ['🎉 Exciting news!', '✨ Thrilled to share:', '🚀 Big announcement:'],
    urgent: ['⚡ Urgent:', '🔴 Important:', '⏰ Time-sensitive:'],
  };

  const prefix = tonePrefixes[tone][Math.floor(Math.random() * tonePrefixes[tone].length)];
  summary = `${prefix}\n\n${summary}`;

  // Add hashtags if requested
  let hashtags = '';
  if (include_hashtags && limit.hashtags) {
    const generatedHashtags = generateHashtags(content, platform);
    hashtags = generatedHashtags;
  }

  const finalContent = include_hashtags
    ? `${summary}\n\n${hashtags}`
    : summary;

  return {
    content: [
      {
        type: 'text',
        text: `✓ Generated ${platform} post (${tone} tone)

**Character Count:** ${finalContent.length} / ${limit.chars}

**Preview:**
${finalContent}

---
${finalContent.length > limit.chars ? '⚠️ Warning: Exceeds character limit!' : '✓ Within limits'}`,
      },
    ],
  };
}

function generateHashtags(content, platform) {
  // Simple hashtag generation (can be enhanced with AI)
  const words = content.toLowerCase().split(/\s+/);
  const hashtags = new Set();

  const keywordMap = {
    business: ['#business', '#entrepreneur', '#startup'],
    tech: ['#technology', '#innovation', '#tech'],
    finance: ['#finance', '#money', '#investing'],
    marketing: ['#marketing', '#digitalmarketing', '#branding'],
  };

  for (const [key, tags] of Object.entries(keywordMap)) {
    if (words.some(w => w.includes(key))) {
      tags.forEach(t => hashtags.add(t));
    }
  }

  // Add platform-specific tags
  const platformTags = {
    instagram: ['#instagood', '#photooftheday'],
    facebook: ['#fyp', '#viral'],
    linkedin: ['#linkedingrowth', '#professional'],
    twitter: ['#trending', '#news'],
  };

  if (platformTags[platform]) {
    platformTags[platform].forEach(t => hashtags.add(t));
  }

  return Array.from(hashtags).slice(0, 10).join(' ');
}

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Social Media MCP Server running');
}

main().catch(console.error);
```

## Step 2: Environment Configuration

```bash
# .env
FACEBOOK_PAGE_ID=your_page_id
FACEBOOK_ACCESS_TOKEN=your_access_token
INSTAGRAM_BUSINESS_ID=your_instagram_business_id
```

## Step 3: Setup Instructions

### Facebook App Setup

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a new app
3. Add "Facebook Login" product
4. Get Page Access Token with `pages_manage_posts` permission

### Instagram Setup

1. Convert Instagram to Professional/Business account
2. Connect to Facebook Page
3. Get Instagram Business Account ID

### MCP Configuration

```json
// ~/.config/claude/mcp_settings.json
{
  "mcpServers": {
    "social_media": {
      "command": "node",
      "args": ["/path/to/social-media-mcp/server.js"],
      "env": {
        "FACEBOOK_PAGE_ID": "your_page_id",
        "FACEBOOK_ACCESS_TOKEN": "your_token"
      }
    }
  }
}
```

## ACCEPTANCE CRITERIA

- Creates drafts for Facebook and Instagram posts
- Generates platform-appropriate content
- Includes hashtags when requested
- Supports multiple tones
- Requires approval before posting

## FOLLOW-UPS

- Add image upload support
- Implement scheduling functionality
- Add analytics/reporting
- Support for multiple pages/accounts
