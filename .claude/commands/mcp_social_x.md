---
description: Manages Twitter/X post drafts, scheduling, and summary generation (final publish requires local approval).
---

# COMMAND: MCP Social X (Twitter) Server

Manages Twitter/X post drafts, scheduling, and summary generation (final publish requires local approval).

## IMPLEMENTATION

```javascript
// mcp-social-x/package.json
{
  "name": "mcp-social-x",
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
// mcp-social-x/server.js
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { TwitterApi } from 'twitter-api-v2';
import dotenv from 'dotenv';

dotenv.config();

const twitterClient = new TwitterApi({
  appKey: process.env.TWITTER_API_KEY,
  appSecret: process.env.TWITTER_API_SECRET,
  accessToken: process.env.TWITTER_ACCESS_TOKEN,
  accessSecret: process.env.TWITTER_ACCESS_SECRET,
});

const rwClient = twitterClient.readWrite;

const server = new Server({
  name: 'mcp-social-x',
  version: '1.0.0',
}, { capabilities: { tools: {} } });

server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'create_tweet_draft',
      description: 'Create a tweet draft',
      inputSchema: {
        type: 'object',
        properties: {
          text: { type: 'string', description: 'Tweet text (max 280 chars)' },
          scheduled_time: { type: 'string', description: 'ISO datetime for scheduling (optional)' }
        },
        required: ['text']
      }
    },
    {
      name: 'post_tweet',
      description: 'Post a tweet (requires approval)',
      inputSchema: {
        type: 'object',
        properties: {
          text: { type: 'string' },
          approved: { type: 'boolean' }
        },
        required: ['text', 'approved']
      }
    },
    {
      name: 'create_thread_draft',
      description: 'Create a thread draft',
      inputSchema: {
        type: 'object',
        properties: {
          tweets: { type: 'array', items: { type: 'string' } }
        },
        required: ['tweets']
      }
    },
    {
      name: 'generate_tweet_summary',
      description: 'Generate tweet from longer content',
      inputSchema: {
        type: 'object',
        properties: {
          content: { type: 'string' },
          style: { type: 'string', enum: ['professional', 'casual', 'humorous'] },
          include_hashtags: { type: 'boolean' }
        },
        required: ['content']
      }
    }
  ]
}));

server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'create_tweet_draft') {
    const { text, scheduled_time } = request.params.arguments;
    if (text.length > 280) {
      return { content: [{ type: 'text', text: `Error: Tweet exceeds 280 characters (${text.length})` }], isError: true };
    }
    return { content: [{ type: 'text', text: `✓ Tweet draft created (${text.length}/280)\n\n${text}\n\n${scheduled_time ? `Scheduled: ${scheduled_time}` : 'Ready for approval'}` }] };
  }

  if (request.params.name === 'post_tweet') {
    const { text, approved } = request.params.arguments;
    if (!approved) {
      return { content: [{ type: 'text', text: '⚠️ Tweet requires local approval. Set approved: true.' }] };
    }

    try {
      const tweet = await rwClient.v2.tweet(text);
      return { content: [{ type: 'text', text: `✓ Tweet posted: ID ${tweet.data.id}\n\nView: https://twitter.com/i/status/${tweet.data.id}` }] };
    } catch (error) {
      return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
    }
  }

  if (request.params.name === 'create_thread_draft') {
    const { tweets } = request.params.arguments;
    for (let i = 0; i < tweets.length; i++) {
      if (tweets[i].length > 280) {
        return { content: [{ type: 'text', text: `Error: Tweet ${i+1} exceeds 280 characters` }], isError: true };
      }
    }
    const preview = tweets.map((t, i) => `${i+1}/${tweets.length}: ${t}`).join('\n\n');
    return { content: [{ type: 'text', text: `✓ Thread draft created (${tweets.length} tweets)\n\n${preview}\n\nUse post_tweet for each after approval.` }] };
  }

  if (request.params.name === 'generate_tweet_summary') {
    const { content, style = 'professional', include_hashtags = false } = request.params.arguments;
    const sentences = content.split(/[.!?]+/).filter(s => s.trim());
    const summary = sentences.slice(0, 2).join('. ').slice(0, 250);
    const prefixes = { professional: '📢', casual: 'Hey!', humorous: '😄' };
    const tweet = `${prefixes[style]} ${summary}`;
    const hashtags = include_hashtags ? '\n\n#tech #business #innovation' : '';
    return { content: [{ type: 'text', text: `Generated tweet:\n\n${tweet}${hashtags}\n\nCharacters: ${tweet.length}/280` }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error('MCP Social X Server running');
```

## SETUP

```bash
npm install
echo "TWITTER_API_KEY=your_key" > .env
echo "TWITTER_API_SECRET=your_secret" >> .env
echo "TWITTER_ACCESS_TOKEN=your_token" >> .env
echo "TWITTER_ACCESS_SECRET=your_secret" >> .env
node server.js
```
