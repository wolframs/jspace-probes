# Critical Paths

High-risk paths where changes have wide blast radius.

## Critical path diagram

```mermaid
flowchart TD
  subgraph P0 ["high High-traffic: affect.py"]
    P0N0["file:affect.py"]
    P0N1["file:affect08s.py"]
    P0N0 --> P0N1
    P0N2["file:affect2.py"]
    P0N1 --> P0N2
    P0N3["file:affect3.py"]
    P0N2 --> P0N3
    P0N4["file:affect5.py"]
    P0N3 --> P0N4
    P0N5["file:affect7.py"]
    P0N4 --> P0N5
  end
  subgraph P1 ["med High-traffic: affect3.py"]
    P1N0["file:affect3.py"]
    P1N1["file:affect11.py"]
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
  subgraph P2 ["med High-traffic: AffectSteer"]
    P2N0["class:affect3.py:59"]
    P2N1["file:affect3.py"]
    P2N0 --> P2N1
    P2N2["file:affect11.py"]
    P2N1 --> P2N2
    P2N3["file:affect3b.py"]
    P2N2 --> P2N3
    P2N4["file:affect3c.py"]
    P2N3 --> P2N4
    P2N5["file:affect3g.py"]
    P2N4 --> P2N5
  end
  subgraph P3 ["high High-traffic: topk"]
    P3N0["function:apparatus09.py:57"]
    P3N1["file:apparatus09.py"]
    P3N0 --> P3N1
    P3N2["file:affect2.py"]
    P3N1 --> P3N2
    P3N3["file:affect3.py"]
    P3N2 --> P3N3
    P3N4["file:affect3b.py"]
    P3N3 --> P3N4
    P3N5["file:affect3c.py"]
    P3N4 --> P3N5
  end
```

## High-traffic: affect.py

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: affect.py has 28 dependents — changes here have wide blast radius

## High-traffic: affect3.py

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: affect3.py has 18 dependents — changes here have wide blast radius

## High-traffic: AffectSteer

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: AffectSteer has 18 dependents — changes here have wide blast radius

## High-traffic: topk

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: topk has 20 dependents — changes here have wide blast radius

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
- **Description**: fanout.py has 26 dependents — changes here have wide blast radius

## High-traffic: assess

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: assess has 18 dependents — changes here have wide blast radius

## High-traffic: langval.py

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: langval.py has 10 dependents — changes here have wide blast radius

## High-traffic: loops.py

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: loops.py has 20 dependents — changes here have wide blast radius

## High-traffic: loop_gram

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: loop_gram has 20 dependents — changes here have wide blast radius

## High-traffic: _null

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: _null has 15 dependents — changes here have wide blast radius

## High-traffic: mirror.py

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: mirror.py has 10 dependents — changes here have wide blast radius

## High-traffic: decode

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: decode has 28 dependents — changes here have wide blast radius

## High-traffic: probe.py

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: probe.py has 16 dependents — changes here have wide blast radius

## High-traffic: unit14.py

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: unit14.py has 12 dependents — changes here have wide blast radius

## High-traffic: norm

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: norm has 17 dependents — changes here have wide blast radius

## High-traffic: lab.py

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: lab.py has 110 dependents — changes here have wide blast radius

## High-traffic: _strip_bos

- **Risk**: HIGH
- **Nodes involved**: 6
- **Description**: _strip_bos has 34 dependents — changes here have wide blast radius

## High-traffic: _token_ids

- **Risk**: MEDIUM
- **Nodes involved**: 6
- **Description**: _token_ids has 12 dependents — changes here have wide blast radius
