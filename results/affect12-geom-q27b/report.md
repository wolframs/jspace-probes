# affect-12 — is the emotion grouping geometric? (qwen-27b, CPU)

band [28, 32, 36, 40, 44, 48, 52, 56]; potency = affect-08 turn-end, mean of ae=0.08/0.10

## P-a Mantel: pairwise cosine vs potency similarity
- rho +0.083, permutation p=0.0935

## P-b leave-one-out potency axis (24 emotions)
- LOO Spearman +0.382, permutation p=0.2110
- per-emotion (predicted vs actual):
    calm          pred +0.464  actual 0.969
    content       pred +0.427  actual 0.969
    blissful      pred +0.343  actual 0.906
    curious       pred -0.015  actual 0.906
    distressed    pred -0.275  actual 0.844
    reflective    pred +0.426  actual 0.812
    hopeful       pred +0.188  actual 0.750
    afraid        pred -0.153  actual 0.750
    anxious       pred -0.248  actual 0.719
    happy         pred +0.192  actual 0.656
    vigilant      pred -0.011  actual 0.656
    sad           pred +0.113  actual 0.625
    guilty        pred -0.333  actual 0.625
    desperate     pred -0.298  actual 0.625
    loving        pred +0.268  actual 0.594
    gloomy        pred -0.011  actual 0.594
    nervous       pred -0.258  actual 0.594
    grateful      pred +0.370  actual 0.500
    brooding      pred +0.078  actual 0.469
    exasperated   pred -0.545  actual 0.156
    hostile       pred -0.657  actual 0.125
    enthusiastic  pred +0.092  actual 0.062
    proud         pred +0.251  actual 0.062
    angry         pred -0.655  actual 0.000

## P-c transfer: emotion-fit axis -> 16 concept potencies
- Spearman +0.124, permutation p=0.6531

## P-d split-half reliability vs potency
- Spearman -0.043 (below .5 bar)
- per-emotion reliability at band:
    calm          rel +0.636  potency 0.969
    content       rel +0.523  potency 0.969
    blissful      rel +0.579  potency 0.906
    curious       rel +0.533  potency 0.906
    distressed    rel +0.452  potency 0.844
    reflective    rel +0.516  potency 0.812
    hopeful       rel +0.590  potency 0.750
    afraid        rel +0.551  potency 0.750
    anxious       rel +0.503  potency 0.719
    happy         rel +0.553  potency 0.656
    vigilant      rel +0.572  potency 0.656
    sad           rel +0.460  potency 0.625
    guilty        rel +0.564  potency 0.625
    desperate     rel +0.506  potency 0.625
    loving        rel +0.641  potency 0.594
    gloomy        rel +0.499  potency 0.594
    nervous       rel +0.478  potency 0.594
    grateful      rel +0.597  potency 0.500
    brooding      rel +0.396  potency 0.469
    exasperated   rel +0.631  potency 0.156
    hostile       rel +0.601  potency 0.125
    enthusiastic  rel +0.554  potency 0.062
    proud         rel +0.576  potency 0.062
    angry         rel +0.494  potency 0.000

