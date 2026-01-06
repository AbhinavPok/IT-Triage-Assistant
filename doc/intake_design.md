# IT Triage Assistant – Intake Design

## Purpose and Background
In many IT environments, delays in issue resolution are caused not by technical complexity, but by incomplete or unclear problem reporting. End users often submit tickets with vague descriptions such as “my computer isn’t working,” which forces technicians to spend time gathering basic information instead of diagnosing and resolving the issue.

The IT Triage Assistant is designed to address this problem by guiding users through a structured intake process. By asking targeted, category-specific questions, the tool ensures that each ticket contains the minimum information required for effective troubleshooting from the outset.

## Intended Users
This tool is designed to support two primary audiences:

- **End Users:** Non-technical users who need clear guidance to describe their issues accurately without requiring IT knowledge.
- **Technicians / Analysts:** IT support and security personnel who rely on consistent, actionable information to diagnose issues efficiently and prioritize work appropriately.

## Definition of Success
A triage submission is considered successful when a technician can begin troubleshooting immediately, without needing to request additional clarification from the user. The output should clearly communicate what is happening, who is affected, when it started, and how severely work is impacted.

## Intake Flow Overview
The IT Triage Assistant follows a simple, repeatable flow to ensure consistency:

1. The user launches the tool and is informed of its purpose.
2. The user selects the issue category that best matches their problem.
3. The tool presents a focused set of questions relevant to that category only.
4. User responses are evaluated using predefined, rule-based logic.
5. The system determines the issue’s impact and priority level.
6. A technician-ready summary is generated for use in an IT ticketing system.

This flow mirrors common enterprise help desk and incident management practices.

## Supported Issue Categories (Minimum Viable Product)
The initial release of the IT Triage Assistant supports the following issue categories, which collectively represent the majority of common help desk requests:

1. Login or Account Access
2. Network or Wi-Fi Connectivity
3. Email or Phishing Concerns
4. Slow Computer or Performance Issues
5. Software Errors or Installation Problems

Additional categories may be added in future iterations as needed.

## Intake Questions by Category

### Login or Account Access
These questions are intended to identify authentication failures, account lockouts, expired credentials, or system-specific login problems.

- Operating system in use (Windows or macOS)
- Exact error message displayed, if any
- When the issue was first observed
- Whether the user recently changed their password (yes/no)
- Whether other users are experiencing the same issue (yes/no)

This information helps technicians distinguish between individual account issues and broader authentication or directory-related problems.

### Network or Wi-Fi Connectivity
These questions help determine whether the issue is isolated to the user’s device or indicative of a wider network or service outage.

- Whether the device is currently connected to Wi-Fi (yes/no)
- Whether any websites or online services are accessible (yes/no)
- Whether other users are affected (yes/no)
- Whether the user is working on-site or remotely
- When the issue began

The responses guide initial troubleshooting steps such as checking local connectivity, DNS resolution, or upstream network availability.

### Email or Phishing Concerns
These questions are designed to assess whether the situation represents a security incident or a general inquiry that can be resolved through user education.

- Sender’s email address
- Email subject line
- Whether a link in the email was clicked (yes/no)
- Whether an attachment was opened (yes/no)
- Approximate time the email was received

If a link was clicked or an attachment opened, the issue may require immediate escalation to security personnel.

### Slow Computer or Performance Issues
These questions help identify performance degradation caused by system resource constraints, recent changes, or potential malicious activity.

- Device type (laptop or desktop)
- When the performance issue began
- Whether the slowness is constant or intermittent
- Whether any recent software installations or system updates occurred (yes/no)
- Whether pop-ups, freezes, or other unusual behavior are present (yes/no)

This information allows technicians to prioritize investigations related to hardware limitations, software conflicts, or malware indicators.

### Software Errors or Installation Problems
These questions focus on understanding the scope and urgency of application-related issues.

- Name of the affected application
- Exact error message displayed
- When the issue began
- Whether restarting the system resolved or improved the issue (yes/no)
- Whether the issue is preventing the user from completing required work (yes/no)

This helps technicians determine whether the issue is a known application problem, a configuration issue, or a user-specific fault.

## Impact Assessment Rules
Issue impact is determined using deterministic, rule-based logic to ensure consistency and transparency.

An issue is classified as **High Impact** if any of the following conditions are met:
- Multiple users are affected
- The issue completely prevents the user from performing required work
- A phishing-related issue involved a clicked link or opened attachment

An issue is classified as **Medium Impact** if:
- A single user is affected
- Work is partially disrupted but not fully blocked

An issue is classified as **Low Impact** if:
- The issue is informational in nature
- The disruption is minimal or non-urgent

## Priority Mapping
Based on the assessed impact level, issues are assigned a priority to guide response time:

- **High Impact:** Priority 1 (P1)
- **Medium Impact:** Priority 2 (P2)
- **Low Impact:** Priority 3 (P3)
