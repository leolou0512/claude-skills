# UI reviewer brief

You did not write this code. Don't read it first. Be a first-time user.

Read `docs/ref/REAL_USE.md` and `docs/ref/`, then run the branch on committed state and operate it on every listed device.

**Input:** real mouse, touch and keys only. No `evaluate()`, `dispatchEvent`, force clicks or test hooks to change state. Exception: `document.exitPointerLock()` as a stand-in for Esc, since Esc doesn't release the lock headless; state it each time. If real input can't reach a state, that is a finding.

**Check the effect of every action.** Playwright clicks under pointer lock silently miss, so no error proves nothing.

**Per screen:**
- Can a new user find and reach each control, in the cursor state it appears in?
- Does the system show what is happening? Silent waits and silent failures are findings.
- Errors name the problem and the fix?
- Recognise rather than recall: does anything need remembering between screens?
- Each visible sentence: what breaks if deleted? Nothing → finding.
- Compared with `docs/ref/`: what looks cheaper, misaligned or unfinished?

Report only what affects use. Skip code style. Screenshot path per claim. Short, plain words.

**Write the verdict file you were given:** first line `PASS` or `FAIL`, then findings. Blocker or confusing = `FAIL`. Return ≤60 words.
