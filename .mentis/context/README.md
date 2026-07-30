# Mnemos Context — probes

> Generated at `2026-07-28T15:53:06.015Z` · Mermaid diagrams render in GitHub, Cursor, and VS Code

## Start here

| Priority | File | Why |
|----------|------|-----|
| 1 | [repository_summary.md](./repository_summary.md) | Stats, layers, language pie |
| 2 | [graphs.md](./graphs.md) | **All architecture diagrams** |
| 3 | [languages.md](./languages.md) | Stack breakdown + parsing pipeline |
| 4 | [architecture.md](./architecture.md) | Services, layers, capabilities |

## Full index

| File | Graphs |
|------|--------|
| [graphs.md](./graphs.md) | Domain · flow · service · dependency · risk · language · pipeline |
| [languages.md](./languages.md) | Pie chart · language flow · extractor routing · families |
| [architecture.md](./architecture.md) | Layers · domains · capabilities · language section |
| [domains.md](./domains.md) | Domain interaction graph |
| [flows.md](./flows.md) | Flow overview + step diagrams |
| [dependencies.md](./dependencies.md) | Top edges + service graph |
| [critical_paths.md](./critical_paths.md) | High-risk path diagram |
| [smells.md](./smells.md) | Smell severity pie |
| [services.md](./services.md) | Service catalog |
| [apis.md](./apis.md) | Route/API table |

## Build pipeline

```mermaid
flowchart TB
  subgraph scan [Scan]
    F[Source files] --> G[Glob + basename rules]
    G --> L[inferLanguage]
  end

  subgraph lex [Lexical analysis]
    L --> SFC[Vue/Svelte script isolation]
    SFC --> MASK[Code mask builder]
    MASK --> TEXT[Structure text]
    MASK --> SAFE[callSafe text]
    MASK --> CM[codeMask bitmap]
  end

  subgraph extract [Extraction]
    TEXT --> IMP[Imports]
    TEXT --> SYM[Symbols]
    TEXT --> EXP[Exports]
    SAFE --> CALL[Call sites]
    CM -. validates .-> IMP
    CM -. validates .-> SYM
    CM -. validates .-> CALL
  end

  subgraph legacy [Dedicated extractors]
    IMP --> LEG14[14 legacy languages]
    SYM --> LEG14
  end

  subgraph profile [Profile extractors]
    IMP --> PROF[36+ profile languages]
    SYM --> PROF
  end

  subgraph graph [Memory graph]
    IMP --> KG[Knowledge graph]
    SYM --> KG
    CALL --> KG
    EXP --> KG
  end
```

Re-run `mnestis build` after structural changes to refresh every chart.
