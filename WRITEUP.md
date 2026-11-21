# COMP 440 HW3 write-up

Name: Lorenzo Gurrola

Type each answer after the `>` under its question. An answer can run over several lines, but a blank line
ends it: to start a new paragraph, put a line with just `>` between the two. In a table, fill every cell
of every numbered row. Claude may paste a program's output where a question asks for it, but never an
answer. The homework page ticks a step when every answer in its section is filled in.

## Learning goals

In this homework you will:

- Understand what makes a program an *agent*. You will study a language model that picks the next Wikipedia search query, reads the page that comes back, and decides when to stop.
- Gain hands-on experience with the loop around the model by writing it yourself: its tools, its instructions, and its limit of 12 lookups.
- Compare the agent with two simpler methods on your claims, and measure how effective each one is.
- Check the agent's evidence yourself, and decide whether accuracy alone is a fair measure of it.

For extra credit, in Part 3, you find out why the agent fails on your claims, make one change, and see where Wikipedia, which is written by its volunteer editors, is thin, out of date or wrong.

# Part 0: Set up and check one claim

## 0a. Get your copy running

There is nothing to write for this step except your name, after `Name:` at the top of this file.

## 0b. Ask the model to assess a claim without tools

What verdict did the model give (*supported*, *refuted* or *doesn't say*), and what reason did it give? Quote the lines of the output that show them.

>The verdict is "doesn't say", and the reason is 'I cannot confirm from memory who composed "Persian Surgery Dervishes" or what that composer's birth date is, so I cannot verify the claim against English Wikipedia.'

## 0c. Give it one search

Which Wikipedia page did it read? Quote the line of the output that shows it.

>"title": "Persian Surgery Dervishes"

Did that page settle the claim correctly? If not, why do you think the search led there?

>No. The birthdate of the composer was not on the page the model read. It looked at that page because the name matches text in the claim very well.

## 0d. Run the agent and read its trace

In one or two sentences, how did the agent get from the claim to its verdict? Point to the trace entries by their numbers.

>It went from the claim, to 1. searching for "Persian Surgery Dervishes", to 2. reading the wikipedia page on Terry Riley, to 3. reading a wikidata page where it found evidence supporting the verdict. (entry 4 is the answer, "supported")

Which lookup would you have done differently, and how? If none, which one surprised you?

>That's about exactly how I would have done it. I wouldn't say any surprised me either.

Describe Wikidata briefly. Why may it be important to this task?

>Wikidata is structured for machines to read easier than Wikipedia. It is important to this task because it has a lot of data that our agents might want to look at in order to determine the truth value of these claims.

# Part 1: How the agent works

## 1a. Design the loop

Your loop should repeatedly call the model with the message history so far, and ask for its next step. It should check whether the model has given an answer yet. If not, it should make the lookups that step asks for, and add what they return to the history. It should also pay attention to whether the loop has reached its limit: a claim that runs out of lookups cannot be decided. One limit is set for you: 12 lookups for a claim.

The Background and an example outline are under 1a on the homework page, and in [instructions/part1.md](instructions/part1.md#1a-design-the-loop).

Write your outline of the loop in the code block: what it remembers, what it repeats, and every way it stops.

```
Remember: all text you have read so far (none yet), which pages you have visited (none yet), and how many lookups you have made (none yet).
While either the total number of loops is less than 12, or no verdict has been reached yet
    Ask model for its next step, and give it the conversation so far
    If it is a verdict, done, proccess is complete
    If it is a lookup or list of lookups, check if we're on the last loop
    If we are on the last loop, return no verdict
    If not, perform those lookup(s)
    Save the results to which pages we've visited, how many lookups we've made, and save the text to the variable as well
    Update the conversation with these variables
    Increment number of loops
    

```

List each thing your loop remembers from one turn to the next, and say what would go wrong without it.

>My loop remembers which webpages it has visited, the text on these pages, the number of lookups made, and the loop number

Now open `reference_loop.py` and compare it with your loop. Describe one difference in implementation and the resulting effects on agent behavior.

>The only difference in implementation I could find was that reference_loop does not track visited pages in a separate variable.

## 1b. Be the agent

The claim: "Vic & Anthony's Steakhouse is located at the American casino that was combined with the California Club. The casino is owned by Landry's, Inc."

List your lookups, in order. Ask Claude to paste every column but the last from `runs/part1/lookups.jsonl`. Type "Why you chose it" yourself.

| # | Tool | What you asked for | Why you chose it |
|---|---|---|---|
| 1 | search | "Vic & Anthony's Steakhouse" | Needed some initial data on the steakhouse|
| 2 | read | "Vic & Anthony's Steakhouse" (no section) | Read the most relevant article on it, found evidence for 1/3 of the claim|
| 3 | search | "Golden Nugget Casinos" | Needed information on the second named location in the claim|
| 4 | search | "golden nugget casinos and California Club" | Realized I could search for info on the combination directly|
| 5 | read | "Golden Nugget Las Vegas" (no section) | Read this article, didn't find anything|
| 6 | search | "California Club" | Searched for this named location|
| 7 | read | "California Club" (no section) | Didn't find anything|
| 8 | search | "golden nugget casino and california club combination" | Searched for very specific phrasing|
| 9 | read | "Golden Nugget Hotel & Casinos" (no section) | Read another article|
| 10 | read | "California Club (casino)" (no section) | Found what I was looking for here|

What is your verdict on the claim, and which sentence or sentences from what you read is it based on?

>True: 
>1: "Vic & Anthony's is an American steakhouse restaurant chain with locations ... inside the Golden Nugget Casinos in Las Vegas..." 
>2: "The Golden Nugget Las Vegas ... is owned and operated by Landry's, Inc." 
>3: "The California Club was combined into the Golden Nugget ..."

## 1c. Watch the agent work

List the three traces you read closely. At least one should be a claim the agent got wrong (if it got any wrong).

| # | Claim (first few words) | Articles | Did it match the dataset's label? | Did it get there for a good reason? Why or why not |
|---|---|---|---|---|
| 1 | The former leader of the school | 2 | no | every peice of the claim except one was correct, and the model retrieved evidence for every piece but assumed something incorrect |
| 2 | Scotland holds both this landmark | 3 | yes | yes, it returned an answer of "doesn't say" after using 11 lookups and being unable to find one piece of the claim |
| 3 | The film, that Buddy Baker | 4 | yes | yes, it searched and got the evidence it needed succesfully |

Which trace did you find most interesting, and what did the agent do well or badly in it?

>I found the first trace I listed to be the most interesting. I originally thought the agent matched the dataset's label, because it retrieved almost all the information it needed. However, it assumed that the son in question was the youngest, when this evidence wasn't found.

## 1d. Write the agent's instructions

What changed in the agent's traces after you wrote your instructions? Give one claim as an example.

>After these instructions, the model got more accurate. For example, in the claim "The former leader of the school...", the model found the correct answer, which was that the claim could not be verified.

## 1e. Start the full run, and predict

Predict the share of claims each version will get right (its verdict matches the dataset's label), as a percentage. A guess is fine; the reasons are what I grade.

| Version | 2 articles | 3 articles | 4 articles | Why you think so |
|---|---|---|---|---|
| No tools | 40% | 40% | 40% | I think no-tools will do a poorer job than the agent, but still hover around 50%, as there are only two options |
| One search | 50% | 40% | 40% | I think one-search will do slightly better than no-tools, but still hover around 50% |
| Agent | 60% | 50% | 40% | The agent's previous runs hovered around 50%. I think this is feasible again. |

How many lookups will the agent make per claim, on average? Why?

>The 

# Part 2: The agent against the baselines

## 2a. Compare accuracy

Ask Claude to paste the report of your full run, from `runs/part2/report.txt`, into the empty block below.

```
```

How do the results compare with your predictions? Where were you furthest off? Use the numbers from your run, by number of articles.

>

Does the gap between the agent and the one-search baseline grow with the number of articles? What in the claims or the traces explains what you see?

>

The no-tools baseline read nothing. How did it do, and what does that tell you about these claims?

>

## 2b. Check the evidence yourself

Fill in one row for each of the first five claims in your full run, in the order of the claims file, where the agent's verdict is *supported* or *refuted*.

| # | Claim (first few words) | Agent's verdict | Matched the dataset's label? | Does the quoted evidence support that verdict? | Why or why not |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

Of the five, how many matched the dataset's label, and for how many of those does the quoted evidence support the verdict?

>

Is accuracy alone a good measure of this agent? Why or why not?

>

# Part 3 (extra credit): Why the agent fails, and one change

## 3a. Sort the failures

Fill in one row for each of the first eight failures in your full run, rows 1 to 8 of the claims table for runs/part2 with "Result" in "The agent" box set to "does not match the dataset's label (any reason)". If you have fewer than eight, fill a row for each and delete the rest.

| Row | Claim (first few words) | Your label | The entry of the trace that shows it | Is the dataset's label right? (yes, no or can't tell) | Claude's label |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |

Where did you and Claude disagree, and who do you think is right?

>

Which kind of failure was most common? If no kind repeats, say which failure you will aim at in 3b, and why.

>

## 3b. Make one change

What did you change, and why did you expect it to help?

>

How many of your evaluation claims did the agent match before the change and after it? Which of your failures from 3a now match?

>

Quote one claim the agent matched before the change and not after it, if there is one, and say what you think happened. If there is none, say so.

>

## 3c. Write it up

What does the agent's loop add over one search, what does it cost, and when would you not use an agent for a job like this? Use your numbers from Part 2 and Part 3.

>

What did your claims show you about Wikipedia as a source? Where it was thin or wrong, why might that be, given who writes it?

>

Your numbers rest on 100 claims. Which of your conclusions would you trust on another 100 claims, which might be chance, and what would you measure to find out?

>
