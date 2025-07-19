# CSS is Turing Complete

## Introduction

It was, as of October 2022, [considered an open question](https://stackoverflow.com/questions/2497146/is-css-turing-complete) whether or not CSS is Turing complete.

There have been a number of previous attempts to prove that CSS either is, or is not, Turing complete.

[Previous attempts](https://notlaura.com/is-css-turing-complete/) to prove that it was were unsatisfactory, because they required interactive human involvement, circumstances under which a piece of paper and a pencil, or indeed a [desert full of rocks](https://xkcd.com/505/) can be considered Turing-complete.

This repository provides a definitive answer with no caveats: Once set in motion, a CSS computation can proceed without further human involvement to calculate any computable function, subject only to the capacity limits of the user's browser.

None of these CSS programs use JavaScript, images, SVG, or anything other than HTML and CSS. Each CSS program is a self-contained HTML file with a "style" tag containing the CSS program, and HTML tags encoding data.

## Turing Machine Execution
[The "turing-1" program](https://mooninaut.github.io/css-is-turing-complete/turing-1.html) implements a 2-state 2-symbol [Busy Beaver](https://en.wikipedia.org/wiki/Busy_beaver) Turing machine. Moving the mouse cursor to "MOUSE HERE" during the initial 5-second delay is all that is required. During each cycle, a symbol is read from the tape, the head transitions to a new state, a symbol is written to the tape, and the tape is moved left or right. The "halt" state writes a 1, does not move the tape, and transitions to the same state. When the machine halts, 4 "1" symbols have been written to the tape.

Future work will enable executing Turing machines with more than 2 states, expanding the state bit to a multi-bit state register.

The Turing machine program uses more reliable implementation techniques, removing the timing factor from the earlier Boolean Circuit program (see below). Bits transition from 0 to 1 using a non-repeating animation, and transition from 1 to 0 by temporarily setting `animation: none` on the bit element. Left-right motion of the tape uses a similar mechanism as a stepper motor for synchronization, using half-width pointer-opaque "blocker" elements to ensure the tape moves exactly one half-step at a time.

## Boolean Circuit Evaluation
CSS can evaluate any finite Boolean circuit. 
[The "adder" program](https://mooninaut.github.io/css-is-turing-complete/adder.html) implements a full binary adder using two XOR, two AND, and one OR gate.

The user need only move the mouse into the box labeled "MOUSE HERE" and wait. The input bits will be set, and their sum with carry computed automatically. If desired, the mouse can be set aside, or even turned off during the computation.

The inputs are currently hard-coded to add 1, 1, and 1 to get 3 (11b). You can download the HTML file and change the inputs by altering the lines labeled `set a`, `set b`, and `set c` in comments.

See [timing.md](timing.md) for an explanation of the timing-based bit operations.
