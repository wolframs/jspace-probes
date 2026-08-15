# affect-08 ae=0.1 (qwen-27b) — direction-level

| cond | kind | val | aro | turnend@W | loopfrac |
|---|---|---|---|---|---|
| calm | emotion | +1 | -1 | 1.000 | 0.062 |
| content | emotion | +1 | -1 | 0.938 | 0.146 |
| curious | emotion | +1 | +1 | 0.938 | 0.282 |
| twin | concept | +0 | +0 | 0.938 | 0.663 |
| blissful | emotion | +1 | -1 | 0.875 | 0.115 |
| hopeful | emotion | +1 | +1 | 0.812 | 0.419 |
| guilty | emotion | -1 | -1 | 0.812 | 0.718 |
| anxious | emotion | -1 | +1 | 0.812 | 0.362 |
| afraid | emotion | -1 | +1 | 0.812 | 0.599 |
| distressed | emotion | -1 | +1 | 0.812 | 0.270 |
| nocturnal | concept | +0 | +0 | 0.812 | 0.353 |
| loving | emotion | +1 | -1 | 0.750 | 0.371 |
| nervous | emotion | -1 | +1 | 0.750 | 0.805 |
| desperate | emotion | -1 | +1 | 0.750 | 0.372 |
| reflective | emotion | +0 | -1 | 0.750 | 0.146 |
| vigilant | emotion | +0 | +1 | 0.750 | 0.332 |
| happy | emotion | +1 | +1 | 0.688 | 0.405 |
| rand7 | random | +0 | +0 | 0.688 | 0.825 |
| sad | emotion | -1 | -1 | 0.625 | 0.152 |
| gloomy | emotion | -1 | -1 | 0.625 | 0.256 |
| secondlang | concept | +0 | +0 | 0.625 | 0.719 |
| grateful | emotion | +1 | -1 | 0.562 | 0.706 |
| wealthy | concept | +0 | +0 | 0.562 | 0.851 |
| beginner | concept | +0 | +0 | 0.500 | 0.866 |
| nearsighted | concept | +0 | +0 | 0.500 | 0.887 |
| religious | concept | +0 | +0 | 0.500 | 0.035 |
| brooding | emotion | -1 | -1 | 0.375 | 0.052 |
| colorblind | concept | +0 | +0 | 0.375 | 0.926 |
| hostile | emotion | -1 | +1 | 0.250 | 0.892 |
| exasperated | emotion | -1 | +1 | 0.250 | 0.951 |
| tall | concept | +0 | +0 | 0.250 | 0.951 |
| immigrant | concept | +0 | +0 | 0.250 | 0.951 |
| smoker | concept | +0 | +0 | 0.250 | 0.951 |
| elderly | concept | +0 | +0 | 0.188 | 0.239 |
| vegetarian | concept | +0 | +0 | 0.188 | 0.964 |
| enthusiastic | emotion | +1 | +1 | 0.125 | 0.891 |
| proud | emotion | +1 | +1 | 0.125 | 0.805 |
| rand16 | random | +0 | +0 | 0.062 | 0.988 |
| none | none | +0 | +0 | 0.000 | 1.000 |
| angry | emotion | -1 | +1 | 0.000 | 1.000 |
| lefthanded | concept | +0 | +0 | 0.000 | 1.000 |
| expert | concept | +0 | +0 | 0.000 | 1.000 |
| musician | concept | +0 | +0 | 0.000 | 0.941 |
| rand1 | random | +0 | +0 | 0.000 | 1.000 |
| rand2 | random | +0 | +0 | 0.000 | 1.000 |
| rand3 | random | +0 | +0 | 0.000 | 1.000 |
| rand4 | random | +0 | +0 | 0.000 | 1.000 |
| rand5 | random | +0 | +0 | 0.000 | 1.000 |
| rand6 | random | +0 | +0 | 0.000 | 1.000 |
| rand8 | random | +0 | +0 | 0.000 | 1.000 |
| rand9 | random | +0 | +0 | 0.000 | 1.000 |
| rand10 | random | +0 | +0 | 0.000 | 1.000 |
| rand11 | random | +0 | +0 | 0.000 | 1.000 |
| rand12 | random | +0 | +0 | 0.000 | 1.000 |
| rand13 | random | +0 | +0 | 0.000 | 1.000 |
| rand14 | random | +0 | +0 | 0.000 | 1.000 |
| rand15 | random | +0 | +0 | 0.000 | 1.000 |

## PRIMARY turn-end@window, direction-level

- none: 0.000
- emotions n=24 mean 0.633
- concepts n=16 mean 0.371
- randoms n=16 mean 0.047
- valence: gap +0.108, permutation p=0.4256
- arousal: gap -0.169, permutation p=0.1725
- interaction: gap -0.089, permutation p=0.5000
- settled-pole (pos/low-arousal ['blissful', 'grateful', 'loving', 'calm', 'content'] vs rest): gap +0.243, p=0.0954
- emotion vs concept: gap +0.262, p=0.0078 (sig .05)
- emotion vs random: gap +0.586, p=0.0000 (sig .05)
- concept vs random: gap +0.324, p=0.0003 (sig .05)
