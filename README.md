# IT Triage Assistant

The IT Triage Assistant is a command-line tool designed to help collect clearer IT problem reports, assign appropriate priority based on impact, and manage ticket data in a safe and structured way.

The goal of this project is not to replace a full ticketing system, but to demonstrate how thoughtful intake, validation, and data handling can significantly improve day-to-day IT operations.

---

## Why This Project Exists

In many IT environments, tickets are vague, incomplete, or inconsistent. This leads to delays, unnecessary back-and-forth, and missed context during troubleshooting.

This project focuses on:
- Asking the *right* questions up front
- Standardizing how issues are reported
- Automatically assessing impact and priority
- Treating operational data as something that must be handled carefully, not casually

It reflects how a small internal IT tool might actually be built and maintained.

---

## What the Tool Does

### IT Triage (Interactive)
- Guides a user through reporting an issue using a CLI interface
- Validates inputs (yes/no, choices, required fields)
- Adjusts questions based on the type of issue
- Evaluates impact and assigns a priority level
- Produces a technician-ready summary
- Stores tickets in date-based folders

### Data Management (Maintenance Job)
- Keeps ticket data locally for a defined retention period
- Archives older data to a separate location (simulated upload)
- Verifies file integrity using SHA-256 hashes
- Deletes local data only after successful verification
- Writes operational and audit logs for traceability

The triage tool and the data management job are intentionally separated to mirror real operational design.

---

## Features

- Interactive command-line IT intake
- Input validation to prevent invalid or unexpected data
- Automatic impact and priority assignment
- Technician-ready ticket summaries
- Date-based storage structure
- Secure data retention and archival workflow
- Hash verification before deletion
- Append-only audit logging
- Dockerized execution for consistency and isolation

---

## Project Structure
# IT Triage Assistant

The IT Triage Assistant is a command-line tool designed to help collect clearer IT problem reports, assign appropriate priority based on impact, and manage ticket data in a safe and structured way.

The goal of this project is not to replace a full ticketing system, but to demonstrate how thoughtful intake, validation, and data handling can significantly improve day-to-day IT operations.

---

## Why This Project Exists

In many IT environments, tickets are vague, incomplete, or inconsistent. This leads to delays, unnecessary back-and-forth, and missed context during troubleshooting.

This project focuses on:
- Asking the *right* questions up front
- Standardizing how issues are reported
- Automatically assessing impact and priority
- Treating operational data as something that must be handled carefully, not casually

It reflects how a small internal IT tool might actually be built and maintained.

---

## What the Tool Does

### IT Triage (Interactive)
- Guides a user through reporting an issue using a CLI interface
- Validates inputs (yes/no, choices, required fields)
- Adjusts questions based on the type of issue
- Evaluates impact and assigns a priority level
- Produces a technician-ready summary
- Stores tickets in date-based folders

### Data Management (Maintenance Job)
- Keeps ticket data locally for a defined retention period
- Archives older data to a separate location (simulated upload)
- Verifies file integrity using SHA-256 hashes
- Deletes local data only after successful verification
- Writes operational and audit logs for traceability

The triage tool and the data management job are intentionally separated to mirror real operational design.

---

## Features

- Interactive command-line IT intake
- Input validation to prevent invalid or unexpected data
- Automatic impact and priority assignment
- Technician-ready ticket summaries
- Date-based storage structure
- Secure data retention and archival workflow
- Hash verification before deletion
- Append-only audit logging
- Dockerized execution for consistency and isolation

---

## Project Structure

# IT Triage Assistant

The IT Triage Assistant is a command-line tool designed to help collect clearer IT problem reports, assign appropriate priority based on impact, and manage ticket data in a safe and structured way.

The goal of this project is not to replace a full ticketing system, but to demonstrate how thoughtful intake, validation, and data handling can significantly improve day-to-day IT operations.

---

## Why This Project Exists

In many IT environments, tickets are vague, incomplete, or inconsistent. This leads to delays, unnecessary back-and-forth, and missed context during troubleshooting.

This project focuses on:
- Asking the *right* questions up front
- Standardizing how issues are reported
- Automatically assessing impact and priority
- Treating operational data as something that must be handled carefully, not casually

It reflects how a small internal IT tool might actually be built and maintained.

---

## What the Tool Does

### IT Triage (Interactive)
- Guides a user through reporting an issue using a CLI interface
- Validates inputs (yes/no, choices, required fields)
- Adjusts questions based on the type of issue
- Evaluates impact and assigns a priority level
- Produces a technician-ready summary
- Stores tickets in date-based folders

### Data Management (Maintenance Job)
- Keeps ticket data locally for a defined retention period
- Archives older data to a separate location (simulated upload)
- Verifies file integrity using SHA-256 hashes
- Deletes local data only after successful verification
- Writes operational and audit logs for traceability

The triage tool and the data management job are intentionally separated to mirror real operational design.

---

## Features

- Interactive command-line IT intake
- Input validation to prevent invalid or unexpected data
- Automatic impact and priority assignment
- Technician-ready ticket summaries
- Date-based storage structure
- Secure data retention and archival workflow
- Hash verification before deletion
- Append-only audit logging
- Dockerized execution for consistency and isolation

---

## Project Structure

src/ # Main IT triage application
datamgmt.py # Data retention and archival script
output/ # Runtime ticket data (ignored by git)
archive/ # Archived data (ignored by git)
logs/ # Operational and audit logs (ignored by git)
docs/ # Documentation
examples/ # Example inputs or workflows
tests/ # Test files


Folders that contain runtime data are intentionally excluded from version control.

---

## Running the Application Locally

To run the IT triage tool directly on your machine:

```bash
python src/main.py

for data deletion and archive run this
python datamgmt.py

**Run with dockers**
docker compose build
docker compose run triage
docker compose run datamgmt


