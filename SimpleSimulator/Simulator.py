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