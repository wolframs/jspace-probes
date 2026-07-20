# affect-01 validation — gemma-4b

Workspace band L16-31 (47%-94% depth). 24 emotions, chance 0.042.

- held-out story top-1: peak 0.889 at L33 (97% depth, motor band)
  curve: L0:0.319 L2:0.333 L4:0.292 L6:0.333 L8:0.417 L10:0.528 L12:0.597 L14:0.611 L16:0.778 L18:0.597 L20:0.736 L22:0.708 L24:0.681 L26:0.667 L28:0.611 L30:0.694 L32:0.847
- scenario transfer (raw): peak 0.250 at L27 (79% depth, IN WORKSPACE BAND)
  curve: L0:0.000 L2:0.000 L4:0.000 L6:0.077 L8:0.000 L10:0.000 L12:0.000 L14:0.000 L16:0.000 L18:0.058 L20:0.019 L22:0.019 L24:0.173 L26:0.212 L28:0.192 L30:0.192 L32:0.192
- scenario transfer (chat): peak 0.173 at L24 (71% depth, IN WORKSPACE BAND)
  curve: L0:0.000 L2:0.000 L4:0.000 L6:0.077 L8:0.000 L10:0.000 L12:0.000 L14:0.000 L16:0.000 L18:0.000 L20:0.058 L22:0.115 L24:0.173 L26:0.154 L28:0.173 L30:0.154 L32:0.135
- valence PC1 |r|: peak 0.972 at L14 (41% depth, below band)
  curve: L0:0.873 L2:0.892 L4:0.922 L6:0.935 L8:0.954 L10:0.968 L12:0.971 L14:0.972 L16:0.969 L18:0.968 L20:0.958 L22:0.946 L24:0.948 L26:0.946 L28:0.954 L30:0.954 L32:0.956
- split-half within-emotion cos: L0:0.009 L2:0.022 L4:0.010 L6:0.018 L8:0.062 L10:0.254 L12:0.256 L14:0.256 L16:0.295 L18:0.304 L20:0.352 L22:0.331 L24:0.334 L26:0.284 L28:0.308 L30:0.296 L32:0.362
- split-half between-emotion cos: L0:-0.020 L2:-0.015 L4:-0.006 L6:-0.005 L8:-0.012 L10:-0.016 L12:-0.011 L14:-0.013 L16:-0.014 L18:-0.014 L20:-0.016 L22:-0.017 L24:-0.017 L26:-0.015 L28:-0.015 L30:-0.015 L32:-0.018
- attribution same-emotion cross-arm cos: L0:0.187 L2:0.203 L4:0.244 L6:0.321 L8:0.369 L10:0.478 L12:0.528 L14:0.489 L16:0.565 L18:0.554 L20:0.548 L22:0.518 L24:0.528 L26:0.517 L28:0.513 L30:0.496 L32:0.495
- attribution diff-emotion cross-arm cos: L0:-0.008 L2:-0.009 L4:-0.010 L6:-0.013 L8:-0.015 L10:-0.019 L12:-0.022 L14:-0.020 L16:-0.023 L18:-0.023 L20:-0.022 L22:-0.021 L24:-0.022 L26:-0.021 L28:-0.021 L30:-0.020 L32:-0.020
- separation anthropic (lower better): L0:-0.042 L2:-0.042 L4:-0.041 L6:-0.042 L8:-0.041 L10:-0.040 L12:-0.041 L14:-0.040 L16:-0.041 L18:-0.042 L20:-0.041 L22:-0.041 L24:-0.041 L26:-0.041 L28:-0.040 L30:-0.040 L32:-0.040
- separation grandmean: L0:-0.041 L2:-0.040 L4:-0.039 L6:-0.041 L8:-0.039 L10:-0.039 L12:-0.036 L14:-0.041 L16:-0.041 L18:-0.041 L20:-0.041 L22:-0.041 L24:-0.041 L26:-0.041 L28:-0.041 L30:-0.041 L32:-0.041
- separation meandiff: L0:0.800 L2:0.821 L4:0.871 L6:0.843 L8:0.888 L10:0.934 L12:0.935 L14:0.971 L16:0.930 L18:0.954 L20:0.948 L22:0.950 L24:0.947 L26:0.950 L28:0.956 L30:0.950 L32:0.905

Reading guide: reliability = within >> between; attribution-generality (P8) = same >> diff; the depth question = where classification/valence peaks sit relative to the band.