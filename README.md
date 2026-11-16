# RISC-V RV32I Assembler & Simulator

A modular, lightweight assembler and cycle-by-cycle simulator for a custom subset of the **RISC-V (RV32I 32-bit Integer)** Instruction Set Architecture, implemented in Python.

---

## 📌 Project Overview

This project implements an end-to-end toolchain to parse, encode, and execute programs on a custom subset of the **RV32I** instruction set. Developed as part of a Computer Organization (CO) engineering curriculum, it bridges the gap between high-level assembly programming and architectural hardware execution.

### Key Components

- **SimpleAssembler (`SimpleAssembler/`)**: Translates human-readable RISC-V assembly code into 32-bit binary machine instructions. Features two-pass label resolution, immediate range checking, syntax verification, and Virtual Halt validation.
- **SimpleSimulator (`SimpleSimulator/`)**: Simulates the execution of assembled binary programs cycle by cycle. Tracks the Program Counter (PC), all 32 architectural registers, and simulated memory spaces (Program, Stack, and Data). Outputs execution traces and post-halt memory state dumps.
- **Automated Testing Suite (`automatedTesting/`)**: Test harness covering error generation (`ErrorGen`), basic instruction tests (`simpleBin`), and complex programs (`hardGen`).

---

## 🛠️ Supported Instruction Set (RV32I Subset)

| Type | Instruction | Syntax / Operation | Description |
|---|---|---|---|
| **R-Type** | `add` | `add rd, rs1, rs2` | Addition (`rd = rs1 + rs2`) |
| | `sub` | `sub rd, rs1, rs2` | Subtraction (`rd = rs1 - rs2`) |
| | `slt` | `slt rd, rs1, rs2` | Set Less Than (signed comparison) |
| | `sltu` | `sltu rd, rs1, rs2` | Set Less Than Unsigned |
| | `xor` | `xor rd, rs1, rs2` | Bitwise XOR (`rd = rs1 ^ rs2`) |
| | `sll` | `sll rd, rs1, rs2` | Shift Left Logical (`rd = rs1 << rs2[4:0]`) |
| | `srl` | `srl rd, rs1, rs2` | Shift Right Logical (`rd = rs1 >> rs2[4:0]`) |
| | `or` | `or rd, rs1, rs2` | Bitwise OR (`rd = rs1 \| rs2`) |
| | `and` | `and rd, rs1, rs2` | Bitwise AND (`rd = rs1 & rs2`) |
| **I-Type** | `addi` | `addi rd, rs1, imm` | Add Immediate (`rd = rs1 + sext(imm)`) |
| | `sltiu` | `sltiu rd, rs1, imm` | Set Less Than Immediate Unsigned |
| | `lw` | `lw rd, imm(rs1)` | Load 32-bit Word from memory into register |
| | `jalr` | `jalr rd, rs1, imm` | Jump and Link Register (`rd = PC + 4; PC = (rs1 + imm) & ~1`) |
| **S-Type** | `sw` | `sw rs2, imm(rs1)` | Store 32-bit Word from register into memory |
| **B-Type** | `beq` | `beq rs1, rs2, label` | Branch if Equal |
| | `bne` | `bne rs1, rs2, label` | Branch if Not Equal |
| | `blt` | `blt rs1, rs2, label` | Branch if Less Than (signed) |
| | `bge` | `bge rs1, rs2, label` | Branch if Greater than or Equal (signed) |
| | `bltu` | `bltu rs1, rs2, label` | Branch if Less Than Unsigned |
| | `bgeu` | `bgeu rs1, rs2, label` | Branch if Greater than or Equal Unsigned |
| **U-Type** | `lui` | `lui rd, imm` | Load Upper Immediate (`rd = imm << 12`) |
| | `auipc` | `auipc rd, imm` | Add Upper Immediate to PC (`rd = PC + (imm << 12)`) |
| **J-Type** | `jal` | `jal rd, label` | Jump and Link (`rd = PC + 4; PC += offset`) |

### Virtual Halt
Programs terminate using the **Virtual Halt** instruction:
```assembly
beq zero, zero, 0
```
- **Binary representation:** `00000000000000000000000001100011`
- The assembler verifies that Virtual Halt is present and positioned as the terminating instruction.

---

## 📋 Register Architecture

The processor implements 32 general-purpose 32-bit registers. Both standard ABI names and raw register identifiers (`x0`–`x31`) are supported:

| Register | ABI Name | Role | Saver |
|---|---|---|---|
| `x0` | `zero` | Hardwired constant 0 | — |
| `x1` | `ra` | Return address | Caller |
| `x2` | `sp` | Stack pointer (starts at `0x0000017C`) | Callee |
| `x3` | `gp` | Global pointer | — |
| `x4` | `tp` | Thread pointer | — |
| `x5`–`x7` | `t0`–`t2` | Temporary registers | Caller |
| `x8` | `s0`/`fp` | Saved register / Frame pointer | Callee |
| `x9` | `s1` | Saved register | Callee |
| `x10`–`x17` | `a0`–`a7` | Function arguments / Return values | Caller |
| `x18`–`x27` | `s2`–`s11` | Saved registers | Callee |
| `x28`–`x31` | `t3`–`t6` | Temporary registers | Caller |

---

## 💾 Memory Layout

| Memory Region | Address Range | Size / Capacity | Purpose |
|---|---|---|---|
| **Program Memory** | `0x00000000` – `0x000000FF` | 256 B (64 instructions) | Stores 32-bit assembled machine instructions |
| **Stack Memory** | `0x00000100` – `0x0000017F` | 128 B (32 words) | Stack frame space (grows downward from `sp = 0x0000017C`) |
| **Data Memory** | `0x00010000` – `0x0001007F` | 128 B (32 words) | Read/write memory for `lw` and `sw` instructions |

---

## 📂 Repository Structure

```text
├── SimpleAssembler/
│   ├── Assembler.py          # Assembler: tokenization, syntax validation, binary emission
│   └── README.md
├── SimpleSimulator/
│   └── Simulator.py          # Simulator: cycle execution, register trace & memory dumper
├── automatedTesting/         # Automated grading and test harness
│   └── README.md
├── assignment details.pdf    # Complete specification and ISA assignment documentation
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher.

### 1. Assembling a Program
Run the assembler by providing an assembly input file and a target binary output file:

```bash
python3 SimpleAssembler/Assembler.py <input_assembly_file> <output_binary_file>
```

- **Input:** Plaintext file containing valid RISC-V assembly instructions and labels.
- **Output:** File containing 32-bit binary instructions (one per line).
- **Error Diagnostics:** In case of syntax errors, invalid registers, undefined labels, or missing Virtual Halt, descriptive errors with line numbers are printed to standard output.

### 2. Simulating Execution
Execute an assembled binary file with the simulator:

```bash
python3 SimpleSimulator/Simulator.py <input_binary_file> <output_trace_file>
```

- **Input:** Binary instruction text file produced by the assembler.
- **Output:** Trace file containing:
  1. **Cycle State Traces:** On each cycle, writes the PC and all 32 registers in binary format:
     ```text
     {PC} {x0} {x1} {x2} ... {x31}
     ```
  2. **Memory Dump:** After encountering Virtual Halt, outputs the 32 data memory locations (`0x00010000` to `0x0001007C`) with their 32-bit values:
     ```text
     0x00010000:0b00000000000000000000000000000000
     ...
     ```

---

## 🧪 Testing & Validation

The test suite in `automatedTesting/` includes:
- **`ErrorGen`**: Validates assembler rejection and error reporting on syntactically invalid input.
- **`simpleBin`**: Validates basic arithmetic, logical, and memory operations.
- **`hardGen`**: Validates complex control flow, subroutines (`jal`/`jalr`), recursion, and stack manipulation.

---

## 👥 Contributors

- **Divyansh Garg** ([@divyanshgargofficial-beep](https://github.com/divyanshgargofficial-beep))
- **Aariz** ([@aariz25311](https://github.com/aariz25311))
- **Kunal Martolia** ([@Kunal-Dafuq](https://github.com/Kunal-Dafuq))
- **haraloo** ([@haraloo](https://github.com/haraloo))
