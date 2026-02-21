---
description: Handles Facebook + Instagram post drafts, scheduling, and summary generation (final publish requires local approval).
---

# COMMAND: MCP Social FB/IG Server

Handles Facebook + Instagram post drafts, scheduling, and summary generation (final publish requires local approval).

## IMPLEMENTATION

```javascript
// mcp-social-fb-ig/package.json
{
  "name": "mcp-social-fb-ig",
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
// mcp-social-fb-ig/server.js
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const FACEBOOK_PAGE_ID = process.env.FACEBOOK_PAGE_ID;
const FACEBOOK_ACCESS_TOKEN = process.env.FACEBOOK_ACCESS_TOKEN;
const INSTAGRAM_BUSINESS_ID = process.env.INSTAGRAM_BUSINESS_ID;

const server = new Server({
  name: 'mcp-social-fb-ig',
  version: '1.0.0',
}, { capabilities: { tools: {} } });

server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'create_facebook_draft',
      description: 'Create a Facebook post draft',
      inputSchema: {
        type: 'object',
        properties: {
          message: { type: 'string' },
          scheduled_time: { type: 'string' }
        },
        required: ['message']
      }
    },
    {
      name: 'post_to_facebook',
      description: 'Post to Facebook (requires approval)',
      inputSchema: {
        type: 'object',
        properties: {
          message: { type: 'string' },
          approved: { type: 'boolean' }
        },
        required: ['message', 'approved']
      }
    },
    {
      name: 'create_instagram_draft',
      description: 'Create an Instagram post draft',
      inputSchema: {
        type: 'object',
        properties: {
          caption: { type: 'string' },
          image_url: { type: 'string' }
        },
        required: ['caption', 'image_url']
      }
    },
    {
      name: 'generate_social_summary',
      description: 'Generate social media summary from content',
      inputSchema: {
        type: 'object',
        properties: {
          content: { type: 'string' },
          platform: { type: 'string', enum: ['facebook', 'instagram'] },
          tone: { type: 'string', enum: ['professional', 'casual', 'enthusiastic'] }
        },
        required: ['content', 'platform']
      }
    }
  ]
}));

server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'create_facebook_draft') {
    const { message, scheduled_time } = request.params.arguments;
    return { content: [{ type: 'text', text: `✓ Facebook draft created\n\n${message}\n\n${scheduled_time ? `Scheduled: ${scheduled_time}` : 'Ready for approval'}` }] };
  }

  if (request.params.name === 'post_to_facebook') {
    const { message, approved } = request.params.arguments;
    if (!approved) {
      return { content: [{ type: 'text', text: '⚠️ Facebook post requires local approval. Set approved: true.' }] };
    }

    try {
      const response = await axios.post(`https://graph.facebook.com/v19.0/${FACEBOOK_PAGE_ID}/feed`,
        { message, access_token: FACEBOOK_ACCESS_TOKEN }
      );
      return { content: [{ type: 'text', text: `✓ Facebook post published: ID ${response.data.id}` }] };
    } catch (error) {
      return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
    }
  }

  if (request.params.name === 'create_instagram_draft') {
    const { caption, image_url } = request.params.arguments;
    return { content: [{ type: 'text', text: `✓ Instagram draft created\n\nCaption: ${caption}\nImage: ${image_url}\n\n⚠️ Instagram posts must be published via Mobile App or Creator Studio after approval.` }] };
  }

  if (request.params.name === 'generate_social_summary') {
    const { content, platform, tone = 'professional' } = request.params.arguments;
    const limit = platform === 'instagram' ? 2200 : 63206;
    const summary = content.slice(0, limit);
    const tonePrefix = { professional: '📢', casual: 'Hey!', enthusiastic: '✨' }[tone];
    return { content: [{ type: 'text', text: `Generated ${platform} content:\n\n${tonePrefix} ${summary}\n\nCharacters: ${summary.length}/${limit}` }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error('MCP Social FB/IG Server running');
```

## SETUP

```bash
npm install
echo "FACEBOOK_PAGE_ID=your_page_id" > .env
echo "FACEBOOK_ACCESS_TOKEN=your_token" >> .env
echo "INSTAGRAM_BUSINESS_ID=your_ig_id" >> .env
node server.js
```
