# Not possible to script with ROM and RAM?

## Attempts

Since the command line verification requires an output labelled "halt", all of the below file have "halt" in them but are not mentioned further.

### Data for Loading
For the dataset, a simple text file [`data.txt`](./data.txt) containing the [data from the Logisim docs](http://www.cburch.com/logisim/docs/2.7/en/html/guide/mem/menu.html) were used.

### rom-example.circ
#### Description
The `rom-example.circ` file contains a simple counter, clock, ROM, and output.

#### Result
Running `java -jar ../logisim-generic-2.7.1.jar rom-example.circ -tty table -load data.txt` gives the following output:
`No RAM was found for the "-load" option.`

### RAM.circ and main-checker.circ
Since the ROM doesn't allow loading in command line, I entertained the idea of possibly making the instruction memory be RAM instead of ROM. Though not ideal, being able to script the instruction set would mean it would be possible to test various different instructions without having to open and set the data in the circuit.

#### Description
The `RAM.circ` file contains a counter, a RAM component, a clock, and the output of RAM.
The `main-checker.circ` file uses the `RAM.circ` file as the loaded library, but has additional components such as HEX displays and an output testing whether the RAM output is zero.

#### Result
Each file was ran with the following commands:
`java -jar ../logisim-generic-2.7.1.jar {file-name}.circ -tty table -load data.txt`
`java -jar ../logisim-generic-2.7.1.jar {file-name}.circ -load data.txt -tty table`

The output for the RAM read is the following:
```
    0000 0000
    0000 0011
    0000 0000
    0001 0100
    1111 0000
    1111 1111
```

As visible in [`data.txt`](./data.txt), the first address in memory should be 2 and not 0. The output that checks whether the RAM read is zero gives 1 from `main-checker.circ`, implying that the circuit will behave as if the first address is 0 rather than what we load. The hex displays are not included in the circuit output.

This seems to be a [known bug](https://sourceforge.net/p/circuit/bugs/143/) since 2017, and my various attempts at it including trying the [logisim-evolution](https://github.com/reds-heig/logisim-evolution) version does not seem adequate for the purpose of scripting. Just to clarify, the data at the first address being 0 is problematic since it is equivalent to `HALT` in Haverford Educational RISC Architecture (HERA).

Furthermore, the [Logisim docs](http://www.cburch.com/logisim/docs/2.7/en/html/guide/verify/other.html) state that running the command will load the data in every RAM in the circuit and its subcircuits, which may not be ideal.

## Conclusion
Loading into ROM is not allowed, and loading into RAM has critical bugs that would cause bad HERA behavior. Until the bug is resolved or someone finds a work-around, the instructors may have to input the ROM data by hand and run the script.

Fortunately, since the ROM data persists after saving file, the circuit could still be scripted after loading in the data (without substitutions).
<!-- TODO: implement... Use the script in [autograder-example](../autograder-example) with the flag `--nosub`. -->
