PRODUCT REQUIREMENTS DOCUMENT (PRD)
Feature: Counsel Sessions & Live Chat System
Project: The Truth Gate

1. PURPOSE & GOAL
Objective

Build a secure, private, real-time counselling and live chat system that allows logged-in users to communicate with pastors/counsellors in a respectful, confidential, and spiritually safe environment.

This system must:

Feel lightweight and non-intrusive

Scale from casual chat → deep counselling

Uphold pastoral confidentiality

Match the institutional-grade UI of The Truth Gate

Failure here = loss of trust.
This feature must feel calm, safe, and professional.

2. USER ROLES
2.1 Regular User (Congregant)

Must be authenticated

Can initiate chats

Can configure message retention

Can delete conversations locally (self-only)

2.2 Counsellor / Pastor

Must be authenticated + authorized

Can receive chat requests

Can view full conversation history

Cannot see when users delete chats locally

Has access to counselling dashboard

2.3 Admin

Manages counsellor accounts

Assigns roles and permissions

Can disable compromised accounts

Cannot read encrypted messages

3. CORE FEATURES
3.1 Floating Live Chat Widget (LinkedIn-style)
Description

A small floating chat widget appears on all public pages (Home, Sermons, About).

Behavior

Fixed position (bottom-right)

Minimal footprint

Neutral, calming design

Shows:

“Chat with a Counsellor”

Online/offline status

Clicking opens mini chat panel

Access Control

If user is not logged in:

Prompt login/signup

If logged in:

Chat opens immediately

3.2 Expand to Full Counsel Page
Feature

A maximize button in the chat header

Clicking it:

Navigates to /counsel/

Opens the full counselling interface

Preserves the active conversation

Counsel Page Includes

Larger chat window

Conversation context

Settings panel

Optional scripture suggestions (future-ready)

3.3 Authentication & Access Control
Rules

Only logged-in users can chat

Counsellors must have is_counsellor=True

No anonymous messages

Session expires on logout

3.4 Message Retention Options (User-Controlled)

Users can choose per conversation:

Disappear after 24 hours

Saved indefinitely

Rules

Retention preference is set at chat start

Counsellor is notified of retention mode

System enforces deletion automatically

3.5 Conversation Deletion (User-Side Only)
User Can:

Clear chat history from their own view

This does NOT delete counsellor records

Counsellor:

Always retains full conversation history

For accountability and continuity of care

4. SECURITY & PRIVACY (NON-NEGOTIABLE)
4.1 End-to-End Encryption (E2EE)
Requirements

Messages encrypted before leaving the client

Only sender and recipient can decrypt

Server stores ciphertext only

Implementation Guidance

Use modern encryption:

AES-256 for message content

RSA / ECC for key exchange

Encryption keys:

User-specific

Stored securely

Never logged

4.2 Zero-Trust Server Design

Server cannot read messages

Admins cannot decrypt chats

Logs must never contain message content

Metadata minimized (timestamps only)

4.3 Data Protection

HTTPS enforced everywhere

CSRF & XSS protection enabled

Rate limiting on chat initiation

Brute-force protection on login

Secure session cookies (HttpOnly, Secure)

4.4 Privacy Guarantees

No third-party analytics on chat pages

No auto-indexing by search engines

Counsel pages excluded from crawlers

Explicit privacy notice displayed

5. DESIGN REQUIREMENTS
5.1 Visual Style

Must strictly follow The Truth Gate design system:

Calm, neutral colors

Soft contrast

Plenty of whitespace

No harsh alerts

No “chat app” gimmicks

Think:

Seminary × Modern SaaS × Minimalist

5.2 Chat UI
Floating Widget

Rounded edges

Subtle shadow

Gentle animations

Non-distracting icon

Full Counsel Page

Two-column layout (chat + settings)

Clear hierarchy

Typography-first design

Focused, quiet atmosphere

6. TECHNICAL REQUIREMENTS
6.1 Backend

Django

Django Channels / WebSockets

Redis for real-time messaging

PostgreSQL for metadata

6.2 Frontend

HTMX or minimal JS

Progressive enhancement

Works without SPA complexity

Mobile-first

6.3 Performance

Messages < 300ms latency

Graceful offline handling

Auto-reconnect WebSockets

7. AUDIT & LOGGING (SAFE ONLY)

Log ONLY:

Message IDs

Sender/receiver IDs

Timestamps

Retention mode

NEVER log:

Message content

Encryption keys

Private metadata

8. FUTURE EXTENSIONS (DO NOT BUILD YET)

Scheduled counsel sessions

Audio/video counselling

AI-assisted scripture prompts (opt-in)

Crisis escalation workflow

9. SUCCESS METRICS

Zero privacy incidents

Sub-1s message delivery

High completion rate of counselling sessions

User trust feedback

FINAL NOTE TO AGENTIC IDE

This is not a casual chat system.
Treat it like digital pastoral care.

If anything compromises:

Privacy

Calmness

Trust

…it fails the product.