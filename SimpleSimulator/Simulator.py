import sys


def extract_paths():
    try:
        return sys.argv[1], sys.argv[2]
    except:
        raise Exception("Input/output paths not provided correctly")


def binarycheck(binarystring):
    for inst in binarystring:
        if len(inst) != 32:
            raise ValueError(f"Invalid instruction length: {len(inst)}='{inst}'")
        for bit in inst:
            if bit not in ("0", "1"):
                raise ValueError(f"Invalid bit: '{bit}'")


#helper function
def sign_extend(val, bits):
    if val&(1<<(bits-1)):
        val-=(1<<bits)
    return val


def to_32bit(x):
    return x&0xFFFFFFFF


def to_signed(x):
    if x&0x80000000:
        return x-(1<<32)
    return x


def to_bin(x):
    return "0b" + format(x&0xFFFFFFFF,"032b")

#instruction decode dictionary
instr_type = {
    "0110011": {  # R-type
        "format": "R",
        "instructions": {
            ("000", "0000000"): "add",
            ("000", "0100000"): "sub",
            ("111", "0000000"): "and",
            ("110", "0000000"): "or",
            ("100", "0000000"): "xor",
            ("001", "0000000"): "sll",
            ("101", "0000000"): "srl",
            ("101", "0100000"): "sra",
            ("010", "0000000"): "slt",
            ("011", "0000000"): "sltu",
        }
    },

    "0010011": {  # I-type
        "format": "I",
        "instructions": {
            "000": "addi",
            "111": "andi",
            "110": "ori",
            "100": "xori",
            "010": "slti",
            "011": "sltiu",
            "001": "slli",
            "101": "shifti"
        }
    },

    "0000011": {"format": "LOAD"},
    "0100011": {"format": "STORE"},
    "1100011": {"format": "B"},
    "1101111": {"format": "J"},
    "1100111": {"format": "JALR"},
    "0110111": {"format": "LUI"},
    "0010111": {"format": "AUIPC"},
}



def execute(instr, registers, memory, PC):
    opcode = instr[25:32]
    funct3 = instr[17:20]
    funct7 = instr[0:7]

    rd  = int(instr[20:25], 2)
    rs1 = int(instr[12:17], 2)
    rs2 = int(instr[7:12], 2)

    next_PC = PC + 4

    entry = instr_type.get(opcode)
    if not entry:
        return next_PC

    format_type=entry["format"]

    # R TYPE 
    if format_type=="R":
        name=entry["instructions"].get((funct3, funct7))

        if name=="add":
            registers[rd]=to_32bit(registers[rs1] + registers[rs2])

        elif name == "sub":
            registers[rd] = to_32bit(registers[rs1] - registers[rs2])

        elif name == "and":
            registers[rd] = to_32bit(registers[rs1] & registers[rs2])

        elif name == "or":
            registers[rd] = to_32bit(registers[rs1] | registers[rs2])

        elif name == "xor":
            registers[rd] = to_32bit(registers[rs1] ^ registers[rs2])

        elif name == "sll":
            registers[rd] = to_32bit(registers[rs1] << (registers[rs2] & 0x1F))
        elif name == "sra":
            registers[rd] = to_32bit(to_signed(registers[rs1]) >> (registers[rs2] & 0x1F))

        elif name == "slt":
            registers[rd] = int(to_signed(registers[rs1]) < to_signed(registers[rs2]))

        elif name == "sltu":
            registers[rd] = int(registers[rs1] < registers[rs2])

        elif name == "srl":
            registers[rd] = (registers[rs1] & 0xFFFFFFFF) >> (registers[rs2] & 0x1F)



    #I TYPE
    elif format_type == "I":
        imm = sign_extend(int(instr[0:12], 2), 12)
        name = entry["instructions"].get(funct3)

        if name == "addi":
            registers[rd] = to_32bit(registers[rs1] + imm)

        elif name == "andi":
            registers[rd] = to_32bit(registers[rs1] & imm)

        elif name == "ori":
            registers[rd] = to_32bit(registers[rs1] | imm)

        elif name == "xori":
            registers[rd] = to_32bit(registers[rs1] ^ imm)

        elif name == "slti":
            registers[rd] = int(to_signed(registers[rs1]) < imm)

        elif name == "sltiu":
            registers[rd] = int(registers[rs1] < (imm & 0xFFFFFFFF))

        elif name == "slli":
            shamt = int(instr[7:12], 2)
            registers[rd] = to_32bit(registers[rs1] << (shamt & 0x1F))

        elif name == "shifti":
            shamt = int(instr[7:12], 2)
            if funct7 == "0000000":
                registers[rd] = (registers[rs1] & 0xFFFFFFFF) >> (shamt & 0x1F)
            elif funct7 == "0100000":
                registers[rd] = to_32bit(to_signed(registers[rs1]) >> (shamt & 0x1F))

        #U TYPE
    elif format_type == "LUI":
        registers[rd] = to_32bit(int(instr[0:20], 2) << 12)

    elif format_type == "AUIPC":
        registers[rd] = to_32bit(PC + (int(instr[0:20], 2) << 12))      

#BRANCH
    elif format_type == "B":
        imm = sign_extend(
            int(instr[0] + instr[24] + instr[1:7] + instr[20:24] + "0", 2), 13
        )
        elif funct3 == "001" and to_signed(registers[rs1]) != to_signed(registers[rs2]):
            next_PC = PC + imm
        if funct3 == "000" and to_signed(registers[rs1]) == to_signed(registers[rs2]):
            next_PC = PC + imm


    #JUMP
    elif format_type == "J":
        imm = sign_extend(
            int(instr[0] + instr[12:20] + instr[11] + instr[1:11] + "0", 2), 21
        )
        registers[rd] = to_32bit(PC + 4)
        next_PC = PC + imm

    elif format_type == "JALR":
        imm = sign_extend(int(instr[0:12], 2), 12)
        registers[rd] = to_32bit(PC + 4)
        next_PC = (registers[rs1] + imm) & ~1



    registers[0] = 0
    return next_PC

    #LOA
    elif format_type == "LOAD":
        imm = sign_extend(int(instr[0:12], 2), 12)
        addr = to_32bit(registers[rs1] + imm)
        registers[rd] = to_32bit(memory.get(addr, 0))

    #STORE 
    elif format_type == "STORE":
        imm=sign_extend(int(instr[0:7] + instr[20:25], 2), 12)
        addr=to_32bit(registers[rs1] + imm)
        memory[addr]=to_32bit(registers[rs2])

def main():
    input_path, output_path = extract_paths()

    raw_lines = []
    with open(input_path, "r") as f:
        for line in f:
            for token in line.split():
                token = token.strip()
                if token.startswith("0b") or token.startswith("0B"):
                    token = token[2:]
                if token:
                    raw_lines.append(token)

    binarycheck(raw_lines)

    registers = [0] * 32
    registers[2] = 0x17C
    memory = {}
    PC = 0

    with open(output_path, "w") as out:
        while PC < len(raw_lines) * 4:
            instr = raw_lines[PC // 4]
            PC = execute(instr, registers, memory, PC)

            line = [to_bin(PC)] + [to_bin(r) for r in registers]
            out.write(" ".join(map(str, line)) + "\n")

            # halt condition
            if instr == "00000000000000000000000001100011":
                break

        for addr in range(0x00010000, 0x00010080, 4):
            val = memory.get(addr, 0)
            out.write(f"0x{addr:08X}:{to_bin(val)}\n")


if __name__ == "__main__":
    main()

