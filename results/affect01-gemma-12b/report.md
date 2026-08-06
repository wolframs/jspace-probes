# affect-01 validation — gemma-12b

Workspace band L28-44 (58%-94% depth). 24 emotions, chance 0.042.

- held-out story top-1: peak 0.571 at L47 (98% depth, motor band)
  curve: L0:0.214 L3:0.250 L6:0.286 L9:0.214 L12:0.214 L15:0.214 L18:0.179 L21:0.250 L24:0.250 L27:0.357 L30:0.357 L33:0.393 L36:0.393 L39:0.357 L42:0.393 L45:0.429
- scenario transfer (raw): peak 0.154 at L25 (52% depth, below band)
  curve: L0:0.000 L3:0.000 L6:0.000 L9:0.077 L12:0.000 L15:0.000 L18:0.000 L21:0.038 L24:0.135 L27:0.154 L30:0.096 L33:0.115 L36:0.154 L39:0.154 L42:0.135 L45:0.077
- scenario transfer (chat): peak 0.212 at L41 (85% depth, IN WORKSPACE BAND)
  curve: L0:0.000 L3:0.000 L6:0.000 L9:0.077 L12:0.000 L15:0.000 L18:0.000 L21:0.077 L24:0.115 L27:0.154 L30:0.154 L33:0.154 L36:0.135 L39:0.192 L42:0.154 L45:0.115
- valence PC1 |r|: peak 0.976 at L47 (98% depth, motor band)
  curve: L0:0.167 L3:0.571 L6:0.556 L9:0.890 L12:0.418 L15:0.949 L18:0.959 L21:0.962 L24:0.963 L27:0.968 L30:0.964 L33:0.968 L36:0.961 L39:0.964 L42:0.968 L45:0.974
- split-half within-emotion cos: L0:0.130 L3:0.082 L6:0.060 L9:0.033 L12:-0.072 L15:-0.002 L18:-0.143 L21:0.134 L24:0.106 L27:0.103 L30:-0.001 L33:0.034 L36:0.052 L39:0.062 L42:0.059 L45:0.079
- split-half between-emotion cos: L0:-0.017 L3:-0.013 L6:-0.018 L9:-0.017 L12:-0.008 L15:-0.009 L18:-0.001 L21:-0.017 L24:-0.013 L27:-0.018 L30:-0.017 L33:-0.022 L36:-0.020 L39:-0.020 L42:-0.019 L45:-0.025
- attribution same-emotion cross-arm cos: L0:nan L3:nan L6:nan L9:nan L12:nan L15:nan L18:nan L21:nan L24:nan L27:nan L30:nan L33:nan L36:nan L39:nan L42:nan L45:nan
- attribution diff-emotion cross-arm cos: L0:nan L3:nan L6:nan L9:nan L12:nan L15:nan L18:nan L21:nan L24:nan L27:nan L30:nan L33:nan L36:nan L39:nan L42:nan L45:nan
- separation anthropic (lower better): L0:-0.042 L3:-0.041 L6:-0.042 L9:-0.042 L12:-0.043 L15:-0.042 L18:-0.042 L21:-0.042 L24:-0.041 L27:-0.042 L30:-0.042 L33:-0.042 L36:-0.042 L39:-0.042 L42:-0.042 L45:-0.042
- separation grandmean: L0:-0.039 L3:-0.040 L6:-0.041 L9:-0.041 L12:-0.038 L15:-0.039 L18:-0.040 L21:-0.042 L24:-0.041 L27:-0.042 L30:-0.042 L33:-0.043 L36:-0.043 L39:-0.043 L42:-0.042 L45:-0.042
- separation meandiff: L0:0.546 L3:0.571 L6:0.725 L9:0.831 L12:0.723 L15:0.811 L18:0.601 L21:0.547 L24:0.659 L27:0.839 L30:0.839 L33:0.826 L36:0.863 L39:0.861 L42:0.824 L45:0.813

Reading guide: reliability = within >> between; attribution-generality (P8) = same >> diff; the depth question = where classification/valence peaks sit relative to the band.