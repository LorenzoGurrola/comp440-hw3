"""Your agent's loop, which you design in step 1a. The homework page says what the
loop is for, under "1a. Design the loop" (also in instructions/part1.md), and the
check tells you each rule it must follow when your loop breaks it.

You design the loop as an outline in plain words, in WRITEUP.md under 1a. The
loop below the line that says where it goes is Claude's translation of that
outline, written with the parts in loop_parts.py: each line of your outline is a
comment, with about one line of Python for it under it. To change the loop,
change your outline and ask Claude to translate it again.

Check it after each translation. The check uses a scripted stand-in for the
model and for Wikipedia, so it needs no key and costs nothing:

    uv run python check_loop.py

Part 0 runs the agent on the reference loop. Once every rule passes, the agent
runs on this loop and no other: the runs of 1c and later need it to pass.
"""

import anthropic

# The names below include every one the file had before the parts, so that a loop written
# then still runs.
from agent import (ACCEPTED, DECLINED, INSTRUCTIONS, MAX_REJECTED, MAX_STEPS, MODEL, NO_ANSWER,
                   OUT_OF_STEPS, RAN_OUT, REJECTED, REJECTED_TOO_OFTEN, REMINDED, REMINDER,
                   TOOLS, answer_problem, clean_answer, finish, run_tool)
from loop_parts import Conversation


def run_agent(claim, client=None, max_steps=MAX_STEPS, lookup=run_tool):
    """Check one claim. Returns what talk.accept() or talk.stop() returns."""
    client = client or anthropic.Anthropic()
    system = INSTRUCTIONS.read_text()
    messages = [{"role": "user", "content": f"Claim: {claim}"}]
    trace, read_so_far = [], []
    talk = Conversation(claim, client, system, messages, trace, read_so_far, lookup)
    steps = 0          # lookups made so far
    rejected = 0       # answers sent back so far

    # Your loop should repeatedly call the model with the message history so far, and ask for
    # its next step. It should check whether the model has given an answer yet. If not, it should
    # make the lookups that step asks for, and add what they return to the history. It should
    # also pay attention to whether the loop has reached its limit: a claim that runs out of
    # lookups cannot be decided.
    # ---- your loop goes below this line (step 1a) ----

    # Remember: all text you have read so far (none yet), which pages you have visited (none yet),
    # and how many lookups you have made (none yet).
    # (all text read so far is read_so_far, and lookups made is steps: both are set up above)
    visited = []

    # While either the total number of loops is less than 12, or no verdict has been reached yet
    # ("the total number of loops" read as the lookups made, steps; 12 is max_steps. The outline
    # remembers no verdict; the loop returns as soon as it has one, so inside the loop "no verdict
    # has been reached yet" is always true.)
    while steps < max_steps or True:

        #     Randomly choose between the following
        pass  # not translated: the choice is between the two lines below, which are not translated

        #         Query a wikipedia page that both closely matches text in the claim, and that you haven't seen yet
        pass  # not translated: this line does not say who picks the query or how; the parts can only make a lookup the model asked for

        #         Query a wikidata page that both closely matches text in the claim, and that you haven't seen yet
        pass  # not translated: this line does not say who picks the query or how; the parts can only make a lookup the model asked for

        #     Ask the model to read the page
        # (read as: ask the model for its next step, sending it the whole conversation so far. No
        # line above chose a page, so no page is added to what it is sent.)
        reply = talk.ask()

        #     Check if there is some evidence in the page that either confirms the claim or refutes it.
        pass  # not translated: this line does not say what happens; no part reads a page for evidence

        #         If so, return that verdict
        pass  # not translated: this line needs the result of the check above, which is not translated

        #         If not, continue with the next loop
        continue
