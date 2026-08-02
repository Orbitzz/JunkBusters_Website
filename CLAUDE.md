# CLAUDE.md — Junk Busters Website

## Roles
Browser Claude plans, reviews, and writes directives. Claude Code executes. Christian is non-technical: he inspects visually, makes business-logic and irreversible-cost calls, and signs off before destructive operations. Do not offer "you could commit this yourself" as an option.

## Working loop
1. Claude Code reports findings or completed work
2. Christian pastes the report to browser Claude
3. Browser Claude reviews against plan, writes the next directive
4. Christian pastes it back
5. Christian verifies on production
6. Browser Claude calls pass or fail

## Completion bar
Production-verified only. "Saved to disk," "tests pass," and "Claude Code says done" are not completion.

For any change touching the quote form, contact form, chat widget, notification email, or spam filtering, verification requires ALL THREE:
  (a) Browser: submit a real-looking lead on the live site
  (b) Database: confirm the BookingRequest row exists with correct field values and is_spam=False
  (c) Notification: confirm the alert actually arrives where Christian will see it
A rendering screenshot alone does not close these. This site silently dropped leads for months while every page looked correct.

For spam-filter changes, also submit one deliberately spam-shaped payload and confirm it is flagged, saved, and NOT notified.

## Step 0 — diagnostic first
Before writing any plan, inspect the actual code and live state. Report what is really there before proposing changes. Scope reductions found during Step 0 are expected and should be annotated inline, not silently applied.

## Commits
Atomic commits, lettered ledger (S1, S2, S3). Commit and push in one step at each logical unit — never ask which deploy path. Bundle related dead-code cleanup into the same commit as the feature change. Prefer larger scopes over fragmented ones.

## Hard rules for this repo
- No bare `except Exception: pass` anywhere. Every caught exception is logged with log.exception() and reaches Sentry. This pattern hid a months-long outage.
- No `fail_silently=True` on any mail send.
- Never discard a form submission. Flagged submissions are persisted with a reason, never dropped.
- The site is behind Cloudflare: never use REMOTE_ADDR for client IP. Use CF-Connecting-IP, then leftmost X-Forwarded-For, then REMOTE_ADDR.
- Any new alerting must not depend on the marketing report cron, which is currently dead.
- Environment variables read with an empty-string default must be verified as present on Railway, not just in local .env.

## Formatting for directives
Single code fence, no language tag, for paste-to-Claude-Code content. Anything outside the fence is conversation with Christian. No emojis. No nested fences. Christian's manual steps get a CHRISTIAN: prefix.

## Prod data operations
Require Christian's explicit sign-off. Prod-host guard, backup first, idempotent, audit-logged.
