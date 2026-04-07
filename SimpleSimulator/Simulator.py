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