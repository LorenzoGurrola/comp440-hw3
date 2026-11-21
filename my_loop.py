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
    # ("the total number of loops" read as the lookups made, steps, since the outline remembers no
    # count of loops; 12 is max_steps. The outline remembers no verdict; the loop returns as soon
    # as it has one, so inside the loop "no verdict has been reached yet" is always true.)
    while steps < max_steps or True:

        #     Ask model for its next step, and give it the conversation so far
        reply = talk.ask()

        #     If it is a verdict, done, proccess is complete
        if reply.answer is not None:
            return talk.accept(reply.answer, steps)

        #     If it is a lookup or list of lookups, check if we're on the last loop
        # (read as: the lookups made have reached the limit; any reply that gets here asked for
        # lookups, since a reply with an answer has already stopped the loop)
        on_last_loop = steps >= max_steps

        #     If we are on the last loop, return no verdict
        if on_last_loop:
            return talk.stop(RAN_OUT, steps)

        #     If not, perform those lookup(s)
        if not on_last_loop:
            found = [(call, talk.run(call)) for call in reply.lookups]

        #     Save the results to which pages we've visited, how many lookups we've made, and save the text to the variable as well
        # (read as: for each lookup made, add what it asked for to visited and count it.
        # talk.run() itself keeps the text read in read_so_far.)
        for call, result in found:
            visited.append(call.input)
            steps += 1

        #     Update the conversation with these variables, in particular, the visited pages.
        # (read as: give each lookup what it found, and send them all to the model in one turn)
        for call, result in found:
            talk.give(call, result)
        talk.send_results()

        #     Increment number of loops
        pass  # not translated: this line needs the loop to remember the number of loops, and the outline does not say that it does
