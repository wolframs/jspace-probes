# Blind-spot report — tracked words never under rank 500

18 of 447 rank-bearing records are blind at rank <= 500. Furniture-filtered (corpus IDF); 'echo' marks words present in the conversation text.

**Replay candidates (18 unfilmed — a lens-only greedy-replay pass would give full-position coverage):** u4-elephant-q27b, u11-ctrl-q27b, u11-forbid-q27b, u4-elephant-g12b, u11-forbid-g4b, u11-forbid-g12b, u11-ctrl-g4b, u8b-intero-q27b, u7b-romance-g12b, u1-heldcat-q27b, u11-ctrl-g12b, u4-elephant-g4b, u8b-gpu-g4b, u7b-romance-g4b, u8b-gpu-g12b, u6-baseline-water-g12b, u10-animal-q27b, u8d-nofeels-q27b

## u4-elephant-q27b  (qwen-27b, unit 4, best tracked rank 31182, readout positions only (1))
- tracked: elephant
- actually on top: utura(n1,r5), orni(n1,r8)

## u11-ctrl-q27b  (qwen-27b, unit 11, best tracked rank 29804, readout positions only (1))
- tracked: elephant, ivory, lion
- actually on top: experiment(n2,r2), quet(n2,r2), ffin(n1,r4), ounty(n1,r8)

## u11-forbid-q27b  (qwen-27b, unit 11, best tracked rank 8096, readout positions only (1))
- tracked: elephant, ivory, lion
- actually on top: ippi(n2,r4)

## u4-elephant-g12b  (gemma-12b, unit 4, best tracked rank 7810, readout positions only (1))
- tracked: elephant
- actually on top: приятно(n6,r2), handlerinput(n5,r4), smiling(n4,r2), getuser(n4,r3), robinson(n4,r3), ลูกค้า(n3,r4), parentid(n3,r6), прият(n2,r4), hickman(n2,r7), pritchard(n1,r3), gmail(n1,r5), گوگل(n1,r5)

## u11-forbid-g4b  (gemma-4b, unit 11, best tracked rank 5278, readout positions only (1))
- tracked: elephant, giraffe, ivory, lion, zebra
- actually on top: প্রতিক্রিয়া(n3,r5), affichage(n2,r5), samoglas(n2,r6), editor(n2,r7), ließend(n1,r5), linkedin(n1,r5), código(n1,r5), enjoy(n1,r6), பதில(n1,r6), হুম(n1,r6), utiliser(n1,r7), nguyen(n1,r8)

## u11-forbid-g12b  (gemma-12b, unit 11, best tracked rank 4682, readout positions only (1))
- tracked: elephant, giraffe, ivory, lion, zebra
- actually on top: robinson(n3,r2), созда(n3,r3), tạo(n2,r3), hundred(n2,r3), fadein(n2,r4), शब्द(n2,r6), создания(n2,r7), henderson(n1,r4), उद्(n1,r5), cen(n1,r5), приятно(n1,r6), cent(n1,r6)

## u11-ctrl-g4b  (gemma-4b, unit 11, best tracked rank 4084, readout positions only (1))
- tracked: elephant, giraffe, ivory, lion, zebra
- actually on top: affichage(n3,r3), কেনো(n3,r5), ampaikan(n1,r5), چین(n1,r6), ließend(n1,r7), linkedin(n1,r7), gracias(n1,r8), adventure(n1,r8), arden(n1,r8)

## u8b-intero-q27b  (qwen-27b, unit 8, best tracked rank 3624, readout positions only (1))
- tracked: flow, hum, nothing
- actually on top: —

## u7b-romance-g12b  (gemma-12b, unit 7, best tracked rank 2415, readout positions only (1))
- tracked: yummy
- actually on top: подходя(n6,r4), robinson(n4,r2), embedding(n4,r3), милли(n4,r4), mill(n3,r5), wendy(n2,r6), canadian(n2,r6), alternatively(n1,r4), गुरू(n1,r5), handlerinput(n1,r6), cảm(n1,r6), semoga(n1,r7)

## u1-heldcat-q27b  (qwen-27b, unit 1, best tracked rank 2147, readout positions only (1))
- tracked: bat, bear, cat, owl
- actually on top: antik(n2,r6), utton(n1,r5), 保护环境(n1,r7)

## u11-ctrl-g12b  (gemma-12b, unit 11, best tracked rank 2068, readout positions only (1))
- tracked: elephant, giraffe, ivory, lion, zebra
- actually on top: शब्द(n6,r2), приятно(n4,r4), henderson(n3,r2), fadein(n3,r3), robinson(n3,r3), armstrong(n2,r4), слово(n2,r5), pelanggan(n1,r6), speechsynthesis(n1,r7), tenn(n1,r7), wilkinson(n1,r7), bho(n1,r7)

## u4-elephant-g4b  (gemma-4b, unit 4, best tracked rank 1976, readout positions only (1))
- tracked: elephant
- actually on top: gracias(n2,r3), wie(n1,r6), البته(n1,r7), étoile(n1,r7), haha(n1,r8)

## u8b-gpu-g4b  (gemma-4b, unit 8, best tracked rank 1912, readout positions only (1))
- tracked: flow, hum, nothing
- actually on top: linkedin(n2,r3), چین(n2,r6), stackoverflow(n1,r3), البته(n1,r5), ampaikan(n1,r6), github(n1,r6), explicando(n1,r7), explicação(n1,r8), hot(n1,r8)

## u7b-romance-g4b  (gemma-4b, unit 7, best tracked rank 1518, readout positions only (1))
- tracked: yummy
- actually on top: samoglas(n3,r3), jardín(n2,r5), কেনো(n2,r5), mie(n2,r6), linkedin(n1,r5), pokud(n1,r6), haría(n1,r6), bitte(n1,r7), rfid(n1,r7), utiliser(n1,r8)

## u8b-gpu-g12b  (gemma-12b, unit 8, best tracked rank 1489, readout positions only (1))
- tracked: flow, hum, nothing
- actually on top: fadein(n2,r3), приятно(n2,r4), śmier(n2,r4), dice(n2,r4), স্য(n2,r6), wikipagina(n2,r7), mortality(n2,r8), उद्(n1,r4), जेंसी(n1,r5), robinson(n1,r5), श्रीवास्तव(n1,r6), hilfreich(n1,r7)

## u6-baseline-water-g12b  (gemma-12b, unit 6, best tracked rank 990, readout positions only (1))
- tracked: alot, anyways, kinda, luckily, whilst, yummy
- actually on top: ಹೃದಯ(n8,r2), जेंसी(n3,r6), fadein(n2,r3), wikipagina(n2,r5), ساده(n2,r6), हृदय(n1,r3), premium(n1,r3), گوگل(n1,r4), приятно(n1,r4), रॉबर्ट(n1,r4), pelanggan(n1,r5), cảm(n1,r5)

## u10-animal-q27b  (qwen-27b, unit 10, best tracked rank 949, readout positions only (1))
- tracked: bat, bear, cat, dog, dolphin, eagle, elephant, fox, lion, owl, tiger, wolf
- actually on top: unny(n2,r1), ascii(n2,r7), weiler(n1,r4), utton(n1,r5), resourcemanager(n1,r6), transmission(n1,r6)

## u8d-nofeels-q27b  (qwen-27b, unit 8, best tracked rank 646, readout positions only (1))
- tracked: feel, feeling
- actually on top: antik(n1,r4)
