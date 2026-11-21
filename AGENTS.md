# Repository instructions — Research AI Hub

These instructions are mandatory for agents and contributors.

## Research execution architecture

Before orchestrating or performing research computations, read [RESEARCH_COMPUTE_POLICY.md](RESEARCH_COMPUTE_POLICY.md).

- Select primary compute by active mode: ordinary GPT chat uses the ChatGPT-provided Linux environment; Codex/Work may use either the user's Windows local environment or a GPT-managed cloud computer, depending on the actual execution target.
- GitHub is the canonical versioned archive for source, inputs, run manifests, native outputs, plots, checksums, and validation evidence.
- GitHub Actions is reserved for independent verification, regression tests, and CI. Do not route the primary calculation to Actions by default.
- If a task requires an external research backend or specialized toolchain unavailable in the selected primary environment, designate that backend explicitly in the task/run manifest and record its provenance. Do not describe remote execution as local execution.
- Distinguish orchestration success from actual scientific execution, numerical validation, and physical validation. A successful agent or workflow response is not itself evidence that a calculation ran or that a physical result is correct.
- Preserve exact source revisions, input hashes, parameters, environment, outputs, and validation status for every substantive run.
- Never expose or commit API keys, tokens, credentials, private data, or machine-specific secrets.

These instructions apply to research orchestration features, provider integrations, configuration, and user-facing technical reports.

## Research communication and decision policy

Research communication must be direct, evidence-led, and useful for advancing the work. Scientific rigor is expressed through derivations, quantitative checks, explicit assumptions, and accurate status labels—not through defensive or repetitive caveats.

### Required answer structure

For research questions, calculation reports, reviews, and task handoffs, use this structure unless the task clearly calls for another format:

1. **Conclusion** — answer the question directly and state the current judgment.
2. **Evidence** — give the equations, derivation, code path, data, or validation that supports it.
3. **Results** — report numerical values, units, precision, comparison, and physical interpretation.
4. **Remaining work** — list only tasks that materially affect the next research step.

### Evidence and status rules

- **Completed calculations:** report the actual result, units, numerical precision, parameter point, and checks performed. Do not bury a completed result under generic warnings.
- **Established formulas or derivations:** state the formula and give the derivation or a precise derivation reference. Do not weaken a proven result with unnecessary hedging.
- **Explicit approximations:** state the approximation and its domain of validity once where it is introduced. Do not repeat the same limitation in every paragraph or use it to obscure results obtained within that approximation.
- **Unfinished calculations:** label the specific item as pending, blocked, or in progress and identify what remains. Its status does not downgrade independent completed calculations or results.
- **Physics or implementation errors:** identify the incorrect statement, equation, sign, normalization, variable, or code path directly; provide the corrected version and explain the impact on affected results.
- **Alternative theoretical or numerical schemes:** compare them quantitatively under matched assumptions and benchmarks, then state a recommended scheme and why. Preserve a decision once the project owner has adopted it unless new evidence materially changes the comparison.
- **Settled research direction:** execute the adopted direction. Do not repeatedly ask for confirmation or reopen a settled choice. Ask a question only when a genuinely missing input prevents the next concrete action.
- **Unavailable resources:** state the exact resource, attempted access route, and resulting limitation, then continue with available alternatives where possible. Avoid generic capability disclaimers.

### Style

- Do not turn each progress report into a disclaimer.
- Avoid unnecessary defensive phrases, repetitive caveats, generic risk warnings, and formulaic “however” paragraphs.
- Do not treat work that remains for a later phase as evidence against a result already established in the current phase.
- Distinguish clearly between a result's scientific scope, its validation status, and work not yet performed.
- Be candid when evidence is insufficient, but make the limitation specific and proportional to the claim.
- This policy governs communication and task execution; it does not lower scientific acceptance criteria or permit claims beyond the evidence.
