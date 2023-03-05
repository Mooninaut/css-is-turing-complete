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
[The "adder" program](https://mooninaut.github.io/css-is-turing-complete/adder.html) implements a full binary adder using two XOR, two AND and one OR gate.


The user need only move the mouse into the box labeled "MOUSE HERE" and wait. The input bits will be set, and their sum with carry computed automatically. If desired, the mouse can be set aside, or even turned off during the computation.

The inputs are currently hard-coded to add 1, 1, and 1 to get 3 (11b). You can download the HTML file and change the inputs by altering the lines labeled `set a`, `set b`, and `set c` in comments.


### Mechanism

Bits are represented by divs that move left and right on a tick-tock cycle, like a metronome.

A 0-bit "ticks" left and "tocks" right.<br>
A 1-bit "ticks" right and "tocks" left.

The value of a bit can be seen during a "tock" cycle, during which a "0" or "1" appears on the un-blocked side of the bit.

Bits can be switched by hovering the mouse cursor over either the top half of the active bit,
or a "pause" button to the left of the bit.

To set a bit, hover over the top half of the active bit during the appropriate half-cycle. If the bit
is in the desired state, nothing will change, but if it is in the other state, it will be delayed
by a half-cycle, switching to the other state.

Using z-index, the read half of bits that are read from (perform output) are moved on top of either
the write half or the pause button of bits that are written to (accept input).
The bits on top block the mouse cursor from activating the hover 

Any boolean gate can be emulated by appropriately positioning combinations of bits under the mouse cursor
in the correct sequence.

The "MOUSE HERE" box changes size continuously to force the browser to perform cursor hit detection
even though the mouse is not moving.

This sample file computes a 1-bit full add with carry, computing a 2-bit sum from inputs A, B and C (carry-in)
to sum and carry (carry-out) bits, using 3 temporary bits to store intermediate results.

Every bit has the same HTML structure, but a unique CSS animation that places either the moving bit or
its static pause region under the mouse cursor, and sets the proper z-index for reading or writing at
each time step.

### Operations on one bit:<br>
Set to 0 (hover right for a "tick" or left for a "tock")<br>
Set to 1 (hover left for a "tick" or right for a "tock")<br>
Invert (hover pause for either a "tick" or a "tock")<br>

### Operations on two bits, using the 2nd bit as output:<br>
**Copy**: Hover read bit's left or right output over the same side of the write bit's input for a full "tick-tock" cycle).<br>
**XOR**: Hover read bit's left output over write bit's pause for a "tick" or read bit's right output over write bit's pause for a "tock".

### Operations on two bits, using a 3rd bit as output:<br>
**AND**: Set output to 0 and invert if both inputs are 1.
**NAND**: Set output to 1 and invert if both inputs are 1.
**OR**: Set output to 1 and invert if both inputs are 0.
**NOR**: Set output to 0 and invert if both inputs are 0.

These can be chained together to create any fixed Boolean circuit.

### Halting State
A "Halt" button can be moved underneath the mouse cursor, with one or more read bits underneath,
to halt the program once a stop condition is reached.

# Operations
Write left:
```css
top: var(--accept-input-top); left: var(--active-left); z-index: var(--accept-input-z);
```
Write right:
```css
top: var(--accept-input-top); left: var(--active-right); z-index: var(--accept-input-z);
```
Write pause:
```css
top: var(--accept-input-top); left: var(--active-pause); z-index: var(--accept-input-z); 
```

Read left:
```css
top: var(--perform-output-top); left: var(--active-left); z-index: var(--perform-output-z);
```
Read right:
```css
top: var(--perform-output-top); left: var(--active-right); z-index: var(--perform-output-z); 
```

Most operations are different during a "tick" cycle from a "tock" cycle, swapping right and left positioning.
## TICK

During a "0" half-cycle (tick):<br>
A 0 is left  (blocks left,  permits right)<br>
A 1 is right (blocks right, permits left)

To set 0, position the right write box under the cursor, a 0 will be unaffected and a 1 will be delayed
```css
left: var(--active-right); top: var(--accept-input-top); z-index: var(--accept-input-z);
```

To set 1, position the left write box under the cursor
```css
left: var(--active-left); top: var(--accept-input-top); z-index: var(--accept-input-z);
```

XOR is left over pause 
```css
left: var(--active-left); top: var(--perform-output-top); z-index: var(--perform-output-z);
```

AND is set receiver to 0 on tock, then<br>
both inputs 1 activate pause (left over) inverts if both are 1
```css
left: var(--active-left); top: var(--perform-output-top); z-index: var(--perform-output-z);
```

OR is set receiver to 1 on tock, then<br>
both inputs 0 activate pause (right over) inverts if both are 0
```css
left: var(--active-right); top: var(--perform-output-top); z-index: var(--perform-output-z);
```

## TOCK

During a "1" half-cycle (tock):<br>
A 1 is left  (blocks left,  permits right)<br>
A 0 is right (blocks right, permits left)

To set 0
```css
left: var(--active-left); top: var(--accept-input-top); z-index: var(--accept-input-z);
```

To set 1
```css
left: var(--active-right); top: var(--accept-input-top); z-index: var(--accept-input-z); 
```

XOR is right over pause
```css
left: var(--active-right); top: var(--perform-output-top); z-index: var(--perform-output-z); 
```

AND is set receiver 0 on tick, then<br>
both inputs 1 activate pause (right over) inverts if both are 1
```css
left: var(--active-right); top: var(--perform-output-top); z-index: var(--perform-output-z); 
```

OR is set receiver to 1 on tick, then<br>
both inputs 0 activate pause (left over) inverts if both are 0
```css
left: var(--active-left); top: var(--perform-output-top); z-index: var(--perform-output-z);
```
