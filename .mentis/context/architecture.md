# Architecture — probes

## System Type

Single Package

## Layers

## Services

## Architecture layers

```mermaid
flowchart TB
  repo["Single Package"]
```

## Domain overview

```mermaid
flowchart LR
  D0["General (55)"]
```

## Capabilities map

```mermaid
flowchart LR
  none["No capabilities detected"]
```

## Languages & parsing

**Detected in this repo:** python (60), javascript (1)

Mnemos uses a lexical code-mask pipeline (52 languages engine-wide). Imports and symbols are extracted only from real code regions — not comments, strings, or Vue templates.

```mermaid
pie showData title Files by language
    "python" : 60
    "javascript" : 1
```

```mermaid
flowchart TD
  START[Parsed file] --> Q{Legacy language?}
  Q -->|typescript javascript python go rust java csharp php ruby kotlin scala swift c cpp| DED[Dedicated regex extractors]
  Q -->|dart elixir terraform solidity vue ...| PROF[Profile-based extractors]
  DED --> MASK[isMatchInCode filter]
  PROF --> MASK
  MASK --> OUT[ParsedImport ParsedSymbol ParsedCall]
```

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
