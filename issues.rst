Known issues
============

- If PyMOL is launched in *command-line-only* mode, failing tests take
  extremely long.
  **Fix:** Run PyMOL in GUI mode by setting ``no_window=False``.
- If PyMOL is launched in *command-line-only* mode, the ``ray`` and ``png``
  commands may not finish before the script finishes, resulting in missing
  output.
  **Fix:** Execute another PyMOL command or ``time.sleep`` for a short time 
  after ``ray`` or ``png``, respectively.