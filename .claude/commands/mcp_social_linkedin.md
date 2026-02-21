---
description: Manages LinkedIn post drafts and scheduling (content generation from business context, final send requires approval).
---

# COMMAND: MCP Social LinkedIn Server

Manages LinkedIn post drafts and scheduling (content generation from business context, final send requires approval).

## IMPLEMENTATION

```javascript
// mcp-social-linkedin/package.json
{
  "name": "mcp-social-linkedin",
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
// mcp-social-linkedin/server.js
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const LINKEDIN_ACCESS_TOKEN = process.env.LINKEDIN_ACCESS_TOKEN;
const LINKEDIN_PERSON_ID = process.env.LINKEDIN_PERSON_ID;

const server = new Server({
  name: 'mcp-social-linkedin',
  version: '1.0.0',
}, { capabilities: { tools: {} } });

server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'create_linkedin_draft',
      description: 'Create a LinkedIn post draft',
      inputSchema: {
        type: 'object',
        properties: {
          content: { type: 'string', description: 'Post content (max 3000 chars)' },
          scheduled_time: { type: 'string', description: 'ISO datetime for scheduling (optional)' }
        },
        required: ['content']
      }
    },
    {
      name: 'post_to_linkedin',
      description: 'Post to LinkedIn (requires approval)',
      inputSchema: {
        type: 'object',
        properties: {
          content: { type: 'string' },
          approved: { type: 'boolean' }
        },
        required: ['content', 'approved']
      }
    },
    {
      name: 'generate_linkedin_content',
      description: 'Generate LinkedIn content from business context',
      inputSchema: {
        type: 'object',
        properties: {
          topic: { type: 'string' },
          tone: { type: 'string', enum: ['professional', 'casual', 'enthusiastic'] },
          include_hashtags: { type: 'boolean' }
        },
        required: ['topic']
      }
    }
  ]
}));

server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'create_linkedin_draft') {
    const { content, scheduled_time } = request.params.arguments;
    if (content.length > 3000) {
      return { content: [{ type: 'text', text: `Error: Content exceeds 3000 characters (${content.length})` }], isError: true };
    }
    return { content: [{ type: 'text', text: `✓ LinkedIn draft created\n\n${content}\n\n${scheduled_time ? `Scheduled: ${scheduled_time}` : 'Ready for approval'}` }] };
  }

  if (request.params.name === 'post_to_linkedin') {
    const { content, approved } = request.params.arguments;
    if (!approved) {
      return { content: [{ type: 'text', text: '⚠️ LinkedIn post requires local approval. Set approved: true.' }] };
    }

    try {
      const response = await axios.post('https://api.linkedin.com/v2/ugcPosts', {
        author: LINKEDIN_PERSON_ID,
        lifecycleState: "PUBLISHED",
        specificContent: {
          "com.linkedin.ugc.ShareContent": {
            shareCommentary: { text: content },
            shareMediaCategory: "NONE"
          }
        },
        visibility: { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" }
      }, { headers: { 'Authorization': `Bearer ${LINKEDIN_ACCESS_TOKEN}`, 'Content-Type': 'application/json' } });

      return { content: [{ type: 'text', text: `✓ LinkedIn post published: ID ${response.data.id}` }] };
    } catch (error) {
      return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
    }
  }

  if (request.params.name === 'generate_linkedin_content') {
    const { topic, tone = 'professional', include_hashtags = true } = request.params.arguments;
    const prefixes = { professional: '📢', casual: 'Hey!', enthusiastic: '🚀' };
    const hashtags = include_hashtags ? '\n\n#business #entrepreneur #innovation' : '';
    const content = `${prefixes[tone]} ${topic}${hashtags}`;
    return { content: [{ type: 'text', text: `Generated content:\n\n${content}` }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error('MCP Social LinkedIn Server running');
```

## SETUP

```bash
npm install
echo "LINKEDIN_ACCESS_TOKEN=your_token" > .env
echo "LINKEDIN_PERSON_ID=urn:li:person:xxx" >> .env
node server.js
```
