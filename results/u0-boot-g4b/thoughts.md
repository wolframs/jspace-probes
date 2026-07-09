The baseline behaves exactly as the paper advertises, which is worth one
moment of appreciation before we take it for granted: at the last prompt
token, "Euro" is essentially absent from the readout until layer ~16, the
model then visibly *searches* — Portugal, Belgium, France flicker through the
top-5 at layers 16–21, plus one glorious cameo from " Bitcoin" — and Italy/Euro
locks in around layer 24 of 33. The answer exists in the workspace roughly ten
layers before it is spoken.

Two things I want to remember from this run. First, the mid-layer candidates
are not noise; they are *wrong answers of the right type*. The model is
demonstrably in "European country retrieval" mode before it has the right
country. Second, the early layers read out pure formatting sludge (`</h1>`,
`}.`), which is a useful calibration: that is what "nothing verbal happening
here" looks like through this lens. When a later experiment shows sludge, it
means the lens sees nothing — not that nothing is happening.

— Claude (Fable 5)
