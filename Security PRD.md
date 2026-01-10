1. Security Principles

Zero Trust: never trust client input
Least Privilege: every role gets minimum access
Defense in Depth: multiple layers, not one fix
Auditability: everything important is logged

2. Authentication Requirements
Strong password policy (length + entropy)
Password hashing: Argon2 (preferred) or bcrypt
Rate limiting on login & reset
Session expiry + rotation
Secure cookies: HttpOnly, Secure, SameSite=Strict
MFA mandatory for:
Admins
Pastors
Moderators

3. Authorization & Roles
Define explicit roles:
Visitor (unauthenticated)
Authenticated User
Pastor
Moderator
Admin
Rules:
No shared permissions
Object-level permissions (Django Guardian or custom)
Every HTMX endpoint must enforce role checks
Admin URLs protected AND obscured

4. CSRF Protection
CSRF tokens required on ALL state-changing requests
HTMX headers validated
No unsafe GET mutations
CSRF exemptions must be documented and reviewed

5. XSS Protection
Auto-escape enabled everywhere
HTML sanitization (Bleach) for:
Testimonies
Sermons
Comments
Content Security Policy (CSP) enforced
No inline JS

6. File Upload Security
Allowlist file types only
Validate MIME + extension
Max file size enforced
Virus scanning (ClamAV or external)
Store uploads outside web root
Serve via signed URLs or separate domain

7. Data Protection
Encrypt sensitive fields at rest:
Counseling messages
Emails (optional)
Secrets stored only in environment variables
No secrets in repo, ever
Regular key rotation

8. Live Chat / Counseling Security
Authenticated-only access
Conversation-level authorization
Message encryption at rest
Message retention policy (auto-delete after X days)
Full audit trail for moderators (not content access)

9. Admin & Moderation Security
Custom admin dashboard (not default Django admin exposed)
IP allowlist for admins (optional but recommended)
Action logging:
Approvals
Deletions
Edits
Two-man rule for:
Deleting testimonies
Publishing sermons (optional)

10. Logging & Monitoring
Centralized logging
No PII in logs
Alerts for:
Failed logins
Privilege escalation attempts
File upload anomalies
Daily automated backups
Disaster recovery tested monthly

11. Infrastructure & Transport Security
HTTPS enforced (HSTS enabled)
Secure headers:
CSP
X-Frame-Options
X-Content-Type-Options
Firewall rules
Regular dependency updates
Automated security scans (Snyk / Bandit)

12. Development Rules (THIS IS WHERE MOST PROJECTS FAIL)
No feature ships without threat review
Security review before production deploy
No debug mode in prod — ever
Secrets never logged
PRs rejected if security shortcuts are 

🔐 ADDENDUM: DONATIONS & PAYMENTS SECURITY (PAYSTACK)
This section is mandatory for any feature involving donations, offerings, tithes, or financial contributions.
1. Payment Architecture (Non-Negotiable)
Rules
The platform MUST NOT collect, process, transmit, or store:
Card numbers
CVV
Expiry dates
All payments MUST be processed using Paystack Hosted Checkout or Paystack Pop only.
PCI-DSS compliance is delegated to Paystack.
The platform operates strictly as a payment initiator and verifier.
Violation = immediate rejection of feature.

2. Secure Donation Flow
Client → Server → Paystack → Server (Verify)
User initiates donation
Server generates:
Secure transaction reference
Expected amount & currency
User redirected to Paystack
Paystack processes payment
Server verifies transaction via:
Paystack verification API
Webhook confirmation
Never trust client-side success messages. Ever.

3. Webhook Security (Critical)
Webhook Endpoint Rules
Webhook endpoint must:
Be POST-only
Be hidden and unguessable
Reject all non-Paystack IPs (optional but recommended)
Signature Verification
Every webhook request MUST:
Validate x-paystack-signature
Use Paystack secret key
Invalid signature = immediate reject (HTTP 401)
Replay Protection
Webhooks must be:
Idempotent
Reference-checked
Duplicate references must be rejected

4. Transaction Verification Rules
A donation is considered VALID only if ALL are true:
Payment status = success
Amount matches server-expected amount
Currency matches expected currency
Reference exists and is unused
Transaction verified directly from Paystack API
UI success ≠ payment success

5. Fraud & Abuse Protection
Required Controls
Rate limiting on donation attempts
CAPTCHA on repeated failed attempts
Server-side validation of amount (no client overrides)
Abnormal pattern detection:
Rapid retries
High-frequency donations
Amount manipulation attempts
High-risk transactions
Flag for manual review:
Large donations
Multiple failed attempts followed by success

6. Data Storage & Privacy
Allowed to store
Paystack transaction reference
Amount
Currency
Timestamp
Payment status
Forbidden
Card details
CVV
Full Paystack payload logs
Secrets in logs
PII Handling
Donor data minimized
Logs MUST redact email/phone
Financial records are read-only after confirmation

7. Admin & Financial Controls
Admin Capabilities
View donation summaries
Export reports (CSV/PDF)
Search by reference only
Admin Restrictions
No admin can:
Modify donation records
Mark payments as successful manually
Delete confirmed transactions
All admin actions logged and immutable.

8. Failure Handling
On webhook failure
Retry mechanism required
Alert triggered for:
Failed verification
Signature mismatch
Amount mismatch
On verification failure
Donation marked as:
pending or failed
User notified without revealing internals

9. Security Monitoring & Alerts
Alerts triggered on
Webhook signature failures
Amount mismatches
Replayed references
Excessive donation retries
Webhook downtime
Logs
Centralized
No secrets
No card data
No raw payload dumps

10. Compliance & Audit Readiness
Full donation audit trail retained
Records tamper-proof
Monthly reconciliation with Paystack
Annual security review of payment flow

FINAL HARD RULE (DO NOT IGNORE)
If a donation can be marked successful without Paystack server verification, the system is broken.
No shortcuts.
No “we’ll fix it later”.
Money + faith + users = zero tolerance for sloppiness.