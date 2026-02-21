---
description: Twitter (X) integration for posting messages with draft and approval workflow.
---

# COMMAND: Twitter/X Integration

## CONTEXT

The user needs to integrate with Twitter (X) to:

- Post tweets and threads
- Generate content from business updates
- Handle drafts and approval workflows
- Support media uploads

## YOUR ROLE

Act as a social media integration developer with expertise in:

- Twitter API v2
- Content generation for micro-blogging
- Thread creation
- Media handling

## Step 1: MCP Server for Twitter/X

```javascript
// twitter-mcp/package.json
{
  "name": "twitter-mcp",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "twitter-api-v2": "^1.15.0",
    "dotenv": "^16.3.0"
  }
}
```

```javascript
// twitter-mcp/server.js
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { TwitterApi } from 'twitter-api-v2';
import dotenv from 'dotenv';

dotenv.config();

// Twitter client
const twitterClient = new TwitterApi({
  appKey: process.env.TWITTER_API_KEY,
  appSecret: process.env.TWITTER_API_SECRET,
  accessToken: process.env.TWITTER_ACCESS_TOKEN,
  accessSecret: process.env.TWITTER_ACCESS_SECRET,
});

const rwClient = twitterClient.readWrite;

// MCP Server
const server = new Server(
  {
    name: 'twitter-server',
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
        name: 'create_tweet_draft',
        description: 'Create a draft tweet (requires approval)',
        inputSchema: {
          type: 'object',
          properties: {
            text: {
              type: 'string',
              description: 'Tweet text (max 280 chars)',
            },
            media_urls: {
              type: 'array',
              items: { type: 'string' },
              description: 'Media URLs to attach (optional)',
            },
          },
          required: ['text'],
        },
      },
      {
        name: 'post_tweet',
        description: 'Post a tweet (after approval)',
        inputSchema: {
          type: 'object',
          properties: {
            text: {
              type: 'string',
              description: 'Tweet text',
            },
          },
          required: ['text'],
        },
      },
      {
        name: 'create_thread_draft',
        description: 'Create a draft thread (multiple tweets)',
        inputSchema: {
          type: 'object',
          properties: {
            tweets: {
              type: 'array',
              items: { type: 'string' },
              description: 'Array of tweet texts',
            },
          },
          required: ['tweets'],
        },
      },
      {
        name: 'generate_tweet_from_content',
        description: 'Generate a tweet from longer content',
        inputSchema: {
          type: 'object',
          properties: {
            content: {
              type: 'string',
              description: 'Content to summarize',
            },
            style: {
              type: 'string',
              enum: ['professional', 'casual', 'humerous', 'urgent'],
              description: 'Tweet style',
            },
            include_hashtags: {
              type: 'boolean',
              description: 'Include hashtags',
            },
          },
          required: ['content'],
        },
      },
    ],
  };
});

// Tool Handlers
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === 'create_tweet_draft') {
      return await createTweetDraft(args);
    } else if (name === 'post_tweet') {
      return await postTweet(args);
    } else if (name === 'create_thread_draft') {
      return await createThreadDraft(args);
    } else if (name === 'generate_tweet_from_content') {
      return await generateTweetFromContent(args);
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

async function createTweetDraft(args) {
  const { text, media_urls } = args;

  // Validate length
  if (text.length > 280) {
    throw new Error(`Tweet too long: ${text.length} chars (max: 280)`);
  }

  const draft = {
    platform: 'twitter',
    type: 'tweet',
    content: text,
    media_urls,
    status: 'draft',
    created_at: new Date().toISOString(),
  };

  return {
    content: [
      {
        type: 'text',
        text: `✓ Twitter draft created

**Tweet (${text.length}/280 chars):**
${text}

${media_urls ? `**Media:** ${media_urls.length} attachment(s)` : ''}

The draft has been saved to Pending_Approval. Review and use 'post_tweet' to publish.`,
      },
    ],
  };
}

async function postTweet(args) {
  const { text } = args;

  try {
    const tweet = await rwClient.v2.tweet(text);

    return {
      content: [
        {
          type: 'text',
          text: `✓ Tweet posted successfully!

**Tweet ID:** ${tweet.data.id}
**Text:** ${text}

View at: https://twitter.com/i/status/${tweet.data.id}`,
        },
      ],
    };
  } catch (error) {
    throw new Error(`Twitter API error: ${error.message}`);
  }
}

async function createThreadDraft(args) {
  const { tweets } = args;

  // Validate all tweets
  for (let i = 0; i < tweets.length; i++) {
    if (tweets[i].length > 280) {
      throw new Error(`Tweet ${i + 1} too long: ${tweets[i].length} chars`);
    }
  }

  let preview = tweets.map((t, i) => `${i + 1}/${tweets.length}: ${t}`).join('\n\n');

  return {
    content: [
      {
        type: 'text',
        text: `✓ Twitter thread draft created

**Thread: ${tweets.length} tweets**

${preview}

The draft has been saved to Pending_Approval. To post, you'll need to use the thread posting function.`,
      },
    ],
  };
}

async function generateTweetFromContent(args) {
  const { content, style = 'professional', include_hashtags = false } = args;

  // Extract key points from content
  const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const keyPoints = sentences.slice(0, 3).join('. ');

  // Style-specific prefixes
  const prefixes = {
    professional: ['📢', '🔔', '✨'],
    casual: ['Hey!', 'Check this out:', 'Just sharing:'],
    humerus: ['😄', '😎', '🤔'],
    urgent: ['⚡', '🔴', '⏰'],
  };

  const prefix = prefixes[style][Math.floor(Math.random() * 3)];

  // Generate tweet
  let tweet = `${prefix} ${keyPoints}`;

  // Truncate if too long
  if (tweet.length > 280) {
    tweet = tweet.substring(0, 277) + '...';
  }

  // Add hashtags
  if (include_hashtags) {
    const tags = generateHashtags(content);
    if ((tweet + ' ' + tags).length <= 280) {
      tweet += '\n\n' + tags;
    }
  }

  return {
    content: [
      {
        type: 'text',
        text: `✓ Generated tweet (${style} style)

**Character count:** ${tweet.length}/280

**Preview:**
${tweet}

---
Use 'create_tweet_draft' to save this for approval.`,
      },
    ],
  };
}

function generateHashtags(content) {
  const words = content.toLowerCase().split(/\s+/);
  const hashtags = new Set();

  // Common business hashtags
  const tagMap = {
    tech: ['#tech', '#technology'],
    business: ['#business', '#entrepreneur'],
    ai: ['#AI', '#MachineLearning'],
    startup: ['#startup', '#innovation'],
    finance: ['#finance', '#investing'],
  };

  for (const [key, tags] of Object.entries(tagMap)) {
    if (words.some(w => w.includes(key))) {
      tags.forEach(t => hashtags.add(t));
    }
  }

  return Array.from(hashtags).slice(0, 3).join(' ');
}

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Twitter MCP Server running');
}

main().catch(console.error);
```

## Step 2: Environment Configuration

```bash
# .env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
```

## Step 3: Setup Instructions

### Twitter Developer Setup

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new project/app
3. Get API Key, API Secret, Access Token, and Access Secret
4. Set app permissions to "Read and Write"

### MCP Configuration

```json
// ~/.config/claude/mcp_settings.json
{
  "mcpServers": {
    "twitter": {
      "command": "node",
      "args": ["/path/to/twitter-mcp/server.js"],
      "env": {
        "TWITTER_API_KEY": "your_key",
        "TWITTER_API_SECRET": "your_secret",
        "TWITTER_ACCESS_TOKEN": "your_token",
        "TWITTER_ACCESS_SECRET": "your_access_secret"
      }
    }
  }
}
```

## ACCEPTANCE CRITERIA

- Creates tweet drafts within character limit
- Posts tweets after approval
- Generates content from longer text
- Creates thread drafts
- Includes relevant hashtags

## FOLLOW-UPS

- Add media upload support
- Implement thread posting
- Add reply functionality
- Support for polls
