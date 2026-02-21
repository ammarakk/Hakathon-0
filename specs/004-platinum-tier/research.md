# Phase 0: Research & Technology Decisions

**Feature**: Phase 4 - Platinum Tier (Always-On Cloud + Local Executive)
**Date**: 2026-02-21
**Status**: Complete

---

## Research Tasks

### 1. Cloud Provider Selection

**Decision**: Oracle Cloud Always Free (primary) with Google e2-micro as backup

**Rationale**:
- Oracle Always Free provides 24/7 VM (4 ARM CPUs, 24GB RAM) - significantly better than other free tiers
- Permanent free tier (not trial) - sustainable for long-term operation
- Adequate for Odoo + watchers + orchestrator
- Alternative: Google e2-micro ($6-7/month if Oracle unavailable)

**Alternatives Considered**:
- AWS t4g.micro (12 months free only, then $8/month)
- Render background worker (free tier has cold starts, not true 24/7)
- Fly.io (credit-based, not truly free long-term)

---

### 2. Vault Sync Method

**Decision**: Git with automatic periodic pulls/pushes

**Rationale**:
- Git provides built-in conflict detection and resolution
- Native to Claude Code development workflow
- Excellent audit trail (full history)
- Easy to set up SSH keys for authentication
- Simplicity: no additional service dependencies

**Alternatives Considered**:
- Syncthing: Real-time sync but requires additional daemon, more complex setup
- rsync: No conflict resolution, higher risk of data loss
- Dropbox/Google Drive: Proprietary, less control over security

**Implementation**:
- Cloud VM: Git repository with SSH key for GitHub/GitLab
- Local machine: Same repository, same branch
- Sync interval: 30 seconds (configurable)
- Conflict handling: Stop processing, log to `/Errors/sync/`, await human resolution

---

### 3. Secrets Isolation Strategy

**Decision**: Multi-layered protection (filesystem + gitignore + environment validation)

**Rationale**:
- Defense in depth: multiple layers ensure no secrets leak
- Gitignore as first line of defense
- Pre-sync audit script scans for accidental secret inclusion
- Cloud .env only contains non-sensitive config

**Implementation Layers**:

1. **Gitignore Rules** (enforced on both cloud and local):
   ```
   .env
   .env.*
   *.session
   *.token
   *.cred
   *.credentials
   .claude/
   node_modules/.cache/
   __pycache__/
   ```

2. **Pre-Sync Audit Script**:
   - Scans staged files for secret patterns (API keys, tokens, passwords)
   - Blocks push if secrets detected
   - Logs violations to `/Errors/security/`

3. **Cloud .env Restriction**:
   - Only non-sensitive config: WATCHER_INTERVAL=30, VAULT_PATH=/path
   - MCP URLs without credentials: ODOO_URL=https://odoo.example.com
   - Actual credentials stored ONLY on local

4. **Verification Script**:
   - Run on cloud VM after setup
   - Scans filesystem for secret files
   - Produces audit report

---

### 4. Cloud Odoo Deployment

**Decision**: Odoo 16 Community on Ubuntu 22.04 with PostgreSQL 14, Nginx reverse proxy, Let's Encrypt HTTPS

**Rationale**:
- Odoo 16 is stable LTS with good Python 3.10 support
- PostgreSQL is Odoo's recommended database
- Nginx provides reverse proxy for HTTPS and static file serving
- Let's Encrypt provides free SSL certificates

**Architecture**:
```
Internet → Let's Encrypt (HTTPS) → Nginx (443) → Odoo (8069) → PostgreSQL (5432)
```

**Backup Strategy**:
- Daily pg_dump to cloud storage (Oracle Object Storage FREE)
- Retain 7 days of backups
- Backup script runs via cron at 2 AM UTC

**Health Monitoring**:
- Simple HTTP check: `curl -f https://odoo.example.com/health || fail`
- Check Odoo port: `nc -z localhost 8069`
- Check PostgreSQL: `pg_isready -U odoo`

---

### 5. Health Monitoring Architecture

**Decision**: HTTP health endpoint + external monitoring (UptimeRobot free tier)

**Rationale**:
- Simple HTTP endpoint is universally accessible
- UptimeRobot free tier: 50 monitors at 5-minute intervals
- External monitoring validates actual internet connectivity
- Local supervisor handles process restarts

**Implementation**:

1. **Health Endpoint** (`/health`):
   ```json
   {
     "status": "healthy",
     "timestamp": "2026-02-21T10:30:00Z",
     "last_activity": "2026-02-21T10:29:45Z",
     "active_watchers": ["gmail_watcher", "filesystem_watcher"],
     "error_count": 0,
     "uptime_seconds": 86400
   }
   ```

2. **Process Supervisor**:
   - systemd services for all watchers and orchestrator
   - Auto-restart on failure
   - Log to `/var/log/ai-employee/`

3. **External Monitoring**:
   - UptimeRobot pings `/health` every 5 minutes
   - Alert on 2 consecutive failures
   - Alert via email (or webhook to Slack/Discord)

---

### 6. Work-Zone Specialization Implementation

**Decision**: Configuration-based role assignment via environment variables

**Rationale**:
- Same codebase runs on both cloud and local
- Environment variable determines role (CLOUD vs LOCAL)
- Single codebase reduces maintenance burden

**Implementation**:

```bash
# Cloud .env
AGENT_ROLE=CLOUD
ALLOWED_ACTIONS=triage,draft,schedule
MCPS_ENABLED=mcp_odoo_draft

# Local .env
AGENT_ROLE=LOCAL
ALLOWED_ACTIONS=approve,send,post,whatsapp,banking
MCPS_ENABLED=mcp_email,mcp_odoo_post,mcp_social_*
```

**Action Routing**:
```python
def execute_action(action_type, params):
    if action_type in ALLOWED_ACTIONS:
        return execute(action_type, params)
    elif action_type == "send" and AGENT_ROLE == "CLOUD":
        # Cloud creates draft instead of sending
        create_draft(params)
        write_to_pending_approval(params)
    else:
        raise ActionNotAllowed(f"{action_type} not allowed for {AGENT_ROLE}")
```

---

### 7. Claim-by-Move Coordination

**Decision**: Filesystem-based atomic move operations with retry loop

**Rationale**:
- Filesystem move is atomic on POSIX systems
- Simple and reliable
- No additional coordination infrastructure needed

**Implementation Pattern**:

```python
def claim_task(task_file, agent_name):
    """Attempt to claim a task by moving it to In_Progress/<agent>/"""
    target_dir = f"In_Progress/{agent_name}/"
    os.makedirs(target_dir, exist_ok=True)

    try:
        # Atomic move
        os.rename(task_file, target_dir + os.path.basename(task_file))
        return True  # Claim successful
    except FileNotFoundError:
        return False  # Already claimed by another agent
    except Exception as e:
        log_error(f"Claim failed: {e}")
        return False
```

**Claim Verification**:
- Agent checks if file still exists in `/Needs_Action/` before processing
- If missing, another agent claimed it - skip
- Race condition window: <1ms (atomic rename)

---

### 8. A2A Messaging Upgrade (Optional)

**Decision**: Skip for MVP - file-based coordination is sufficient

**Rationale**:
- File-based vault coordination is fully functional
- A2A adds complexity without critical functionality
- Can be added later as Phase 4.1 if needed
- Spec explicitly marks A2A as P3 (optional)

**Future Consideration**:
If implementing A2A later:
- Use simple HTTP endpoint on local machine
- Cloud POSTs JSON messages to local endpoint
- Vault remains primary audit trail
- Fallback to file if A2A unavailable

---

## Technology Stack Summary

| Component | Technology | Version | Notes |
|-----------|-----------|---------|-------|
| Cloud VM | Oracle Cloud Always Free | Ubuntu 22.04 | 4 ARM CPUs, 24GB RAM |
| Runtime | Python | 3.10+ | watchers, orchestrator |
| Database | PostgreSQL | 14 | For Odoo |
| ERP | Odoo Community | 16 | Accounting integration |
| Web Server | Nginx | 1.18+ | Reverse proxy + HTTPS |
| SSL | Let's Encrypt | certbot 1.21+ | Free SSL certificates |
| Sync | Git | 2.34+ | Vault coordination |
| Process Manager | systemd | 249+ | Service supervision |
| Health Monitoring | Custom HTTP + UptimeRobot | - | External monitoring |

---

## Open Questions Resolved

**Q1: What if cloud provider limits are exceeded?**
- **A**: Monitor usage weekly. Oracle Always Free has generous limits (10TB outbound/month). If exceeded, upgrade to paid tier or switch provider.

**Q2: What if Git sync fails due to network issues?**
- **A**: Continue processing locally, queue sync operations, retry on next interval. Log failures to `/Errors/sync/`.

**Q3: What if Odoo cloud migration fails?**
- **A**: Keep local Odoo as backup. Use local Odoo until cloud is working. Document migration steps in detail.

**Q4: What if secrets accidentally sync to cloud?**
- **A**: Pre-sync audit script blocks push. If bypassed, immediately rotate credentials, remove from git history (git filter-branch), audit access logs.

**Q5: What if external monitoring (UptimeRobot) is unavailable?**
- **A**: Local health checks continue. Use alternative monitoring (Pingdom, StatusCake) or build simple custom monitor.

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Cloud VM uptime <99% | Low | High | Use reliable provider (Oracle), monitor uptime, have local fallback |
| Secrets leak to cloud | Low | Critical | Multi-layer protection, pre-sync audit, regular security scans |
| Git sync conflicts | Medium | Medium | Clear conflict resolution process, stop processing on conflict |
| Odoo migration data loss | Low | High | Full backup before migration, test migration on staging first |
| Free tier limits exhausted | Medium | Medium | Monitor usage, plan budget for upgrade ($8-20/month) |

---

## Next Steps

1. **Phase 1**: Design data models and contracts
2. **Phase 2**: Generate detailed task list
3. **Implementation**: Follow tasks.md sequentially
