# Key Dependencies

Top dependency relationships by frequency.

## Dependency graph (top edges)

```mermaid
flowchart LR
  A0["affect.py"] --> B0["_strip_bos"]
  A0 -. 2x .-> B0
  A1["affect.py"] --> B1["get_model"]
  A1 -. 2x .-> B1
  A2["affect08s.py"] --> B2["_gen"]
  A2 -. 2x .-> B2
  A3["affect08s.py"] --> B3["_mean_resid"]
  A3 -. 2x .-> B3
  A4["affect08s.py"] --> B4["_unit"]
  A4 -. 2x .-> B4
  A5["affect08s.py"] --> B5["outdir"]
  A5 -. 2x .-> B5
  A6["affect08s.py"] --> B6["get_model"]
  A6 -. 2x .-> B6
  A7["affect3.py"] --> B7["Steering"]
  A7 -. 2x .-> B7
  A8["affect3.py"] --> B8["_strip_bos"]
  A8 -. 2x .-> B8
  A9["affect3.py"] --> B9["get_model"]
  A9 -. 2x .-> B9
  A10["affect3.py"] --> B10["_all_resid"]
  A10 -. 2x .-> B10
  A11["affect3.py"] --> B11["_load_vectors"]
  A11 -. 2x .-> B11
  A12["affect3.py"] --> B12["assess"]
  A12 -. 2x .-> B12
  A13["affect3.py"] --> B13["loop_gram"]
  A13 -. 2x .-> B13
  A14["affect3.py"] --> B14["_null"]
  A14 -. 2x .-> B14
```

## Service dependency graph

```mermaid
flowchart TB
  none["No services detected"]
```

- **affect.py → _strip_bos**: 2 references
- **affect.py → get_model**: 2 references
- **affect08s.py → _gen**: 2 references
- **affect08s.py → _mean_resid**: 2 references
- **affect08s.py → _unit**: 2 references
- **affect08s.py → outdir**: 2 references
- **affect08s.py → get_model**: 2 references
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
