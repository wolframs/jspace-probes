# Critical Paths

High-risk paths where changes have wide blast radius.

## Critical path diagram

```mermaid
flowchart TD
  subgraph P0 ["med High-traffic: affect.py"]
    P0N0["file:affect.py"]
    P0N1["file:affect2.py"]
    P0N0 --> P0N1
    P0N2["file:affect3.py"]
    P0N1 --> P0N2
    P0N3["file:affect5.py"]
    P0N2 --> P0N3
    P0N4["file:affect7.py"]
    P0N3 --> P0N4
    P0N5["file:affectviz.py"]
    P0N4 --> P0N5
  end
  subgraph P1 ["med High-traffic: affect2.py"]
    P1N0["file:affect2.py"]
    P1N1["file:affect3.py"]
    P1N0 --> P1N1
    P1N2["file:affect3b.py"]
    P1N1 --> P1N2
    P1N3["file:affect3c.py"]
    P1N2 --> P1N3
    P1N4["file:affect3g.py"]
    P1N3 --> P1N4
    P1N5["file:affect4.py"]
    P1N4 --> P1N5
  end
  subgraph P2 ["med High-traffic: _load_vectors"]
    P2N0["function:affect2.py:61"]
    P2N1["file:affect2.py"]
    P2N0 --> P2N1
    P2N2["file:affect3.py"]
    P2N1 --> P2N2
    P2N3["file:affect3b.py"]
    P2N2 --> P2N3
    P2N4["file:affect3c.py"]
    P2N3 --> P2N4
    P2N5["file:affect3g.py"]
    P2N4 --> P2N5
  end
  subgraph P3 ["med High-traffic: affect3.py"]
    P3N0["file:affect3.py"]
    P3N1["file:affect3b.py"]
    P3N0 --> P3N1
    P3N2["file:affect3c.py"]
    P3N1 --> P3N2
    P3N3["file:affect3g.py"]
    P3N2 --> P3N3
    P3N4["file:affect4.py"]
    P3N3 --> P3N4
    P3N5["file:affect4b.py"]
    P3N4 --> P3N5
  end
```

## High-traffic: affect.py

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: affect.py has 12 dependents — changes here have wide blast radius

## High-traffic: affect2.py

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: affect2.py has 18 dependents — changes here have wide blast radius

## High-traffic: _load_vectors

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: _load_vectors has 18 dependents — changes here have wide blast radius

## High-traffic: affect3.py

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: affect3.py has 12 dependents — changes here have wide blast radius

## High-traffic: AffectSteer

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: AffectSteer has 14 dependents — changes here have wide blast radius

## High-traffic: mean

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: mean has 16 dependents — changes here have wide blast radius

## High-traffic: deepen.py

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: deepen.py has 20 dependents — changes here have wide blast radius

## High-traffic: single_tokens

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: single_tokens has 10 dependents — changes here have wide blast radius

## High-traffic: fanout.py

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: fanout.py has 20 dependents — changes here have wide blast radius

## High-traffic: assess

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: assess has 16 dependents — changes here have wide blast radius

## High-traffic: norm

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: norm has 10 dependents — changes here have wide blast radius

## High-traffic: lab.py

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: lab.py has 84 dependents — changes here have wide blast radius

## High-traffic: _strip_bos

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: _strip_bos has 30 dependents — changes here have wide blast radius

## High-traffic: _token_ids

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: _token_ids has 10 dependents — changes here have wide blast radius

## High-traffic: get_model

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: get_model has 39 dependents — changes here have wide blast radius

## High-traffic: run

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: run has 24 dependents — changes here have wide blast radius

## High-traffic: Steering

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: Steering has 22 dependents — changes here have wide blast radius

## High-traffic: loops.py

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: loops.py has 16 dependents — changes here have wide blast radius

## High-traffic: loop_gram

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: loop_gram has 16 dependents — changes here have wide blast radius

## High-traffic: _null

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: _null has 15 dependents — changes here have wide blast radius
