from PIL import Image
import math
import datetime
import argparse

def str2bs(s):
    """
    Convert string to 8 bits binary bit stream
    :param s: A string
    :return: 1D bit stream
    """
    result = [bin(ord(ch))[2:].zfill(8) for ch in s]
    return ''.join(result)

def dec2bs(n):
    """
    Convert decimal to 8 bits binary bit stream
    :param n: A decimal number
    :return: 1D bit stream
    """
    return bin(n)[2:].zfill(8)

def bs2dec(bs):
    """
    Convert binary bit stream to decimal numbers
    """
    if len(bs) % 8:
        raise ValueError
    return int(bs, 2)

def replace_lsb(i, b):
    """
    Change the last bit of integer i to b
    :param i: An integer number
    :param b: Bit number 1 or 0
    :return: Integer number after changing last bit of i
    """
    result = i | b if b == 1 else i ^ 1
    return result


def get_rgb(img):
    """
    Get RGB values of an image
    :param img: image file name
    :return: RGB values in decimal
    """
    # Get RGB values of cover image
    pxs = img.getdata()
    r_mtx, g_mtx, b_mtx = [], [], []

    # Convert RGB values from decimal to binary
    for px in pxs:
        r_mtx.append(px[0])
        g_mtx.append(px[1])
        b_mtx.append(px[2])

    return r_mtx, g_mtx, b_mtx


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


def img2bs(pxs):
    """
    Get the bit string of the input image
    :param img: Path of image file
    :return: Bit string of the input image
    """
    result = [dec2bs(val) for px in pxs for val in px]
    return ''.join(result)

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


def enc_info(cover_img, hid_img, hid_text, sec_key):
    """
    Encrypt image and/or text into cover image serially.
    With this method, hidden image and hidden text bit streams are concatenated before being encrypted.
    :param cover_img: Path of cover image
    :param hid_img: Path of hidden image
    :param hid_text: Value of hidden text
    :param sec_key: Value of secret key
    :return: RGB values(Pixels) of Stego image
    """
    cimg = Image.open(cover_img)
    cov_pxs = cimg.getdata()

    # hidden text cannot be longer than the number of pixels in cover image
    if len(hid_text) * 8 > len(cov_pxs):
        raise ValueError

    # get pixels of images
    himg = Image.open(hid_img)
    hid_pxs = himg.getdata()

    # the number of pixels in hidden image cannot exceed one third of the number of pixels in cover image
    if len(hid_pxs) * 3 * 8 > len(cov_pxs):
        raise ValueError

    ht_bs = str2bs(hid_text)
    hm_bs = img2bs(hid_pxs)

    hid_lg_bs, hid_sh_bs = hm_bs, ht_bs
    if len(hid_text) > len(hid_pxs) * 3:
        hid_lg_bs, hid_sh_bs = ht_bs, hm_bs

    len_lg_bs = len(hid_lg_bs)
    len_hm_bs = len(hid_sh_bs)

    # convert secure key to binary bit stream
    sk_bs = str2bs(sec_key)
    len_sk_bs, i = len(sec_key), 0

    ret = []
    for px in cov_pxs:
        new_gpx, new_bpx = px[1], px[2]
        if px[0] ^ sk_bs[i % len_sk_bs]:
            new_gpx = replace_lsb(px[1], hid_lg_bs[i])
            if i >= len(hid_sh_bs):
                new_bpx = replace_lsb(px[2], hid_sh_bs[i])

        else:
            new_bpx = replace_lsb(px[2], hid_lg_bs[i])
            if i >= len(hid_sh_bs):
                new_gpx = replace_lsb(px[1], hid_sh_bs[i])
        ret.append((px[0], new_gpx, new_bpx))
        i += 1
    return ret