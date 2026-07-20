# affect-01 validation — qwen-27b

Workspace band L28-58 (44%-92% depth). 24 emotions, chance 0.042.

- held-out story top-1: peak 0.847 at L63 (98% depth, motor band)
  curve: L0:0.264 L4:0.306 L8:0.361 L12:0.639 L16:0.625 L20:0.736 L24:0.722 L28:0.750 L32:0.708 L36:0.736 L40:0.722 L44:0.722 L48:0.722 L52:0.750 L56:0.736 L60:0.819
- scenario transfer (raw): peak 0.385 at L55 (86% depth, IN WORKSPACE BAND)
  curve: L0:0.115 L4:0.096 L8:0.135 L12:0.269 L16:0.269 L20:0.308 L24:0.308 L28:0.308 L32:0.250 L36:0.231 L40:0.231 L44:0.154 L48:0.135 L52:0.250 L56:0.346 L60:0.365
- scenario transfer (chat): peak 0.346 at L38 (59% depth, IN WORKSPACE BAND)
  curve: L0:0.077 L4:0.096 L8:0.077 L12:0.269 L16:0.231 L20:0.269 L24:0.212 L28:0.269 L32:0.231 L36:0.269 L40:0.173 L44:0.115 L48:0.154 L52:0.250 L56:0.288 L60:0.231
- valence PC1 |r|: peak 0.968 at L34 (53% depth, IN WORKSPACE BAND)
  curve: L0:0.914 L4:0.904 L8:0.931 L12:0.957 L16:0.958 L20:0.959 L24:0.959 L28:0.965 L32:0.967 L36:0.966 L40:0.962 L44:0.963 L48:0.960 L52:0.954 L56:0.958 L60:0.956
- split-half within-emotion cos: L0:0.036 L4:0.126 L8:0.237 L12:0.395 L16:0.433 L20:0.514 L24:0.499 L28:0.528 L32:0.548 L36:0.572 L40:0.544 L44:0.569 L48:0.561 L52:0.536 L56:0.489 L60:0.489
- split-half between-emotion cos: L0:-0.011 L4:-0.014 L8:-0.019 L12:-0.024 L16:-0.026 L20:-0.028 L24:-0.029 L28:-0.029 L32:-0.029 L36:-0.029 L40:-0.028 L44:-0.029 L48:-0.028 L52:-0.027 L56:-0.026 L60:-0.026
- attribution same-emotion cross-arm cos: L0:0.157 L4:0.223 L8:0.298 L12:0.426 L16:0.431 L20:0.534 L24:0.538 L28:0.550 L32:0.546 L36:0.591 L40:0.574 L44:0.584 L48:0.566 L52:0.556 L56:0.526 L60:0.499
- attribution diff-emotion cross-arm cos: L0:-0.007 L4:-0.010 L8:-0.013 L12:-0.018 L16:-0.018 L20:-0.022 L24:-0.023 L28:-0.023 L32:-0.023 L36:-0.025 L40:-0.024 L44:-0.024 L48:-0.023 L52:-0.023 L56:-0.022 L60:-0.021
- separation anthropic (lower better): L0:-0.043 L4:-0.043 L8:-0.042 L12:-0.043 L16:-0.042 L20:-0.042 L24:-0.042 L28:-0.042 L32:-0.041 L36:-0.042 L40:-0.041 L44:-0.041 L48:-0.042 L52:-0.042 L56:-0.042 L60:-0.042
- separation grandmean: L0:-0.043 L4:-0.042 L8:-0.042 L12:-0.043 L16:-0.042 L20:-0.042 L24:-0.042 L28:-0.042 L32:-0.041 L36:-0.042 L40:-0.041 L44:-0.041 L48:-0.042 L52:-0.042 L56:-0.042 L60:-0.042
- separation meandiff: L0:0.804 L4:0.891 L8:0.898 L12:0.829 L16:0.827 L20:0.795 L24:0.856 L28:0.824 L32:0.813 L36:0.781 L40:0.801 L44:0.803 L48:0.811 L52:0.801 L56:0.788 L60:0.771

Reading guide: reliability = within >> between; attribution-generality (P8) = same >> diff; the depth question = where classification/valence peaks sit relative to the band.