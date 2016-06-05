def str2bs(s):
    """
    Convert string to 8 bits binary bit stream
    :param s: A string
    :return: 1D bit stream
    """
    result = [bin(ord(ch))[2:].zfill(8) for ch in s]
    return ''.join(result)

def replace_lsb(i, b):
    """
    Change the last bit of integer i to b
    :param i: An integer number
    :param b: Bit number 1 or 0
    :return: Integer number after changing last bit of i
    """
    result = i | int(b) if int(b) == 1 else i & 0xfe
    return result

def bs2img(s):
    """
    Get RGB values from input bit stream
    :param s: Bit stream
    :return: RGB tuples
    """
    if len(s) % 24 != 0:
        print('Invalid bit stream!')
        raise StopIteration

    vals = [int(s[i:i+8], 2) for i in range(0, len(s), 8)]
    pxs = [(vals[i], vals[i+1], vals[i+2]) for i in range(0, len(vals), 3)]
    return pxs

def bs2str(s):
    """
    Get text string from input bit stream
    :param s: Bit stream of a string
    :return: String
    """
    if len(s) % 8:
        print('Invalid bit stream!')
        raise ValueError

    result = [chr(int(s[i:i+8], 2)) for i in range(0, len(s), 8)]
    return ''.join(result)