"""
datamgmt.py

What this script does:
- Keeps ticket data locally for 60 days
- Moves older data to an archive location (simulated upload)
- Verifies file integrity using SHA-256 hashes
- Deletes local data only after successful verification

Why this exists:
- Prevents uncontrolled data growth
- Reduces data exposure risk
- Separates lifecycle management from the main application

This script is intended to be run manually or on a schedule
(e.g., Windows Task Scheduler or cron), not during normal app usage.
"""

import json
import shutil
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------
# Configuration
# ---------------------------

# Where active ticket data lives
BASE_OUTPUT_DIR = Path("output").resolve()

# Where archived data will be placed (dummy upload destination)
BASE_ARCHIVE_DIR = Path("archive").resolve()

# How long to keep local data
RETENTION_DAYS = 60

# Safety switch:
# When True, nothing is copied or deleted
DRY_RUN = False

# ---------------------------
# Logging & Audit Setup
# ---------------------------

LOG_DIR = Path("logs").resolve()
LOG_DIR.mkdir(exist_ok=True)

APP_LOG_FILE = LOG_DIR / "datamgmt.log"
AUDIT_LOG_FILE = LOG_DIR / "audit.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(APP_LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("datamgmt")


def write_audit_event(event_type: str, details: dict):
    """
    Append a structured audit record (JSON lines).
    This is meant to be append-only for accountability.
    """
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": event_type,
        "details": details
    }
    # Keep audit logging resilient: do not crash the job if audit write fails
    try:
        with AUDIT_LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        logger.error(f"Failed to write audit record: {e}")


# ---------------------------
# Safety & Validation Helpers
# ---------------------------

def is_safe_subpath(base: Path, target: Path) -> bool:
    """
    Ensures we never operate outside the intended base directory.

    This prevents:
    - Path traversal attempts (../../)
    - Symlink tricks
    - Accidental deletion of unrelated folders
    """
    try:
        target.resolve().relative_to(base)
        return True
    except ValueError:
        return False


def parse_folder_date(folder_name: str):
    """
    Accept only folders named like YYYY-MM-DD.
    Everything else is ignored to avoid processing unexpected directory names.
    """
    try:
        return datetime.strptime(folder_name, "%Y-%m-%d")
    except ValueError:
        return None


def sha256_file(path: Path) -> str:
    """
    Compute a SHA-256 hash for a file.
    Reads the file in chunks so large files do not consume excessive memory.
    """
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


# ---------------------------
# Manifest Creation & Verification
# ---------------------------

def build_manifest(folder: Path) -> dict:
    """
    Build a manifest describing every file in the folder.
    Stores relative path, size, and SHA-256 hash.
    """
    manifest = {
        "folder": folder.name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "files": []
    }

    for file_path in folder.rglob("*"):
        if file_path.is_file():
            manifest["files"].append({
                "path": file_path.relative_to(folder).as_posix(),
                "size_bytes": file_path.stat().st_size,
                "sha256": sha256_file(file_path)
            })

    manifest["files"].sort(key=lambda x: x["path"])
    return manifest


def write_manifest(folder: Path, manifest: dict) -> Path:
    """
    Write manifest.json into the source folder so it is archived with the data.
    """
    manifest_path = folder / "manifest.json"

    if DRY_RUN:
        logger.info(f"[DRY-RUN] Would write manifest: {manifest_path}")
        return manifest_path

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def verify_manifest(source_folder: Path, archived_folder: Path, manifest: dict) -> bool:
    """
    Verify archived copy matches the original manifest:
    - file exists
    - size matches
    - hash matches
    - archived manifest.json exists
    """
    for entry in manifest["files"]:
        rel = Path(entry["path"])
        src_file = source_folder / rel
        arc_file = archived_folder / rel

        # Sanity: source should exist (if not, something changed mid-run)
        if not src_file.exists():
            logger.error(f"[VERIFY-FAIL] Source file missing unexpectedly: {src_file}")
            return False

        if not arc_file.exists():
            logger.error(f"[VERIFY-FAIL] Missing archived file: {arc_file}")
            return False

        if arc_file.stat().st_size != entry["size_bytes"]:
            logger.error(f"[VERIFY-FAIL] Size mismatch: {arc_file}")
            return False

        if sha256_file(arc_file) != entry["sha256"]:
            logger.error(f"[VERIFY-FAIL] Hash mismatch: {arc_file}")
            return False

    if not (archived_folder / "manifest.json").exists():
        logger.error("[VERIFY-FAIL] Archived manifest.json missing.")
        return False

    return True


# ---------------------------
# Archive Destination (Simulated)
# ---------------------------

def select_archive_destination():
    """
    Ask the user where the data should be archived.
    Dummy selection for now (no real network transfers).
    """
    print("\nSelect archive destination (simulated):")
    print("1. Remote server")
    print("2. External drive")
    print("3. Cloud storage")

    destinations = {
        "1": "remote_server_archive",
        "2": "external_drive_archive",
        "3": "cloud_archive"
    }

    return destinations.get(input("Select option: ").strip())


def dummy_upload_with_verification(source_folder: Path, destination: str, manifest: dict) -> bool:
    """
    Simulate uploading by copying locally into archive/<destination>/<YYYY-MM-DD>/.
    Verify the copied data using the manifest before allowing deletion.
    """
    archived_folder = BASE_ARCHIVE_DIR / destination / source_folder.name

    if not is_safe_subpath(BASE_ARCHIVE_DIR, archived_folder):
        logger.error("[BLOCK] Unsafe archive path detected.")
        write_audit_event("archive_blocked_unsafe_path", {
            "source": str(source_folder),
            "archive_target": str(archived_folder),
            "destination": destination
        })
        return False

    logger.info(f"[UPLOAD] Copying to archive: {archived_folder}")

    if DRY_RUN:
        logger.info("[DRY-RUN] Upload and verification simulated as success.")
        write_audit_event("archive_simulated", {
            "folder": source_folder.name,
            "destination": destination,
            "archive_target": str(archived_folder)
        })
        return True

    archived_folder.parent.mkdir(parents=True, exist_ok=True)

    # Fail fast: never overwrite or merge
    if archived_folder.exists():
        logger.error(f"[ERROR] Archive folder already exists: {archived_folder}")
        write_audit_event("archive_failed_exists", {
            "folder": source_folder.name,
            "destination": destination,
            "archive_target": str(archived_folder)
        })
        return False

    # Copy
    shutil.copytree(source_folder, archived_folder)

    # Verify
    logger.info("[VERIFY] Checking archive integrity against manifest...")
    verified = verify_manifest(source_folder, archived_folder, manifest)

    if verified:
        logger.info("[VERIFY] Archive verification passed.")
        write_audit_event("archive_verified", {
            "folder": source_folder.name,
            "destination": destination,
            "archive_target": str(archived_folder),
            "file_count": len(manifest.get("files", []))
        })
        return True

    logger.error("[VERIFY] Archive verification failed.")
    write_audit_event("archive_verification_failed", {
        "folder": source_folder.name,
        "destination": destination,
        "archive_target": str(archived_folder)
    })
    return False


# ---------------------------
# Retention & Deletion Logic
# ---------------------------

def find_expired_folders():
    """
    Identify folders older than the retention window.
    Only processes date-formatted folders (YYYY-MM-DD).
    """
    expired = []
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)

    if not BASE_OUTPUT_DIR.exists():
        logger.info("[INFO] Output directory does not exist.")
        return expired

    for entry in BASE_OUTPUT_DIR.iterdir():
        if not entry.is_dir():
            continue

        folder_date = parse_folder_date(entry.name)
        if folder_date is None:
            logger.info(f"[SKIP] Ignoring unexpected folder: {entry.name}")
            continue

        if folder_date < cutoff:
            expired.append(entry)

    return sorted(expired, key=lambda p: p.name)


def delete_folder_securely(folder: Path, destination: str):
    """
    Delete a folder only after confirming it is safe.
    Write an audit record for deletion.
    """
    if not is_safe_subpath(BASE_OUTPUT_DIR, folder):
        raise RuntimeError(f"Blocked unsafe delete attempt: {folder}")

    if DRY_RUN:
        logger.info(f"[DRY-RUN] Would delete: {folder}")
        write_audit_event("local_deletion_simulated", {"folder": folder.name})
        return

    shutil.rmtree(folder)
    logger.info(f"[DELETE] Removed local folder: {folder}")
    write_audit_event("local_deleted", {
        "folder": folder.name,
        "destination": destination
    })


# ---------------------------
# Main Execution
# ---------------------------

def run_datamgmt():
    logger.info("=== Data Management Job Started ===")
    logger.info(f"Retention policy: {RETENTION_DAYS} days | Dry run: {DRY_RUN}")

    write_audit_event("job_started", {
        "retention_days": RETENTION_DAYS,
        "dry_run": DRY_RUN,
        "output_dir": str(BASE_OUTPUT_DIR),
        "archive_dir": str(BASE_ARCHIVE_DIR)
    })

    expired_folders = find_expired_folders()
    if not expired_folders:
        logger.info("No expired data found.")
        write_audit_event("job_completed_noop", {})
        return

    logger.info("Folders eligible for archival:")
    for folder in expired_folders:
        logger.info(f" - {folder.name}")

    write_audit_event("expired_folders_identified", {
        "folders": [f.name for f in expired_folders]
    })

    if input("\nProceed with archive and deletion? (yes/no): ").strip().lower() != "yes":
        logger.info("Operation cancelled by user.")
        write_audit_event("job_cancelled", {})
        return

    destination = select_archive_destination()
    if not destination:
        logger.error("Invalid destination selected.")
        write_audit_event("job_failed_invalid_destination", {})
        return

    BASE_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    for folder in expired_folders:
        logger.info(f"Processing folder: {folder.name}")
        write_audit_event("archive_attempt", {
            "folder": folder.name,
            "destination": destination
        })

        manifest = build_manifest(folder)
        write_manifest(folder, manifest)

        archived_ok = dummy_upload_with_verification(folder, destination, manifest)
        if archived_ok:
            delete_folder_securely(folder, destination)
        else:
            logger.error(f"Archive failed or could not be verified: {folder.name}")
            write_audit_event("archive_failed_kept_local", {
                "folder": folder.name,
                "destination": destination
            })

    logger.info("=== Data Management Job Completed ===")
    write_audit_event("job_completed", {})


if __name__ == "__main__":
    run_datamgmt()