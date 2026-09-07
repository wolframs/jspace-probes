# apparatus-06/07 — Fig-29B ambiguity commitment, qwen-14b-nf4

16 country pairs x 40 carriers; transition width of the projection share along the pure-endpoint axis at the mixed position (median across items).

| layer | median width | IQR |
|---|---|---|
| L0 | 0.750 | 0.700-0.750 |
| L1 | 0.700 | 0.650-0.700 |
| L2 | 0.650 | 0.600-0.700 |
| L3 | 0.600 | 0.550-0.650 |
| L4 | 0.600 | 0.550-0.650 |
| L5 | 0.550 | 0.550-0.600 |
| L6 | 0.550 | 0.500-0.550 |
| L7 | 0.500 | 0.450-0.550 |
| L8 | 0.500 | 0.450-0.550 |
| L9 | 0.450 | 0.400-0.500 |  <- half-drop knee
| L10 | 0.450 | 0.400-0.450 |
| L11 | 0.400 | 0.350-0.450 |
| L12 | 0.400 | 0.350-0.450 |
| L13 | 0.350 | 0.300-0.400 |
| L14 | 0.350 | 0.300-0.400 |
| L15 | 0.350 | 0.300-0.400 |
| L16 | 0.350 | 0.300-0.400 |
| L17 | 0.350 | 0.300-0.400 |
| L18 | 0.350 | 0.300-0.400 |
| L19 | 0.350 | 0.300-0.400 |
| L20 | 0.350 | 0.300-0.400 |
| L21 | 0.300 | 0.300-0.350 |
| L22 | 0.300 | 0.250-0.350 |
| L23 | 0.300 | 0.250-0.350 |
| L24 | 0.300 | 0.250-0.350 |
| L25 | 0.300 | 0.250-0.350 |
| L26 | 0.300 | 0.250-0.350 |
| L27 | 0.250 | 0.250-0.300 |
| L28 | 0.250 | 0.200-0.300 |
| L29 | 0.250 | 0.200-0.300 |
| L30 | 0.250 | 0.200-0.300 |
| L31 | 0.200 | 0.200-0.250 |  <- floor reached
| L32 | 0.200 | 0.150-0.250 |
| L33 | 0.200 | 0.150-0.200 |
| L34 | 0.200 | 0.150-0.200 |
| L35 | 0.200 | 0.150-0.200 |
| L36 | 0.200 | 0.150-0.200 |
| L37 | 0.200 | 0.150-0.200 |
| L38 | 0.200 | 0.150-0.200 |
| L39 | 0.200 | 0.150-0.250 |

Early-band max width (L0-11): 0.750; workspace plateau 0.300 reached at **L21** (first layer holding it 5 deep); half-drop knee L9; motor-band min 0.200 (first within 0.02 at L31).

Fraction-ported ws onsets for reference: qwen L24, gemma-12b L18, gemma-4b L13; measured (lens-visible) onsets: qwen L28-36, gemma-12b ~L28-35 (int8 lens), gemma-4b late per u16-trawl-g4b.