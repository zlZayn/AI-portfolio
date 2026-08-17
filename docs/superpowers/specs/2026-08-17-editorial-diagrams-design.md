# Editorial Diagram Redesign

## Goal

Replace the eight Mermaid flowcharts with project-specific editorial SVG diagrams based on `cathrynlavery/diagram-design` 2.4. The diagrams must explain each project's main architectural idea, match the portfolio, remain responsive, and keep the build maintainable.

## Audience And Output

- Audience: technical recruiters and engineering collaborators.
- Detail: balanced; preserve the mechanism that proves each innovation, omit source-level dependencies.
- Output: accessible inline SVG inside the existing self-contained `index.html`.
- Size: responsive `doc-wide` composition with a fixed `viewBox` and mobile-safe labels.
- Motion: none. Every diagram communicates its full meaning in a static frame.

## Visual System

- Use the portfolio palette: warm paper `#faf6ef`, ink `#2d2b55`, muted gray, white surfaces, and orange `#f97316` as the editorial accent.
- Reserve orange for one or two focal elements per diagram.
- Use the site's sans-serif stack with explicit CJK fallbacks. Use monospace only for codes, protocols, and metrics.
- Follow a 4 px grid, restrained 4-8 px radii, no shadows, and low visual density.
- Use orthogonal connectors, distinct attachment points, visible arrow labels, and no overlapping paths.
- Give every SVG a unique accessible title and description.

## Diagram Stories

| Project | Visual type | Architectural story | Focal idea |
| --- | --- | --- | --- |
| AI-decision-maker | Flowchart | Fingerprint cache branches to a zero-token hit or a constrained AI signal path followed by validation and local operations | AI proposes signals; code decides and executes |
| AI-RAG-embed | Architecture | Build and query zones connect semantic chunks, dual indexes, enhanced retrieval, and the original-question bypass | Query enhancement never contaminates the answer prompt |
| AI-schema-mapper | Architecture | Full rows contract to unique values, AI emits a reusable rule asset, and local code applies it across all rows | AI cost scales with unique values, not row count |
| AI-tool-calling | Architecture | MCP and direct Function Calling converge on one registry before entering a guarded execution boundary | One tool definition serves two protocols |
| AI-collaborate | Process | A planner creates sequential stages; agents run in parallel inside each stage; bridge summaries carry focused context forward | Parallel within stages, bridged between stages |
| AI-tier-guardian | Flowchart | Parallel shallow reviewers feed code arbitration; only uncertain cases reach deeper review and human evidence | Zero-token arbitration controls escalation |
| tablesnap | Architecture | Hotkey capture and file input converge on a shared local VLM and export core | Direct visual understanding without an OCR pipeline |
| raw-to-guide | Structured data flow | Unstructured sources become records governed by one Schema contract, then indexes and templates produce an offline H5 | Schema constrains AI output and drives generation |

## Code Architecture

Convert `src/diagrams.py` into a package while preserving `from src.diagrams import render_all`.

- `src/diagrams/__init__.py`: public registry and `render_all()`.
- `src/diagrams/theme.py`: semantic palette and typography roles.
- `src/diagrams/svg.py`: escaped text, canvas, nodes, zones, labels, connectors, and accessibility primitives.
- `src/diagrams/projects/`: one module per project; each module owns only content and layout.
- `tests/test_diagrams.py`: standard-library contract tests without adding a test dependency.

Project render functions stay small by composing shared primitives. SVG generation uses XML-safe escaping and deterministic IDs. No browser-side diagram library or JavaScript is introduced.

## Build And Dependency Changes

- Keep the `render_all() -> dict[str, str]` contract and Jinja integration unchanged.
- Remove the Mermaid CLI subprocess, temporary files, and Puppeteer configuration.
- Update project metadata so it no longer describes Mermaid as a dependency.
- Rebuild `index.html` from source after all checks pass.

## Responsive Integration

- SVGs use a stable `viewBox`, `width="100%"`, and aspect-preserving scaling.
- The project template remains the embedding boundary.
- Diagram CSS controls maximum width, overflow fallback, and mobile spacing without resizing text by viewport width.
- Labels are short enough to remain readable at portfolio column width; dense technical details move to existing prose below the diagram.

## Verification

- Contract tests verify all eight project IDs, accessible SVG metadata, unique ID prefixes, expected focal text, and absence of Mermaid artifacts.
- Run the full portfolio build and verify no diagram error comments are emitted.
- Inspect all diagrams at desktop and mobile widths using browser screenshots.
- Check for clipped text, overlapping connectors, illegible labels, horizontal overflow, and inconsistent accent use.
- Review the final diff for documentation-to-code, naming-to-configuration, and generated-output consistency.

## Documentation

- Update `README.md` to describe editorial SVG diagrams.
- Update `ARCHITECTURE.md` with the package structure, rendering contract, visual rules, and removal of Mermaid/Puppeteer.
- Do not add a changelog or history section.

## Scope Boundaries

- Do not redesign unrelated portfolio sections.
- Do not alter sibling projects; they are read-only architecture sources for this task.
- Do not add animation, remote diagram assets, runtime diagram rendering, or a second output format.
- Preserve all existing project content and screenshots.
