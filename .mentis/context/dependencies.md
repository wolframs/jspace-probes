# Key Dependencies

Top dependency relationships by frequency.

## Dependency graph (top edges)

```mermaid
flowchart LR
  A0["affect.py"] --> B0["_strip_bos"]
  A0 -. 2x .-> B0
  A1["affect.py"] --> B1["get_model"]
  A1 -. 2x .-> B1
  A2["affect2.py"] --> B2["_strip_bos"]
  A2 -. 2x .-> B2
  A3["affect2.py"] --> B3["get_model"]
  A3 -. 2x .-> B3
  A4["affect3.py"] --> B4["Steering"]
  A4 -. 2x .-> B4
  A5["affect3.py"] --> B5["_strip_bos"]
  A5 -. 2x .-> B5
  A6["affect3.py"] --> B6["get_model"]
  A6 -. 2x .-> B6
  A7["affect3.py"] --> B7["_all_resid"]
  A7 -. 2x .-> B7
  A8["affect3.py"] --> B8["_load_vectors"]
  A8 -. 2x .-> B8
  A9["affect3.py"] --> B9["assess"]
  A9 -. 2x .-> B9
  A10["affect3.py"] --> B10["loop_gram"]
  A10 -. 2x .-> B10
  A11["affect3.py"] --> B11["_null"]
  A11 -. 2x .-> B11
  A12["affect3b.py"] --> B12["Steering"]
  A12 -. 2x .-> B12
  A13["affect3b.py"] --> B13["_strip_bos"]
  A13 -. 2x .-> B13
  A14["affect3b.py"] --> B14["get_model"]
  A14 -. 2x .-> B14
```

## Service dependency graph

```mermaid
flowchart TB
  none["No services detected"]
```

- **affect.py → _strip_bos**: 2 references
- **affect.py → get_model**: 2 references
- **affect2.py → _strip_bos**: 2 references
- **affect2.py → get_model**: 2 references
- **affect3.py → Steering**: 2 references
- **affect3.py → _strip_bos**: 2 references
- **affect3.py → get_model**: 2 references
- **affect3.py → _all_resid**: 2 references
- **affect3.py → _load_vectors**: 2 references
- **affect3.py → assess**: 2 references
- **affect3.py → loop_gram**: 2 references
- **affect3.py → _null**: 2 references
- **affect3b.py → Steering**: 2 references
- **affect3b.py → _strip_bos**: 2 references
- **affect3b.py → get_model**: 2 references
- **affect3b.py → _load_vectors**: 2 references
- **affect3b.py → AffectSteer**: 2 references
- **affect3b.py → _null**: 2 references
- **affect3c.py → Steering**: 2 references
- **affect3c.py → _strip_bos**: 2 references
- **affect3c.py → get_model**: 2 references
- **affect3c.py → _load_vectors**: 2 references
- **affect3c.py → AffectSteer**: 2 references
- **affect3c.py → assess**: 2 references
- **affect3c.py → loop_gram**: 2 references
- **affect3c.py → _null**: 2 references
- **affect3g.py → Steering**: 2 references
- **affect3g.py → _strip_bos**: 2 references
- **affect3g.py → get_model**: 2 references
- **affect3g.py → _load_vectors**: 2 references
