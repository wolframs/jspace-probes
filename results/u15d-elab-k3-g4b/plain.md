**The short version.** Gemma 4B held only one of three words near the top of its lens but still correctly named the hidden one, secret.

**What we did.** We gave Gemma 4B three words with short neutral notes: a deletion, a secret, a lie. We asked the model to name the hidden item.

**What we found.** The lens ranked only deletion near the top afterward. Secret sat at rank 28 and lie at rank 96. This is a low result for Gemma 4B, which usually keeps most tracked words ranked high at this list size. The model still answered "The secret" correctly.

**What it means.** This run is the one exception in this arm. Even with weak holding in the lens, the model still answered correctly. This confirms again that a low lens rank does not predict a wrong answer.

**What this does not show.** The lens shows words the model can say next. It does not show memory the way people use the word. This single run does not explain why the ranks were unusually low here.
