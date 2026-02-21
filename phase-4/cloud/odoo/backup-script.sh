#!/bin/bash
# Odoo Backup Script for Phase 4 - Platinum Tier
# Purpose: Automated daily backup of Odoo database with retention policy
# Schedule: Daily at 2 AM via cron
# Retention: 7 days

set -e

echo "=== Odoo Database Backup ==="
echo ""

# Configuration
ODOO_DB_NAME="odoo"
ODOO_DB_USER="odoo"
BACKUP_DIR="/backups/odoo"
RETENTION_DAYS=7
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="odoo-backup-$TIMESTAMP.sql"
LOG_FILE="/var/log/odoo-backup.log"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error_exit() {
    log "ERROR: $*"
    exit 1
}

# Check if PostgreSQL is running
if ! pg_isready -U $ODOO_DB_USER > /dev/null 2>&1; then
    error_exit "PostgreSQL is not running. Cannot proceed with backup."
fi

log "Starting Odoo database backup..."
log "Database: $ODOO_DB_NAME"
log "Backup file: $BACKUP_DIR/$BACKUP_FILE"

# Perform backup
log "Running pg_dump..."
if pg_dump -U $ODOO_DB_USER -d "$ODOO_DB_NAME" > "$BACKUP_DIR/$BACKUP_FILE" 2>/dev/null; then
    log "✓ Backup completed successfully"

    # Get backup file size
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    log "Backup size: $BACKUP_SIZE"

    # Compress backup
    log "Compressing backup..."
    gzip "$BACKUP_DIR/$BACKUP_FILE"
    COMPRESSED_FILE="${BACKUP_FILE}.gz"
    COMPRESSED_SIZE=$(du -h "$BACKUP_DIR/$COMPRESSED_FILE" | cut -f1)
    log "Compressed size: $COMPRESSED_SIZE"
else
    error_exit "Backup failed. Check PostgreSQL logs."
fi

# Clean up old backups (retention policy)
log "Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "odoo-backup-*.sql.gz" -mtime +$RETENTION_DAYS -delete > /dev/null 2>&1
DELETED_COUNT=$(find "$BACKUP_DIR" -name "odoo-backup-*.sql.gz" -mtime +$RETENTION_DAYS -print 2>/dev/null | wc -l)
log "Deleted $DELETED_COUNT old backup(s)"

# List current backups
log "Current backups:"
ls -lh "$BACKUP_DIR" | grep "odoo-backup" | tail -5 | tee -a "$LOG_FILE"

# Verify backup integrity
log "Verifying backup integrity..."
if gunzip -t "$BACKUP_DIR/$COMPRESSED_FILE" > /dev/null 2>&1; then
    log "✓ Backup integrity verified"
else
    log "⚠ WARNING: Backup integrity check failed"
fi

# Calculate total backup size
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
log "Total backup directory size: $TOTAL_SIZE"

log ""
echo "=== Backup Summary ==="
echo "Database: $ODOO_DB_NAME"
echo "Backup file: $BACKUP_DIR/$COMPRESSED_FILE"
echo "Size: $COMPRESSED_SIZE (compressed)"
echo "Retention: $RETENTION_DAYS days"
echo "Total backups: $(find $BACKUP_DIR -name "odoo-backup-*.sql.gz" | wc -l)"
echo ""
echo "Backup log: $LOG_FILE"
echo ""

# Optionally upload to cloud storage (Oracle Object Storage, S3, etc.)
# This is commented out - uncomment and configure if needed
#
# echo "Uploading to cloud storage..."
# # Example: OCI CLI
# # oci os object put --bucket-name backups --name "odoo/$BACKUP_FILE" "$BACKUP_DIR/$BACKUP_FILE.gz"
# echo "✓ Uploaded to cloud storage"

echo "✓ Odoo backup completed successfully"
echo ""