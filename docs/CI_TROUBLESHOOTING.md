# CI troubleshooting

## GitHub-hosted runner fails before the first step

A failure with all of the following properties is a runner-allocation failure, not a pytest failure:

- The job has `runner_id = 0`.
- `runner_name` is empty.
- The job has no steps (`steps = []`).
- The job log endpoint returns 404 / BlobNotFound.
- The job ends within a few seconds.

In this state, checkout, Python setup, package installation, and pytest have not run. Changing test code or pytest configuration cannot fix the missing runner allocation.

### Diagnosis checklist

1. Open **GitHub → Settings → Billing & licensing → Usage** for the account that owns the private repository.
2. Inspect Actions compute usage, included usage, budget, and whether additional usage is blocked.
3. If included compute is exhausted and the budget blocks overage, either wait for the billing-cycle reset or explicitly adjust the account's billing/budget settings.
4. Check **Repository Settings → Actions → General** for Actions policy restrictions and permitted actions.
5. Re-run the workflow only after the account or runner restriction is resolved.

GitHub-hosted runners in private repositories consume the account's included compute allowance and may incur charges beyond it. A workflow YAML change cannot bypass an account-level billing restriction.

## Current PR #1 investigation

The observed run had three matrix jobs for Python 3.11, 3.12, and 3.13. Each job completed in approximately two seconds with runner ID zero, no runner name, no steps, and no downloadable logs. Re-running all failed jobs reproduced the same result.

The workflow YAML was parsed and the three matrix jobs were created, so the failure occurs after workflow/job creation but before a runner begins executing steps. No pytest failure has been observed in GitHub Actions.

The GitHub-hosted runner label is pinned to `ubuntu-24.04` for reproducibility. This does not override billing or account-level runner restrictions.

## Local Windows matrix

When GitHub-hosted compute is unavailable or intentionally not used, run the same three-version matrix on a Windows workstation with `uv`:

    .\scripts\test-python-matrix.ps1

The script installs managed Python 3.11, 3.12, and 3.13 interpreters as needed, creates isolated temporary environments, installs the project with its development dependencies, and runs `python -m pytest -q` for each version.

This local matrix is a separate validation route. A local pass must be reported as local verification, not as a successful GitHub Actions run.
