---
description: Handles external email-sending actions (send drafted emails after local approval).
---

# COMMAND: MCP Email Server

Handles external email-sending actions (send drafted emails after local approval).

## IMPLEMENTATION

```javascript
// mcp-email-server/package.json
{
  "name": "mcp-email-server",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "nodemailer": "^6.9.0",
    "dotenv": "^16.3.0"
  }
}
```

```javascript
// mcp-email-server/server.js
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

dotenv.config();

const transporter = nodemailer.createTransporter({
  host: process.env.SMTP_HOST,
  port: process.env.SMTP_PORT || 587,
  secure: false,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

const server = new Server({
  name: 'mcp-email',
  version: '1.0.0',
}, { capabilities: { tools: {} } });

server.setRequestHandler('tools/list', async () => ({
  tools: [{
    name: 'send_email',
    description: 'Send an email after local approval',
    inputSchema: {
      type: 'object',
      properties: {
        to: { type: 'string', description: 'Recipient email' },
        subject: { type: 'string', description: 'Email subject' },
        body: { type: 'string', description: 'Email body (HTML supported)' }
      },
      required: ['to', 'subject', 'body']
    }
  }]
}));

server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'send_email') {
    const { to, subject, body } = request.params.arguments;

    // Check for approval flag
    if (!request.params.arguments.approved) {
      return {
        content: [{ type: 'text', text: '⚠️ Email requires local approval. Set approved: true after review.' }]
      };
    }

    try {
      await transporter.sendMail({ from: process.env.SMTP_FROM, to, subject, html: body });
      return { content: [{ type: 'text', text: `✓ Email sent to ${to}` }] };
    } catch (error) {
      return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
    }
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error('MCP Email Server running');
```

## SETUP

```bash
npm install
echo "SMTP_HOST=smtp.gmail.com" > .env
echo "SMTP_USER=your@email.com" >> .env
echo "SMTP_PASS=your-app-password" >> .env
node server.js
```

## MCP CONFIG

```json
{
  "mcpServers": {
    "mcp-email": {
      "command": "node",
      "args": ["/path/to/mcp-email-server/server.js"],
      "env": { "SMTP_HOST": "smtp.gmail.com", "SMTP_USER": "you", "SMTP_PASS": "pass" }
    }
  }
}
```
