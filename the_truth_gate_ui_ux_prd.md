# Product Requirements Document (PRD)

## Project Name

**The Truth Gate**

## Purpose

Design and build an institutional‑grade, trust‑first UI/UX for *The Truth Gate* — a faith‑based digital platform offering sermons, counselling, deliverance sessions, testimonies, and community interaction. The UI must feel calm, authoritative, modern, and emotionally safe, comparable to banks, universities, and healthcare platforms.

This PRD focuses strictly on **UI/UX behavior, structure, and standards**. Technology choices (HTMX, Django, React, etc.) must conform to these requirements — not the other way around.

---

## Product Goals (Non‑Negotiable)

1. **Instant Trust** – Users must feel safe, respected, and guided within 5 seconds.
2. **Emotional Stability** – No visual chaos, no aggressive colors, no gimmicks.
3. **Clarity Over Cleverness** – Every element must justify its existence.
4. **Institutional Credibility** – Feels like a platform that will still exist in 10 years.
5. **Accessibility for Non‑Technical Users** – Especially counsellors, pastors, and older users.

---

## Target Users

### Primary Users

- Individuals seeking counselling, prayer, or spiritual guidance
- Users consuming sermons and testimonies
- Emotionally vulnerable users

### Secondary Users

- Pastor / Counsellors (Admins)
- Content moderators (testimony approval)

### Constraints

- Users may be stressed, grieving, confused, or anxious
- UI must reduce cognitive load, not increase it

---

## Core UX Principles (Hard Rules)

- **Calm > Exciting**
- **Readable > Beautiful**
- **Predictable > Creative**
- **Less Color > More Space**

If an element increases emotional tension, it is rejected.

---

## UI Specification Breakdown

### 1. Physical Metaphors (Mental Models)

UI must map to real‑world expectations.

**Approved Metaphors:**

- Sections → Rooms / Spaces
- Pages → Chapters
- Progress → Journey
- Chat → Private conversation room

**Disallowed:**

- Gamification metaphors
- Loud visual metaphors
- Abstract or confusing symbolism

---

### 2. Color & Emotional Tone

**Primary Objective:** Emotional safety and trust.

**Color Rules:**

- Base palette: Neutral (white, off‑white, soft gray)
- Accent colors: Muted blues, deep greens, soft gold (sparingly)
- Error states: Calm red, never aggressive

**Hard Limits:**

- No more than **2 accent colors** per page
- Backgrounds must be light or very dark — never mid‑tone noise

---

### 3. Typography System (Critical)

Typography is the primary UI.

**Hierarchy:**

- Headings: Clear authority (e.g. Inter, Source Serif, IBM Plex Serif)
- Body: Highly readable sans‑serif (e.g. Inter, IBM Plex Sans)
- Accent / Quotes: Optional serif or italic variant

**Rules:**

- Large line‑height (minimum 1.6)
- Generous margins
- No text smaller than 14px (desktop), 16px preferred

---

### 4. Interaction Design (Non‑Technical Users)

#### Buttons

- Soft edges (rounded, not pill)
- Clear labels (no clever wording)
- One primary action per screen

#### Hover & Feedback

- Subtle shadow or elevation
- Gentle transitions (150–250ms)

#### Navigation

- Obvious paths
- No hidden core actions
- Breadcrumbs where applicable

---

### 5. Motion & Animation

**Purpose:** Reinforce calm, not excitement.

**Allowed:**

- Fade‑in
- Slide‑up (small distance)
- Soft easing

**Banned:**

- Bounce
- Elastic effects
- Flashy loaders

---

## Core Product Sections & Requirements

### 1. Landing Page

**Must Communicate:**

- Safety
- Authority
- Spiritual grounding

**Components:**

- Clear mission statement
- Entry paths (Sermons, Counselling, Testimonies)
- No autoplay media

---

### 2. Sermon Library

**Requirements:**

- Filter by topic, date, speaker
- Clean list view
- Progress memory (resume watching/reading)

---

### 3. Counselling / Live Chat

**Critical Feature**

**Requirements:**

- Private, quiet UI
- Clear session boundaries
- Timestamped messages
- No distracting elements

**UI Tone:**
Feels like a confidential office, not social media chat.



---

### 5. Testimony Section

**User Side:**

- Read‑only
- Categorized
- Emotionally respectful layout

**Admin Side:**

- Approval workflow
- Edit before publish
- Status indicators

---

### 6. Admin Dashboard (Lightweight)

**Audience:** 1–2 trusted users

**Requirements:**

- Simple layout
- No unnecessary analytics
- Content management focus

**Tone:** Functional, not flashy.

---

## Accessibility Requirements

- WCAG AA minimum
- High contrast text
- Keyboard navigable
- Clear focus states

Accessibility is credibility.

---

## Non‑Goals (Explicitly Excluded)

- Trend‑driven UI
- Gamification
- Social media‑style engagement hacks
- Dark patterns

---

## Success Metrics

- Users understand where they are without explanation
- Counselling sessions feel private and respectful
- Admin can operate without training
- UI still feels appropriate 5 years from now

---

## High‑Level Visual Direction

**Descriptors:**

- Warm
- Calm
- Modern
- Trustworthy
- Spiritually grounded

If a design choice conflicts with these words, it is wrong.

---

## Ruthless Final Rule

If your UI draws attention to itself, it has failed.

The UI is not the star.
**The experience is.**

