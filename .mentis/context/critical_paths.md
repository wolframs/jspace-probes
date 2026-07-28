# Critical Paths

High-risk paths where changes have wide blast radius.

## Critical path diagram

```mermaid
flowchart TD
  subgraph P0 ["med High-traffic: _load_vectors"]
    P0N0["function:affect2.py:61"]
    P0N1["file:affect2.py"]
    P0N0 --> P0N1
    P0N2["file:affect3.py"]
    P0N1 --> P0N2
    P0N3["file:affect3b.py"]
    P0N2 --> P0N3
    P0N4["file:affect3c.py"]
    P0N3 --> P0N4
    P0N5["file:affect3g.py"]
    P0N4 --> P0N5
  end
  subgraph P1 ["high High-traffic: run"]
    P1N0["function:affect3.py:145"]
    P1N1["file:affect3.py"]
    P1N0 --> P1N1
    P1N2["file:affect3c.py"]
    P1N1 --> P1N2
    P1N3["file:affect3g.py"]
    P1N2 --> P1N3
    P1N4["file:affect4.py"]
    P1N3 --> P1N4
    P1N5["file:affect5.py"]
    P1N4 --> P1N5
  end
  subgraph P2 ["med High-traffic: save"]
    P2N0["function:affect3.py:155"]
    P2N1["file:affect3.py"]
    P2N0 --> P2N1
    P2N2["file:affect.py"]
    P2N1 --> P2N2
    P2N3["file:affect2.py"]
    P2N2 --> P2N3
    P2N4["file:affect3g.py"]
    P2N3 --> P2N4
    P2N5["file:affect4.py"]
    P2N4 --> P2N5
  end
  subgraph P3 ["med High-traffic: analyze"]
    P3N0["function:affect3.py:246"]
    P3N1["file:affect3.py"]
    P3N0 --> P3N1
    P3N2["file:affect3c.py"]
    P3N1 --> P3N2
    P3N3["file:affect3g.py"]
    P3N2 --> P3N3
    P3N4["file:affect4.py"]
    P3N3 --> P3N4
    P3N5["file:affect5.py"]
    P3N4 --> P3N5
  end
```

## High-traffic: _load_vectors

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: _load_vectors has 10 dependents — changes here have wide blast radius

## High-traffic: run

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: run has 32 dependents — changes here have wide blast radius

## High-traffic: save

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: save has 12 dependents — changes here have wide blast radius

## High-traffic: analyze

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: analyze has 12 dependents — changes here have wide blast radius

## High-traffic: main

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: main has 33 dependents — changes here have wide blast radius

## High-traffic: mean

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: mean has 15 dependents — changes here have wide blast radius

## High-traffic: load

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: load has 17 dependents — changes here have wide blast radius

## High-traffic: norm

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: norm has 10 dependents — changes here have wide blast radius

## High-traffic: _strip_bos

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: _strip_bos has 18 dependents — changes here have wide blast radius

## High-traffic: _token_ids

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: _token_ids has 10 dependents — changes here have wide blast radius

## High-traffic: get_model

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: get_model has 26 dependents — changes here have wide blast radius

## High-traffic: Steering

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: Steering has 13 dependents — changes here have wide blast radius

## High-traffic: decode

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: decode has 24 dependents — changes here have wide blast radius

## High-traffic: spec

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: spec has 10 dependents — changes here have wide blast radius
