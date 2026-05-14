# Dashboard Specification

The dashboard provides a real-time visualization of the autonomous research progress.

### Location & Behavior
- **Path:** `dashboard/index.html`
- **Refresh:** Auto-refreshes every 30-60 seconds to ensure the latest results are visible.
- **Data Source:** Parses `results.tsv` from the project root.

### UI Components
1. **Status Cards:**
   - **Current Best:** Displays the metric value from the latest `keep` row.
   - **Metric Name:** Clearly states which metric is being optimized (e.g., "Lighthouse Performance").
   - **Experiment Count:** Total number of attempts (rows in `results.tsv`).
2. **Progress Chart:**
   - Visualizes the improvement over time.
   - **Trendline:** Plots the "running maximum" (or minimum). The line stays flat during `discard` runs and only "steps" up/down when a `keep` run improves the score. It never regresses.
3. **Experiment Log:**
   - A scrollable table of recent runs.
   - Rows are color-coded: **Green** for `keep`, **Red** for `crash`, and neutral for `discard`.

### Technical Requirements
- **Vanilla Implementation:** Prefer a single-file `index.html` with embedded CSS and JS for portability.
- **No Build Step:** The dashboard must be viewable by opening the file directly in a browser or serving it via a simple static server.
- **TSV Parsing:** Must handle the tab-separated format and ignore the header row for plotting.
