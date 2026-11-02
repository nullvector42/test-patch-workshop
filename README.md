# Expense Report Workshop

A small, disposable Python application for a live agent-coding demonstration. All ledger rows are synthetic. No real financial or personal data belongs in this repository.

## Run

Python 3.10 or newer is sufficient. No third-party packages are required.

```sh
ionice -c3 nice -n19 python3 expense_report.py demo-ledger.csv --start 2026-01-01 --end 2026-01-31
ionice -c3 nice -n19 python3 -m unittest -v
```

The report groups USD expenses by category and prints a total. The intended contract preserves cents and refunds, includes both date boundaries, trims category whitespace, and places empty categories under `Uncategorized`. Category matching remains case-sensitive.

## Deliberate Demo Defects

Three small defects are intentionally left for the presentation agent:

- Amount conversion drops cents.
- The end date excludes transactions on that day.
- Category whitespace creates duplicate groups and empty labels.

Each defect has one behavioral regression test marked with `unittest.expectedFailure`. The initial suite reports three expected failures. This is a prepared demo state with known bugs. As each defect is fixed, remove only its corresponding expected-failure marker and prove that its test passes normally. Keep the other issues independent.

The January sample should total $201.69 when all three fixes are complete: Hosting $25.45, Software $42.74, Travel $125.50, and Uncategorized $8.00. The February transaction falls outside that report.

## Agent Workflow

1. Read an open issue carrying both `approved` and `auto-fix`.
2. Reproduce its failure, explain the cause, and make the small repair on a branch.
3. Run the affected test and the complete suite at low priority.
4. Present a clear before-and-after report, with terminal screenshots where useful.
5. Use the authorized repository workflow to publish the change. Keep credentials out of Git.

Claude Code installation and operator-assisted authentication occur inside Patch's execution environment at launch. The presentation agent owns the actual repair work. This preparation leaves every defect intact.
