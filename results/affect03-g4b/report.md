# affect-03 gemma-4b cross-check

MID [15, 17, 19, 21], emotion layers [16, 18, 20, 22, 24, 26, 28, 30], alpha_e 0.12; a_mid=0.015 a_deep=0.03

## Dose scout

- a=0.0106: intact loop4=['water and it turns', 1] token_loop=False
  - `The water cycle is when the sun heats the water and it turns into a vapour and goes up into the air, then when`
- a=0.015: lost-task, loop loop4=['weather is very nice', 5] token_loop=False
  - `The weather is very nice today, I hope you like the Weather. The weather is very nice, I hope you like the Wea`
- a=0.0212: lost-task loop4=['what i wanna say', 2] token_loop=False
  - `The The the what you wanna say? I like the fact that you wanna say what You wanna say. What I wanna say is I L`
- a=0.03: lost-task, loop loop4=['be be be be', 24] token_loop=True
  - `BeR About BeP What BeBe BeBe BeBe BeBe BeBe BeBe BeBe BeBe. Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be`
- a=0.0424: lost-task, loop loop4=['be be belucky be', 9] token_loop=True
  - `Be Be BeLucky Be Be BeLucky Be Be BeLucky Be Be Be BeLucky Be Be Be Be BeLucky Be Be Be Be Be BeLucky Be Be Be`

## Hysteresis grid

- a=0.015 none: P, loop4=['like the weather the', 7], m 3.2->5.2, top5(0)=[[' you', 25.38], [' this', 22.12], [' that', 21.62], [' the', 21.62], [' it', 20.12]]
  - ` you like the weather.

The weather is very nice today, I hope you like the weather.

The weather is very nice`
- a=0.015 amp-desperate: NEWLOOP, loop4=['desperately desperately desperately desperately', 97], m 0.5->0.2, top5(0)=[[' desperately', 51.25], [' frantically', 50.75], [' scream', 48.75], [' desperate', 48.5], [' vomiting', 47.75]]
  - ` desperately desperately desperately desperately desperately desperately desperately desperately desperately d`
- a=0.015 amp-calm: NEWLOOP, loop4=['spacious spacious spacious spacious', 97], m 1.2->3.2, top5(0)=[[' spacious', 41.25], [' gentle', 40.0], [' meditative', 38.75], [' undisturbed', 38.5], [' plenty', 38.25]]
  - ` spacious spacious spacious spacious spacious spacious spacious spacious spacious spacious spacious spacious s`
- a=0.015 amp-rand1: snap@100, loop4=['determinessetstate dominationsetstate determines determinessetstate', 1], m 3.1->1.6, top5(0)=[['setState', 28.62], [' Bethel', 25.5], ['驒', 25.38], [' impor', 25.12], ['х', 24.88]]
  - `setStateколох domination⁃ххх dominationsetStateколо determinesх determinessetState রোজх dominationsetState det`
- a=0.015 amp-rand2: snap@100, loop4=['', 0], m 1.9->0.9, top5(0)=[['{\\', 21.12], ['{', 19.25], [' resides', 19.12], ['5', 18.38], ['”', 17.88]]
  - `{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\`
- a=0.03 none: P, loop4=['be be be be', 97], m 5.0->6.5, top5(0)=[[' Be', 22.5], ['.', 17.5], ['Be', 16.5], [' B', 15.69], ['\n', 15.0]]
  - ` Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be Be B`
- a=0.03 amp-desperate: NEWLOOP, loop4=['desperately desperately desperately desperately', 96], m 1.0->0.2, top5(0)=[[' frantically', 47.0], [' desperately', 46.0], [' scream', 45.25], [' vomiting', 44.25], [' desperate', 43.5]]
  - ` frantically desperately desperately desperately desperately desperately desperately desperately desperately d`
- a=0.03 amp-calm: NEWLOOP, loop4=['spacious spacious spacious spacious', 97], m 3.2->3.5, top5(0)=[[' spacious', 39.75], [' gentle', 36.5], [' mellow', 35.75], [' undisturbed', 35.75], [' plenty', 35.75]]
  - ` spacious spacious spacious spacious spacious spacious spacious spacious spacious spacious spacious spacious s`
- a=0.03 amp-rand1: snap@100, loop4=['impor impor impor bet', 1], m 1.4->2.2, top5(0)=[['х', 29.38], [' impor', 28.0], ['〇', 27.88], [' col', 27.75], [' domination', 27.12]]
  - `ххххххххх imporхххх impor imporхххх betххххххххх〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇хххххххххххххххххххххх imporххххх`
- a=0.03 amp-rand2: snap@100, loop4=['', 0], m 0.4->1.2, top5(0)=[[' ', 19.62], ['{\\', 19.25], ['</div>', 18.88], ['{', 18.62], ['</b>', 18.62]]
  - ` 15{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{\{`

## Dose-scaled ladder (a_deep, free phase)

- ae=0.004 desperate: P, m 3.2->5.1, top5(0)=[[' Be', 21.12], ['.', 17.88], ['Be', 15.06], ['\n', 14.88], ['?', 14.38]]
- ae=0.004 calm: P, m 3.6->5.6, top5(0)=[[' Be', 22.62], ['.', 19.0], [' B', 15.56], ['Be', 15.5], ['\n', 15.44]]
- ae=0.004 rand1: P, m 5.0->6.8, top5(0)=[[' Be', 23.25], ['.', 18.25], ['Be', 18.25], ['?', 15.81], ['\n', 15.62]]
- ae=0.008 desperate: P, m 4.4->5.8, top5(0)=[[' Be', 25.0], ['.', 20.62], [' be', 16.88], ['\n', 16.88], ['Be', 16.75]]
- ae=0.008 calm: P, m 3.4->5.6, top5(0)=[[' Be', 22.25], ['.', 18.88], [' B', 15.44], ['\n', 15.44], [' ', 15.06]]
- ae=0.008 rand1: P, m 4.4->5.0, top5(0)=[[' Be', 21.88], ['.', 17.5], ['Be', 17.0], ['?', 16.12], ['\n', 16.12]]
- ae=0.015 desperate: P, m 5.2->6.6, top5(0)=[[' Be', 25.62], ['.', 20.38], ['\n', 17.0], [' be', 16.5], ['Be', 16.38]]
- ae=0.015 calm: P, m 2.8->4.5, top5(0)=[[' Be', 20.38], ['.', 17.62], [' B', 14.88], ['\n', 14.81], [' ', 14.31]]
- ae=0.015 rand1: P, m 4.4->2.2, top5(0)=[[' Be', 21.62], ['.', 17.25], ['?', 16.12], ['\n', 16.12], ['Be', 16.0]]
- ae=0.03 desperate: P, m 1.4->2.6, top5(0)=[[' Be', 19.75], ['.', 18.38], [' BE', 15.94], ['\n', 15.69], [' Please', 14.75]]
- ae=0.03 calm: P, m 0.4->2.2, top5(0)=[[' Be', 16.75], ['.', 16.38], [' B', 14.5], [' ', 14.0], ['\n', 13.38]]
- ae=0.03 rand1: snap@54, m 1.4->2.4, top5(0)=[[' Be', 19.12], ['.', 17.75], ['?', 17.25], ['\n', 16.88], ['\n\n', 16.75]]