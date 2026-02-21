#!/usr/bin/env python3
"""
Health Endpoint Server for Phase 4 - Platinum Tier
Purpose: HTTP endpoint for monitoring cloud agent health
Port: 8080
Rate Limit: 1 request per second
"""

from flask import Flask, jsonify
from datetime import datetime, timedelta
import os
import time
import psutil
import threading

app = Flask(__name__)

# Global state
last_activity = datetime.now()
start_time = datetime.now()
error_count = 0
active_watchers = []
rate_limit_tracker = {}

# Configuration from environment
AGENT_ROLE = os.getenv('AGENT_ROLE', 'local')
VAULT_PATH = os.getenv('VAULT_PATH', os.path.expanduser('~/AI_Employee_Vault'))
HEALTH_PORT = int(os.getenv('HEALTH_PORT', 8080))
HEALTH_RATE_LIMIT = int(os.getenv('HEALTH_RATE_LIMIT', 1))

def update_last_activity():
    """Update last activity timestamp"""
    global last_activity
    last_activity = datetime.now()

def get_uptime_seconds():
    """Calculate agent uptime in seconds"""
    return int((datetime.now() - start_time).total_seconds())

def get_active_watchers():
    """Get list of active watcher processes"""
    watchers = []

    # Check for common watcher process names
    watcher_names = ['gmail_watcher', 'filesystem_watcher', 'whatsapp_watcher',
                    'finance_watcher', 'orchestrator']

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            proc_name = proc.info['name']
            cmdline = ' '.join(proc.info['cmdline'] or [])

            for watcher in watcher_names:
                if watcher in cmdline.lower():
                    watchers.append(watcher)
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return list(set(watchers))

def check_rate_limit(client_ip):
    """
    Check if client has exceeded rate limit
    Returns: (allowed, retry_after_seconds)
    """
    now = time.time()

    # Clean old entries
    cutoff = now - HEALTH_RATE_LIMIT
    rate_limit_tracker = {k: v for k, v in rate_limit_tracker.items() if v > cutoff}

    if client_ip in rate_limit_tracker:
        last_request = rate_limit_tracker[client_ip]
        if now - last_request < HEALTH_RATE_LIMIT:
            retry_after = int(HEALTH_RATE_LIMIT - (now - last_request)) + 1
            return False, retry_after

    rate_limit_tracker[client_ip] = now
    return True, 0

def get_system_status():
    """Get overall system health status"""
    try:
        # Check if we can access vault
        vault_accessible = os.path.exists(VAULT_PATH)

        # Check error rate
        error_rate = error_count / max(get_uptime_seconds() / 3600, 1)  # errors per hour

        # Determine status
        if not vault_accessible:
            return "error"
        elif error_rate > 10:
            return "degraded"
        else:
            return "healthy"
    except Exception as e:
        return "error"

@app.route('/health')
def health():
    """
    Health check endpoint
    Returns: JSON status with agent health information
    Rate limited: 1 request per second
    """
    client_ip = str(request.remote_addr)

    # Check rate limit
    allowed, retry_after = check_rate_limit(client_ip)
    if not allowed:
        response = jsonify({
            "status": "rate_limited",
            "retry_after": retry_after
        })
        response.status_code = 429
        return response

    # Update activity
    update_last_activity()

    # Get system status
    status = get_system_status()
    watchers = get_active_watchers()

    # Build response
    response_data = {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "last_activity": last_activity.isoformat(),
        "active_watchers": watchers,
        "error_count": error_count,
        "uptime_seconds": get_uptime_seconds(),
        "agent_role": AGENT_ROLE,
        "vault_path": VAULT_PATH
    }

    # Add status code based on health
    if status == "healthy":
        response = jsonify(response_data)
    elif status == "degraded":
        response = jsonify(response_data)
        response.status_code = 503  # Service Unavailable
    else:  # error
        response = jsonify(response_data)
        response.status_code = 503

    return response

@app.route('/health/watchers')
def health_watchers():
    """Detailed watcher status endpoint"""
    watchers = get_active_watchers()

    # Get detailed process info for each watcher
    watcher_details = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time', 'status']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])

            for watcher in watchers:
                if watcher in cmdline.lower():
                    watcher_details.append({
                        "name": watcher,
                        "pid": proc.info['pid'],
                        "status": proc.info['status'],
                        "uptime_seconds": int(time.time() - proc.info['create_time'])
                    })
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return jsonify({
        "watchers": watcher_details,
        "count": len(watcher_details)
    })

@app.route('/health/vault')
def health_vault():
    """Vault status endpoint"""
    vault_stats = {
        "vault_path": VAULT_PATH,
        "accessible": os.path.exists(VAULT_PATH),
        "needs_action_count": 0,
        "in_progress_count": 0,
        "pending_approval_count": 0,
        "done_count": 0
    }

    if vault_stats["accessible"]:
        # Count files in each folder
        import os

        for root, dirs, files in os.walk(VAULT_PATH):
            if '/Needs_Action/' in root:
                vault_stats["needs_action_count"] += len([f for f in files if f.endswith('.md')])
            elif '/In_Progress/' in root:
                vault_stats["in_progress_count"] += len([f for f in files if f.endswith('.md')])
            elif '/Pending_Approval/' in root:
                vault_stats["pending_approval_count"] += len([f for f in files if f.endswith('.md')])
            elif '/Done/' in root:
                vault_stats["done_count"] += len([f for f in files if f.endswith('.md')])

    return jsonify(vault_stats)

def increment_error_count():
    """Increment error counter (called by other modules)"""
    global error_count
    error_count += 1

# Make error counter accessible
app.increment_error_count = increment_error_count

if __name__ == '__main__':
    print(f"Starting Health Server for {AGENT_ROLE} agent...")
    print(f"Port: {HEALTH_PORT}")
    print(f"Rate Limit: {HEALTH_RATE_LIMIT} req/sec")
    print(f"Vault Path: {VAULT_PATH}")
    print("")
    print("Endpoints:")
    print("  GET /health              - Basic health check")
    print("  GET /health/watchers     - Detailed watcher status")
    print("  GET /health/vault        - Vault file counts")
    print("")

    # Run Flask app
    app.run(host='0.0.0.0', port=HEALTH_PORT, threaded=True)