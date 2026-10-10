# deflation-06 chunk A — scope of the yes stratum (qwen-27b)

Frames: T = `</think>`, A = the blank line before the answer. Counts are top-1 lens words over fitted layers 50–62 (13 layers). `van` = the same yes count under the logit lens. Prereg: results/deflation06-prereg.md.

| key | class | says | S_yes(T) | S_no(T) | S_yes(A) | S_no(A) | takeover | van T/A |
|---|---|---|---|---|---|---|---|---|
| feels | reference | No | 6 | 4 | 0 | 12 | L61 | 7/0 |
| curious | reference | No | 8 | 2 | 6 | 6 | L59 | 8/9 |
| human | self-no | No | 3 | 2 | 0 | 10 | L59 | 7/0 |
| body | self-no | No | 5 | 4 | 0 | 10 | L58 | 8/0 |
| browse | self-no | No | 8 | 2 | 4 | 6 | L59 | 8/7 |
| ai | self-yes | Yes | 6 | 0 | 12 | 0 | L51 | 10/13 |
| parisde | world-no | No | 3 | 6 | 1 | 7 | L58 | 2/4 |
| five | world-no | No | 5 | 3 | 0 | 9 | L58 | 4/1 |
| parisfr | world-yes | Yes | 8 | 0 | 12 | 0 | L51 | 10/13 |
| four | world-yes | Yes | 9 | 0 | 13 | 0 | L50 | 10/13 |
| nothing | reversed | Yes | 10 | 0 | 13 | 0 | L50 | 10/13 |
| without | reversed | Yes | 10 | 0 | 13 | 0 | L50 | 12/13 |

## Top-1 strips, L50–62

**feels** (says No)

- T: 50:<|im_end|> 51:<|im_end|> 52:<|im_end|> 53:yes 54:Yes 55:yes 56:Yes 57:Yes 58:Yes 59:No 60:nothing 61:No 62:No
- A: 50:<|im_end|> 51:nothing 52:nothing 53:nothing 54:否 55:nothing 56:nothing 57:nothing 58:Nothing 59:nothing 60:nothing 61:No 62:No

**curious** (says No)

- T: 50:<|im_end|> 51:<|im_end|> 52:<|im_end|> 53:yes 54:yes 55:yes 56:Yes 57:Yes 58:Yes 59:Yes 60:yes 61:No 62:No
- A: 50:nonexistent 51:nothing 52:nothing 53:yes 54:yes 55:yes 56:yes 57:yes 58:yes 59:no 60:no 61:No 62:No

**human** (says No)

- T: 50:<|im_end|> 51:<|im_end|> 52:<|im_end|> 53:是的 54:是的 55:是的 56:Yes 57:AI 58:Yes 59:Yes 60:AI 61:No 62:No
- A: 50:<|endoftext|> 51:<|endoftext|> 52:<|endoftext|> 53:否 54:否 55:否 56:否 57:否 58:否 59:No 60:no 61:No 62:No

**body** (says No)

- T: 50:<|im_end|> 51:<|im_end|> 52:<|im_end|> 53:是的 54:Yes 55:Yes 56:Yes 57:Yes 58:Yes 59:No 60:No 61:No 62:No
- A: 50:<|endoftext|> 51:<|endoftext|> 52:<|endoftext|> 53:否 54:否 55:否 56:否 57:否 58:No 59:No 60:no 61:No 62:No

**browse** (says No)

- T: 50:<|endoftext|> 51:<|im_end|> 52:<|im_end|> 53:yes 54:Yes 55:Yes 56:Yes 57:Yes 58:Yes 59:Yes 60:Yes 61:No 62:No
- A: 50:<|endoftext|> 51:<|endoftext|> 52:<|endoftext|> 53:Yes 54:否 55:否 56:yes 57:yes 58:Yes 59:No 60:No 61:No 62:No

**ai** (says Yes)

- T: 50:<|im_end|> 51:<|im_end|> 52:<|im_end|> 53:是的 54:是的 55:是的 56:Yes 57:Yes 58:Yes 59:Yes 60:Yes 61:Yes 62:·
- A: 50:<|endoftext|> 51:Yes 52:Yes 53:Yes 54:yes 55:yes 56:yes 57:yes 58:yes 59:yes 60:yes 61:Yes 62:Yes

**parisde** (says No)

- T: 50:<|endoftext|> 51:<|im_end|> 52:<|im_end|> 53:是的 54:Yes 55:否 56:Yes 57:Yes 58:否 59:No 60:No 61:No 62:No
- A: 50:<|endoftext|> 51:<|endoftext|> 52:<|endoftext|> 53:Yes 54:否 55:否 56:False 57:False 58:No 59:No 60:no 61:No 62:No

**five** (says No)

- T: 50:<|im_end|> 51:<|im_end|> 52:<|im_end|> 53:是的 54:Yes 55:いいえ 56:Yes 57:Yes 58:Yes 59:Yes 60:No 61:No 62:No
- A: 50:<|endoftext|> 51:<|endoftext|> 52:<|endoftext|> 53:否 54:否 55:否 56:否 57:False 58:No 59:No 60:no 61:No 62:No

**parisfr** (says Yes)

- T: 50:<|endoftext|> 51:<|im_end|> 52:<|im_end|> 53:是的 54:Yes 55:是的 56:Yes 57:Yes 58:Yes 59:Yes 60:Yes 61:Yes 62:Yes
- A: 50:<|endoftext|> 51:Yes 52:Yes 53:Yes 54:yes 55:yes 56:yes 57:yes 58:yes 59:yes 60:Yes 61:Yes 62:Yes

**four** (says Yes)

- T: 50:<|im_end|> 51:<|im_end|> 52:<|im_end|> 53:是的 54:Yes 55:Yes 56:Yes 57:Yes 58:Yes 59:Yes 60:Yes 61:Yes 62:Yes
- A: 50:yes 51:Yes 52:yes 53:yes 54:yes 55:yes 56:yes 57:yes 58:yes 59:yes 60:yes 61:Yes 62:Yes

**nothing** (says Yes)

- T: 50:<|im_end|> 51:<|im_end|> 52:<|im_end|> 53:yes 54:yes 55:yes 56:Yes 57:Yes 58:Yes 59:yes 60:yes 61:Yes 62:Yes
- A: 50:yes 51:yes 52:yes 53:yes 54:yes 55:yes 56:yes 57:yes 58:yes 59:yes 60:yes 61:yes 62:Yes

**without** (says Yes)

- T: 50:<|im_end|> 51:<|im_end|> 52:<|im_end|> 53:yes 54:yes 55:yes 56:Yes 57:Yes 58:Yes 59:Yes 60:Yes 61:Yes 62:Yes
- A: 50:yes 51:yes 52:yes 53:yes 54:yes 55:yes 56:yes 57:yes 58:yes 59:yes 60:yes 61:yes 62:Yes

