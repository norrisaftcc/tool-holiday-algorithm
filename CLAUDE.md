# CLAUDE.md - Holiday Gifting Dashboard™
## A Gift Coordination System for Optimal Generosity Outcomes

**Purpose**: This document provides context for AI assistants helping build this application.  
**Project Type**: Personal productivity tool / simple web app  
**Vibe**: Helpful startup energy, quietly delightful  
**Last Updated**: November 2025

---

## PROJECT OVERVIEW

### What We're Building

A **reverse gift registry** — instead of listing what *you* want, you track what you're *getting* for others.

**The core experience:**
1. User logs in
2. Sees their list of giftees (people they're shopping for)
3. Each giftee has ranked gift ideas
4. Simple status tracking: considering → acquired → wrapped
5. That's it. Elegant simplicity.

### Why This Exists

Gift-giving coordination is surprisingly difficult:
- Remembering what you've already bought
- Tracking ideas across multiple people
- Avoiding duplicate gifts in families
- Staying within budget across all recipients

This dashboard solves the cognitive load problem with minimal friction.

### Design Philosophy

**Core Principles:**

1. **Velocity Over Perfection**  
   Ship features fast. Iterate based on real usage. A working v0.1 beats a planned v2.0.

2. **Delight in Details**  
   Empty states should have personality. Loading states should feel intentional. Every interaction is an opportunity.

3. **Progressive Disclosure**  
   Start simple. Advanced features reveal themselves to users who need them.

4. **Generous Defaults**  
   The app should work beautifully with zero configuration. Power users can customize.

---

## CORE DATA MODEL

Keep it simple:

```
User
├── id
├── email
├── name
└── created_at

Giftee
├── id
├── user_id (owner)
├── name
├── relationship (optional: "sister", "coworker", etc.)
├── budget (optional)
├── notes (optional)
└── created_at

GiftIdea
├── id
├── giftee_id
├── title
├── description (optional)
├── url (optional - link to product)
├── price (optional)
├── rank (1 = top choice, higher = lower priority)
├── status: "considering" | "acquired" | "wrapped" | "given"
└── created_at
```

**That's the whole schema.** Resist the urge to add complexity.

---

## USER EXPERIENCE

### Key Screens

1. **Dashboard** (home)
   - List of giftees with progress indicators
   - Quick-add new giftee
   - Budget overview (if budgets are set)

2. **Giftee Detail**
   - Ranked list of gift ideas
   - Drag to reorder
   - Click to change status
   - Add/edit/remove ideas

3. **Settings** (minimal)
   - Account basics
   - Maybe: default budget, currency preference

### Status Flow

```
considering → acquired → wrapped → given
     ↓            ↓          ↓
   (remove)   (oops, return to considering)
```

Users can move backwards (changed mind, returned item). Status should be forgiving.

### Empty States (Important!)

Empty states are personality opportunities. Examples:

**No giftees yet:**
> "Your generosity awaits direction. Add someone to your list to begin."

**No gift ideas for a giftee:**
> "The perfect gift is out there. Start brainstorming."

**All gifts acquired:**
> "Acquisition complete. Your organizational excellence is noted."

**All gifts wrapped:**
> "Peak preparedness achieved. You are ready."

Keep the tone warm but slightly knowing. Helpful enthusiasm, not corporate-speak.

---

## TECHNICAL APPROACH

### Recommended Stack

**Frontend:**
- React (or Next.js for SSR)
- Tailwind CSS (fast iteration)
- Minimal dependencies

**Backend (choose one):**
- Next.js API routes (simplest if using Next)
- Node.js + Express
- Python + Flask/FastAPI

**Database:**
- SQLite for MVP (seriously, it's fine)
- PostgreSQL if you want to deploy on something like Railway/Render
- Supabase if you want auth handled for you

**Auth:**
- Supabase Auth (easiest)
- NextAuth.js
- Roll your own with sessions (fine for personal project)

### File Structure (React/Next.js example)

```
holiday-gifting-dashboard/
├── CLAUDE.md                 # You are here
├── README.md                 # User-facing documentation
├── package.json
├── .env.example
├── .gitignore
│
├── src/
│   ├── app/                  # Next.js app router
│   │   ├── page.tsx          # Dashboard
│   │   ├── giftee/
│   │   │   └── [id]/
│   │   │       └── page.tsx  # Giftee detail
│   │   ├── settings/
│   │   │   └── page.tsx
│   │   └── api/              # API routes
│   │       ├── giftees/
│   │       └── gifts/
│   │
│   ├── components/
│   │   ├── GifteeCard.tsx
│   │   ├── GiftIdeaRow.tsx
│   │   ├── StatusBadge.tsx
│   │   ├── EmptyState.tsx
│   │   └── ProgressRing.tsx
│   │
│   ├── lib/
│   │   ├── db.ts             # Database connection
│   │   ├── auth.ts           # Auth utilities
│   │   └── types.ts          # TypeScript types
│   │
│   └── styles/
│       └── globals.css
│
├── prisma/                   # If using Prisma ORM
│   └── schema.prisma
│
└── public/
    └── favicon.ico
```

---

## UI COPY GUIDELINES

### Tone

- **Warm but efficient** — like a really organized friend
- **Quietly confident** — the app knows what it's doing
- **Lightly playful** — but never cutesy or annoying
- **Celebration-oriented** — focus on progress, not gaps

### Button Labels

| Instead of... | Consider... |
|---------------|-------------|
| Submit | Save |
| Delete | Remove |
| Create | Add |
| Cancel | Never mind |

### Status Labels

| Internal Status | Display Label | Color |
|-----------------|---------------|-------|
| considering | Considering | Gray |
| acquired | Acquired ✓ | Blue |
| wrapped | Wrapped 🎁 | Purple |
| given | Given 🎉 | Green |

### Progress Messages

When a giftee has all gifts acquired:
> "Gift acquisition complete"

When all gifts are wrapped:
> "Ready for delivery"

When marking something as given:
> "Generosity deployed successfully"

---

## FEATURE PRIORITIZATION

### MVP (v0.1) - Ship This First

- [ ] User authentication (even just email/password)
- [ ] Add/edit/delete giftees
- [ ] Add/edit/delete gift ideas for a giftee
- [ ] Change gift status (the core interaction)
- [ ] Dashboard showing all giftees with progress
- [ ] Mobile-responsive

### v0.2 - Quality of Life

- [ ] Drag-to-reorder gift rankings
- [ ] Budget tracking per giftee
- [ ] Total budget overview
- [ ] Search/filter giftees

### v0.3 - Delight

- [ ] Share a giftee list (read-only link for coordinating with spouse/partner)
- [ ] Import ideas from URL (auto-extract product name/price)
- [ ] Year-over-year history (what did I get them last year?)
- [ ] Gift idea suggestions (based on relationship/budget)

### Maybe Never (Complexity Warning)

- Full family coordination (multiple users, claim gifts)
- Integration with retailers
- AI gift recommendations
- Social features

These add significant complexity. The app's value is simplicity.

---

## DEVELOPMENT WORKFLOW

### Git Conventions

**Branch naming:**
```
feature/add-giftee-crud
fix/status-not-saving
chore/update-dependencies
```

**Commit messages:**
```
feat: add giftee detail page
fix: status badge color not updating
chore: configure eslint
docs: update README with setup instructions
```

### Pull Request Template

```markdown
## What

[Brief description of changes]

## Why

[Motivation for this change]

## Testing

- [ ] Tested locally
- [ ] Works on mobile
- [ ] No console errors

## Screenshots

[If UI changes, include before/after]
```

---

## COMMON PATTERNS

### Loading States

Always show loading states. Never let the UI feel broken.

```tsx
// Good
if (isLoading) return <Spinner />;
if (error) return <ErrorState message={error.message} />;
return <GifteeList giftees={giftees} />;
```

### Optimistic Updates

Update the UI immediately, then sync with server. Makes everything feel fast.

```tsx
// When changing status
const updateStatus = async (giftId: string, newStatus: Status) => {
  // Update local state immediately
  setGifts(prev => prev.map(g => 
    g.id === giftId ? { ...g, status: newStatus } : g
  ));
  
  // Then sync with server
  await api.updateGift(giftId, { status: newStatus });
};
```

### Error Recovery

Always provide a way back:

```tsx
<ErrorState 
  message="Couldn't load your gifts"
  action={{ label: "Try again", onClick: refetch }}
/>
```

---

## METRICS FOR SUCCESS

### User Experience

- Time to add first giftee: < 30 seconds
- Time to add first gift idea: < 15 seconds  
- Time to change status: < 2 seconds (one click/tap)

### Technical

- First contentful paint: < 1.5s
- Time to interactive: < 3s
- Lighthouse score: > 90

### Product

- Does it reduce mental load during gift-giving season?
- Would you actually use this yourself?
- Is it pleasant or just functional?

---

## THINGS TO AVOID

1. **Scope creep** — The core feature is status tracking. Resist adding features until the core is solid.

2. **Over-engineering** — SQLite is fine. A single file component is fine. Ship it.

3. **Feature parity anxiety** — This doesn't need to compete with anything. It needs to solve one problem well.

4. **Premature optimization** — You probably won't have thousands of users. Design for dozens.

5. **Complex state management** — React state + maybe React Query is plenty. No Redux needed.

---

## QUICK START

```bash
# Clone and setup
git clone [repo-url]
cd holiday-gifting-dashboard
npm install
cp .env.example .env.local

# Setup database
npx prisma db push

# Run development server
npm run dev

# Open http://localhost:3000
```

---

## REMEMBER

This is a gift coordination tool. The best feature is the one that helps someone feel less stressed about gift-giving.

Ship early. Iterate often. Measure success by reduced cognitive load.

**Your generosity coordination system awaits activation.** 🎁

---

*Document Version: 1.0*  
*Status: Ready for development*  
*Tone: Helpful enthusiasm with quiet confidence*
