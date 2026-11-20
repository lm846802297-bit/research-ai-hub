# Repository instructions — Research AI Hub

These instructions are mandatory for agents and contributors.

## Research execution architecture

Before orchestrating or performing research computations, read [RESEARCH_COMPUTE_POLICY.md](RESEARCH_COMPUTE_POLICY.md).

- Select primary compute by active mode: ordinary GPT chat uses the ChatGPT-provided Linux environment; Codex and ChatGPT Work use the user's Windows local environment when available.
- GitHub is the canonical versioned archive for source, inputs, run manifests, native outputs, plots, checksums, and validation evidence.
- GitHub Actions is reserved for independent verification, regression tests, and CI. Do not route the primary calculation to Actions by default.
- If a task requires an external research backend or specialized toolchain unavailable in the selected primary environment, designate that backend explicitly in the task/run manifest and record its provenance. Do not describe remote execution as local execution.
- Distinguish orchestration success from actual scientific execution, numerical validation, and physical validation. A successful agent or workflow response is not itself evidence that a calculation ran or that a physical result is correct.
- Preserve exact source revisions, input hashes, parameters, environment, outputs, and validation status for every substantive run.
- Never expose or commit API keys, tokens, credentials, private data, or machine-specific secrets.
