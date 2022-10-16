OLAFv2 Processor
================

OLAFv2 is a virtual [CPU](https://en.wikipedia.org/wiki/Central_processing_unit), emulated over a program called [Logisim](http://www.cburch.com/logisim/), running a custom [Operating System](https://en.wikipedia.org/wiki/Operating_system) that compiled with a special [Assembler](https://en.wikipedia.org/wiki/Assembly_language#Assembler).

This project is an educational project, which is used to give an intuition on how CPUs could work.
Note: this chip is differently from other (and real) CPUs. when I did my research around this project, I tried to only get an intuition about how a processor could work, and I tried to design a CPU that will work internally different from other real life CPUs.

I hope you will find this project entertaining and educational as much as I did.

![OLAFv2CPU](https://raw.githubusercontent.com/itaysaadia/OLAFv2-CPU/master/.github/images/OLAF.png)

Overview
--------

The code is divided to 3 parts:

* The CPU itself
* Am assembler for OLAFv2's assembly
* Basic Operating System written in OLAFv2's assembly

How to run
--------

### Compile the OS

from the top folder, run `python3 ./Assembler/assembler.py`
the output should go to `OS/BOOT.rom` and `OS/initram.ram`
### Loading the OS into the machine

To emulate the CPU, you should download [Logisim](http://www.cburch.com/logisim/ "Click here to download Logisim!").
Once downloaded, load the `CPU/olaf2.circ` to Logisim with `File->Open`.

Then, press with the right click on the ROM (the block behind the CPU) and press `Load Image...` and select the newly compiled `OS/BOOT.rom`. The rom should be filled with hexadecimal numbers.
Load the RAM (the block behind the ROM) the same way, but now load the file `OS/initram.ram`

### Starting the CPU

So everything is loaded now and it's time to start the simulation. In Logisim, under Simulate (on the top bar), change the `Tick frequency` to 256Hz or above.

Then Press `Ctrl+K` or `Simulation -> Ticks Enabled`

**Good Luck!**
