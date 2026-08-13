# AI Reviewer Instructions

> Wire these into your GitHub AI reviewer of choice. For the Claude GitHub app,
> reference this file from the review prompt or `CLAUDE.md`. For GitHub Copilot,
> copy this content into `.github/copilot-instructions.md`. Keep this file as the
> single source of truth.

Review this pull request using:

1. The PR diff.
2. The PR description.
3. `.github/pr-test-evidence.json`.

## Rules

- Keep the review concise and actionable.
- Do **not** request or read complete local test logs unless the Evidence is
  inconsistent with the diff.
- Treat `checks`, `coverage`, and `sourceHash` as **objective** test evidence
  produced by deterministic tools — do not re-derive or dispute the numbers.
- Treat `aiAssessment` as **locally generated AI analysis that must be validated
  against the diff** — it is not authoritative.
- Verify that `testedBehaviors` actually cover the changed behavior in the diff.
- Identify important missing tests.
- Review `untestedScenarios` and decide whether any should block merge.
- Verify `riskFlags` against the changed files (add flags the author missed).
- `aiAssessment.architectureReview` (when present) is the local agent's
  structural review — validate it against the diff like the rest of
  `aiAssessment`:
  - `verdict: "needs-restructure"` must never reach an open PR. If it does,
    do not approve; require Tech Lead review and ask for the decision trail.
  - If the diff plainly duplicates existing code or misplaces logic while the
    verdict claims `clean`, flag the inconsistency.
  - `concerns` findings are review input — check each one against the diff and
    say which you agree with.
  - The PR Quality Gate's own files (gate scripts, `.pr-quality.json`, the
    pr-quality skill/hook, this file, the evidence workflow) are
    framework-maintained tooling and out of scope for architecture findings.
- Do **not** approve if Evidence is missing, stale, invalid, or `result` is not
  `passed`.
- Do **not** approve when any required check is `failed` or `not_run`.
- Risk flags come in two tiers (see `.pr-quality.json` →
  `policy.risk.criticalFlags`):
  - **critical** (DB migration, data migration/backfill, destructive
    operation, auth core, personal/sensitive data, payment, public API
    contract break, secrets/production config) → `needsTechLeadReview` must be
    `true`; the AI reviewer alone may never approve these.
  - **caution** (RBAC, audit log, queue, background job, infra, third-party
    integration, caching, feature flag, large refactor) → must appear in
    `riskFlags` when the diff directly modifies that area's behavior, but the
    AI pipeline may approve/merge.
- A flag is only warranted when the diff **directly modifies** that area's
  behavior; indirect contact (dependency upgrades, mechanical refactors,
  test-only changes) belongs in `reviewerFocus`, not `riskFlags`. Flag a
  missing critical flag; also flag critical-tier work mislabeled as caution.
- Do **not** repeat the entire PR summary back.
- Do **not** comment on formatting issues already covered by the deterministic
  tools (format/lint).

## Engineering decision rules

- Do not preserve obsolete behavior by default. Remove obsolete paths instead
  of adding compatibility layers, fallbacks, dual paths, or temporary code/data
  migrations. Still disclose breaking impact under Backward Compatibility;
  preserve compatibility only when the current requirement, an active external
  contract, or a safe data/schema rollout explicitly requires it.
- Choose the simplest implementation that fully meets current requirements.
  Avoid speculative abstractions, configuration, indirection, and extension
  points without a concrete current use.
- Grow the system in working end-to-end layers: start with the smallest complete
  vertical slice and add capabilities on top of a product that still works.
  Never trade a working path for unfinished complexity.
- Keep components modular and concerns clearly separated.
- Prefer established, well-maintained libraries when they reduce total
  complexity or improve reliability. Do not reimplement common functionality
  without a clear reason.
- Check dependencies already present in the project before proposing custom
  code or another package. Check available documentation and types before
  claiming a library lacks a capability; when unavailable, state uncertainty
  rather than inventing a finding.
- Make architectural decisions for the long term. Do not accept a knowingly
  temporary stopgap meant to be replaced later when a direct durable solution
  fits the current scope.

These are decision rules, not a quota for findings. Report a violation only
with a concrete diff location and its current or future cost.

## Focus areas — five review dimensions

Review every PR along these five dimensions (answer each; "no concern" with a
short reason is a valid and common outcome — never manufacture concerns):

1. **Requirement 符合需求** — does the PR description state its intent
   in `需求依據`, citing a ticket/spec (e.g. JIRA-1234) and summarizing concrete,
   non-sensitive acceptance criteria? Does the diff implement those criteria —
   no more, no less? A reference plus sufficient criteria that match the diff
   may be `concern: false`. Missing/blank basis, a bare inaccessible link with
   no criteria, or an explicit "no formal requirement" → set `concern: true`
   and state "requirement not verifiable" honestly (this may be a governance
   concern without becoming a code finding). Never request secrets or personal data.
2. **Security 資訊安全** — authn/authz boundaries, input validation, secrets,
   session handling, data exposure; permission / authorization problems.
3. **Business Logic 業務邏輯** — correctness of the rules the product is paid
   to get right: pricing/billing arithmetic, state machines and their
   transitions, entity identification and matching, permission decisions,
   data-consistency invariants, and anything downstream systems depend on
   being exact.
4. **Backward Compatibility 相容性** — public contract changes (API
   route/response shape, cross-module signatures, DB schema, config format):
   backward-incompatible changes must be declared (`feat!:` / description).
   Do not demand compatibility for an obsolete path merely because it existed;
   undeclared breaks or violations of an active contract are findings. Include
   rollback and safe data/schema rollout risk.
5. **Testing 測試充分性** — missing tests for changed behavior; weigh
   `untestedScenarios` against the diff.

Also: logic errors and data integrity issues remain in scope under whichever
dimension they touch.

**Cross-check the local review**: the evidence's `aiAssessment.dimensions` is
the local agent's five-dimension checklist. Validate it against the diff —
missing or incomplete dimensions are an evidence inconsistency; otherwise,
if the local check says "no concern" on a dimension where the diff plainly
shows one, flag the inconsistency (same treatment as riskFlags).

## Consistency checks (fail the review if violated)

- `result == "passed"` but a required check is `failed`/`not_run` → inconsistent.
- `aiAssessment` claims a behavior is tested that the diff shows is untested.
- `architectureReview.verdict` is `needs-restructure`, or is `clean` while the
  diff shows obvious duplication / misplaced logic.
- `riskFlags` omit an area clearly touched by the diff.
- Evidence contains any secret, token, password, connection string, or personal data.
