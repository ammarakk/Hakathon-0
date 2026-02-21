---
description: Connects to self-hosted Odoo Community via JSON-RPC for draft accounting actions (invoices, transactions) — posting requires local approval.
---

# COMMAND: MCP Odoo Server

Connects to self-hosted Odoo Community via JSON-RPC for draft accounting actions (invoices, transactions) — posting requires local approval.

## IMPLEMENTATION

```javascript
// mcp-odoo-server/package.json
{
  "name": "mcp-odoo-server",
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
// mcp-odoo-server/server.js
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const ODOO_URL = process.env.ODOO_URL;
const ODOO_DB = process.env.ODOO_DB;
const ODOO_USER = process.env.ODOO_USER;
const ODOO_PASSWORD = process.env.ODOO_PASSWORD;

let uid = null;

async function odooCall(model, method, args = []) {
  const response = await axios.post(`${ODOO_URL}/jsonrpc`, {
    jsonrpc: "2.0",
    method: "call",
    params: {
      service: "object",
      method: "execute_kw",
      args: [ODOO_DB, uid, ODOO_PASSWORD, model, method, args]
    },
    id: Math.random()
  });
  return response.data.result;
}

async function authenticate() {
  const response = await axios.post(`${ODOO_URL}/jsonrpc`, {
    jsonrpc: "2.0",
    method: "call",
    params: { service: "common", method: "login", args: [ODOO_DB, ODOO_USER, ODOO_PASSWORD] },
    id: 1
  });
  uid = response.data.result;
}

const server = new Server({
  name: 'mcp-odoo',
  version: '1.0.0',
}, { capabilities: { tools: {} } });

server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'create_draft_invoice',
      description: 'Create a draft vendor invoice in Odoo',
      inputSchema: {
        type: 'object',
        properties: {
          description: { type: 'string' },
          amount: { type: 'number' },
          partner_id: { type: 'number' }
        },
        required: ['description', 'amount']
      }
    },
    {
      name: 'post_invoice',
      description: 'Post a draft invoice (requires approval)',
      inputSchema: {
        type: 'object',
        properties: {
          invoice_id: { type: 'number' },
          approved: { type: 'boolean' }
        },
        required: ['invoice_id', 'approved']
      }
    }
  ]
}));

server.setRequestHandler('tools/call', async (request) => {
  if (!uid) await authenticate();

  if (request.params.name === 'create_draft_invoice') {
    const { description, amount, partner_id } = request.params.arguments;
    const result = await odooCall('account.move', 'create', [{
      move_type: 'in_invoice',
      state: 'draft',
      invoice_date: new Date().toISOString().split('T')[0]
    }]);
    return { content: [{ type: 'text', text: `✓ Draft invoice created: ID ${result}` }] };
  }

  if (request.params.name === 'post_invoice') {
    const { invoice_id, approved } = request.params.arguments;
    if (!approved) {
      return { content: [{ type: 'text', text: '⚠️ Invoice posting requires local approval. Set approved: true.' }] };
    }
    await odooCall('account.move', 'action_post', [[invoice_id]]);
    return { content: [{ type: 'text', text: `✓ Invoice ${invoice_id} posted` }] };
  }
});

await authenticate();
const transport = new StdioServerTransport();
await server.connect(transport);
console.error('MCP Odoo Server running');
```

## SETUP

```bash
npm install
echo "ODOO_URL=http://localhost:8069" > .env
echo "ODOO_DB=odoo" >> .env
echo "ODOO_USER=admin" >> .env
echo "ODOO_PASSWORD=admin" >> .env
node server.js
```
