# apparatus-06/07 — Fig-29B ambiguity commitment, gemma-4b

16 country pairs x 40 carriers; transition width of the projection share along the pure-endpoint axis at the mixed position (median across items).

| layer | median width | IQR |
|---|---|---|
| L0 | 0.800 | 0.800-0.800 |
| L1 | 0.800 | 0.800-0.800 |
| L2 | 0.800 | 0.800-0.800 |
| L3 | 0.800 | 0.800-0.800 |
| L4 | 0.800 | 0.750-0.800 |
| L5 | 0.750 | 0.750-0.800 |
| L6 | 0.750 | 0.700-0.750 |
| L7 | 0.700 | 0.600-0.750 |
| L8 | 0.550 | 0.450-0.700 |  <- half-drop knee
| L9 | 0.600 | 0.450-0.700 |
| L10 | 0.500 | 0.400-0.650 |
| L11 | 0.450 | 0.350-0.550 |
| L12 | 0.400 | 0.350-0.550 |  <- floor reached
| L13 | 0.450 | 0.350-0.550 |
| L14 | 0.450 | 0.400-0.550 |
| L15 | 0.500 | 0.400-0.600 |
| L16 | 0.450 | 0.400-0.562 |
| L17 | 0.500 | 0.400-0.600 |
| L18 | 0.500 | 0.400-0.600 |
| L19 | 0.500 | 0.400-0.600 |
| L20 | 0.500 | 0.400-0.600 |
| L21 | 0.500 | 0.450-0.600 |
| L22 | 0.500 | 0.450-0.600 |
| L23 | 0.500 | 0.400-0.550 |
| L24 | 0.450 | 0.400-0.500 |
| L25 | 0.450 | 0.350-0.500 |
| L26 | 0.400 | 0.350-0.500 |
| L27 | 0.400 | 0.350-0.500 |
| L28 | 0.400 | 0.350-0.500 |
| L29 | 0.400 | 0.350-0.500 |
| L30 | 0.400 | 0.350-0.500 |
| L31 | 0.400 | 0.350-0.500 |
| L32 | 0.450 | 0.350-0.500 |
| L33 | 0.450 | 0.400-0.500 |

Early-band max width (L0-11): 0.800; workspace plateau 0.500 reached at **L10** (first layer holding it 5 deep); half-drop knee L8; motor-band min 0.400 (first within 0.02 at L12).

Fraction-ported ws onsets for reference: qwen L24, gemma-12b L18, gemma-4b L13; measured (lens-visible) onsets: qwen L28-36, gemma-12b ~L28-35 (int8 lens), gemma-4b late per u16-trawl-g4b.