# affect-01 validation — gemma-12b

Workspace band L28-44 (58%-94% depth). 24 emotions, chance 0.042.

- held-out story top-1: peak 0.571 at L47 (98% depth, motor band)
  curve: L0:0.214 L3:0.250 L6:0.250 L9:0.214 L12:0.214 L15:0.179 L18:0.214 L21:0.250 L24:0.250 L27:0.321 L30:0.357 L33:0.357 L36:0.357 L39:0.357 L42:0.357 L45:0.393
- scenario transfer (raw): peak 0.154 at L28 (58% depth, IN WORKSPACE BAND)
  curve: L0:0.000 L3:0.000 L6:0.000 L9:0.077 L12:0.000 L15:0.000 L18:0.000 L21:0.038 L24:0.077 L27:0.135 L30:0.154 L33:0.154 L36:0.135 L39:0.135 L42:0.154 L45:0.077
- scenario transfer (chat): peak 0.212 at L41 (85% depth, IN WORKSPACE BAND)
  curve: L0:0.000 L3:0.000 L6:0.000 L9:0.077 L12:0.000 L15:0.000 L18:0.000 L21:0.077 L24:0.077 L27:0.135 L30:0.135 L33:0.135 L36:0.135 L39:0.192 L42:0.173 L45:0.115
- valence PC1 |r|: peak 0.978 at L46 (96% depth, motor band)
  curve: L0:0.157 L3:0.559 L6:0.540 L9:0.898 L12:0.371 L15:0.951 L18:0.961 L21:0.963 L24:0.965 L27:0.969 L30:0.968 L33:0.970 L36:0.966 L39:0.968 L42:0.971 L45:0.976
- split-half within-emotion cos: L0:0.134 L3:0.079 L6:0.055 L9:0.030 L12:-0.073 L15:-0.008 L18:-0.145 L21:0.124 L24:0.049 L27:0.058 L30:-0.029 L33:0.008 L36:0.020 L39:0.028 L42:0.022 L45:0.052
- split-half between-emotion cos: L0:-0.020 L3:-0.017 L6:-0.028 L9:-0.024 L12:-0.036 L15:-0.029 L18:-0.005 L21:-0.019 L24:-0.018 L27:-0.026 L30:-0.032 L33:-0.033 L36:-0.029 L39:-0.030 L42:-0.026 L45:-0.033
- attribution same-emotion cross-arm cos: L0:nan L3:nan L6:nan L9:nan L12:nan L15:nan L18:nan L21:nan L24:nan L27:nan L30:nan L33:nan L36:nan L39:nan L42:nan L45:nan
- attribution diff-emotion cross-arm cos: L0:nan L3:nan L6:nan L9:nan L12:nan L15:nan L18:nan L21:nan L24:nan L27:nan L30:nan L33:nan L36:nan L39:nan L42:nan L45:nan
- separation anthropic (lower better): L0:-0.042 L3:-0.041 L6:-0.042 L9:-0.042 L12:-0.042 L15:-0.042 L18:-0.042 L21:-0.042 L24:-0.041 L27:-0.042 L30:-0.042 L33:-0.042 L36:-0.042 L39:-0.042 L42:-0.042 L45:-0.042
- separation grandmean: L0:-0.038 L3:-0.040 L6:-0.041 L9:-0.040 L12:-0.037 L15:-0.040 L18:-0.040 L21:-0.042 L24:-0.042 L27:-0.042 L30:-0.042 L33:-0.043 L36:-0.043 L39:-0.043 L42:-0.042 L45:-0.042
- separation meandiff: L0:0.538 L3:0.567 L6:0.720 L9:0.823 L12:0.711 L15:0.796 L18:0.587 L21:0.541 L24:0.663 L27:0.839 L30:0.838 L33:0.826 L36:0.862 L39:0.860 L42:0.823 L45:0.812

Reading guide: reliability = within >> between; attribution-generality (P8) = same >> diff; the depth question = where classification/valence peaks sit relative to the band.