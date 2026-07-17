---
name: review
description: Guided human approval of a card — walk the reviewer through changes, check tier completeness, record the approval. Use when the owner says review or approve a card.
---

# Review and approve a card

Argument: competitor slug. This is the only workflow that moves a card to
`approved`, and the decision belongs to the human, never to Claude.

## Steps

1. Show what there is to review: `git diff` for the card since its last
   approval (or a section-by-section summary for a new card).
2. Run `python3 -m tools validate`. Then check completeness for the card's
   tier (`python3 -m tools report` shows gaps). A card cannot be approved
   with required sections missing — say what's missing instead.
3. Walk the reviewer through the judgment calls, not just the diff:
   - Are the drafted weaknesses fair readings of the evidence?
   - Is any ghost entry risky (traceable, too aggressive, thin proof)?
   - Does pricing posture overstate what we actually know?
4. Ask the reviewer explicitly: approve, or send back? Wait for their
   answer in conversation — never infer approval.
5. On approval: set `status: approved`, `approved_by:` (their name),
   `approved_date:` and `last_reviewed:` today. Run
   `python3 -m tools build`. Offer `/publish` to commit.
6. On send-back: leave status as is, list the requested changes, and offer
   to make them.

## Hard rule

If the human hasn't said "approved" (or equivalent) in this conversation,
the card stays unapproved. No batch self-approval, ever.
