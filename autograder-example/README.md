# Autograder example
This is an example of a grading script for simple combinational circuits. It should be used for testing the outputs for all possible inputs.

If the assignment requires loading data into a ROM and more closely reflects a sequential circuit, check out the other subfolder.
TODO: make the subfolder and link it.

# Prerequisites
* The following should be clearly described in the lab instructions:
    + The number of data bits for inputs and outputs
    + The orientation of input and output (facing West/North/etc.)
    + The order of inputs and outputs in the circuit appearance (see [The inputs section](#the-inputs) below)

# How to use
You may find it useful to read the [Description of this example section](#description-of-this-example) first to understand the various files needed and how they're used.

TODO: describe the necessary directory/file structure, the arguments to the script, creating a "main-tester" and "key" circuit files, the result of running the program (student outputs and report which could be changed since right now it's either the output matches or it doesn't), ... (also setting "defaults")

## Script
TODO

### Arguments and Default
TODO

### Results
TODO

## Creating a main tester
TODO

## The correct circuit
TODO

### Create the correct circuit
TODO

### Load the correct circuit
TODO

# Description of this example
TODO?

## The files
TODO

## The assignment
The fake assignment in this example is to create a circuit that takes in three 2-bit inputs (A, B, C) and output a two-bit result that corresponds to `AB$\neg$C + $\neg\ABC`.

### The inputs
While the inputs can be labelled whatever, the order of the inputs matter. Specifically, the order of the inputs in the [circuit appearance](http://www.cburch.com/logisim/docs/2.7/en/html/guide/subcirc/appear.html) is important.

They should be the same as how the `correct-circuit.circ` file is used in `main-tester.circ` file.

Changing the order of inputs in the appearance seems to make an impact, and can be shown by students H and I. The distance between inputs and the size might also matter (students J and K), but has not been extensively tested.

Therefore, it is generally recommended that students do not modify the main circuit's appearance and make sure the order of the inputs and the outputs are correct.

Note: the upper most input components are higher up in the circuit's appearance - if they are at the same vertical level in Logisim, then left most input components are higher up.

### Main tester circuit
TODO

### Intermediate path
TODO