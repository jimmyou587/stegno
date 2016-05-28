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
    cov_pxs = cover_img.getdata()

    # hidden text cannot be longer than the number of pixels in cover image
    if len(hid_text) * 8 > len(cov_pxs):
        raise ValueError

    # get pixels of images
    hid_pxs = hid_img.getdata()

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
        if px[0] ^ ord(sk_bs[i % len_sk_bs]):
            new_gpx = replace_lsb(px[1], int(hid_lg_bs[i]))
            if i < len(hid_sh_bs):
                new_bpx = replace_lsb(px[2], int(hid_sh_bs[i]))

        else:
            new_bpx = replace_lsb(px[2], int(hid_lg_bs[i]))
            if i < len(hid_sh_bs):
                new_gpx = replace_lsb(px[1], int(hid_sh_bs[i]))
        ret.append((px[0], new_gpx, new_bpx))
        i += 1
        if i >= len_lg_bs:
            break
    return ret + list(cov_pxs)[i:]

def dec_info(img, sec_key):
    """
    Extract the hidden information, image and/or text, from an image
    :param img: Cover image
    :param hid_img_size: A tuple representing the size of hidden image, eg. (100, 100)
    :param hid_text_size: Number of characters in hidden text
    :param sec_key: Secret key, usually is a word or sentence
    :return:
    """
    # Open the Stego image
    # c_img = Image.open(img)
    # pxs = list(c_img.getdata())

    # # Get secret key bit stream
    # sec_bs = str2bs(sec_key)
    # len_sec_bs = len(sec_bs)

    # cnt = 0
    # hid_bs = ''
    # hid_img_len = hid_img_size[0] * hid_img_size[1] * 3 * 8
    # hid_text_len = hid_text_size * 8
    # hid_len = hid_img_len + hid_text_len

    # while cnt < hid_len:

    #     idx = cnt % len_sec_bs
    #     px = pxs[cnt]
    #     xor = int(sec_bs[idx]) ^ (px[0] & 1)

    #     # 1
    #     # Get LSB of Green and append to 1 bit hidden bit stream
    #     if xor == 1:
    #         hid_bs += str(px[1] & 1)

    #     # 0
    #     # Get LSB of Blue and append to 1 bit hidden bit stream
    #     else:
    #         hid_bs += str(px[2] & 1)
    #     cnt += 1

    # hid_img, hid_text = hid_bs[:hid_img_len], hid_bs[hid_img_len:]

    # return hid_img, hid_text
    return ((1,2))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='Path of cover image')
    parser.add_argument('-s', help='Secure key')
    parser.add_argument('-hi', help='Path of hidden image')
    parser.add_argument('-ht', help='Path of hidden text file')

    args = parser.parse_args()

    cover_img, hid_img, sec_key = Image.open(args.c), Image.open(args.hi), args.s
    with open(args.ht) as ht_file:
        hid_text = ht_file.read().strip()

    new_pxs = enc_info(cover_img, hid_img, hid_text, sec_key)
    img = Image.new('RGB', cover_img.size)
    img.putdata(new_pxs)
    img.save('-'.join([args.c.split('.')[0], 'new', '.png']))

    # for i in xrange(1):
    #     # file_name = 'text_' + str(i*10) + '.txt'
    #     file_name = 'text_100.txt'
    #     # img_name = 'Mercedes_' + str(i*10) + '.jpg'
    #     img_name = 'Mercedes_50.jpg'
    #     # stego_name = 'stego_' + str(i*10) + '.png'
    #     stego_name = 'stego.png'
    #     # output_name = 'output_' + str(i*10) + '.png'
    #     output_name = 'output.png'
    #     imgg = Image.open(img_name)
    #     hid_size = imgg.size
    #     # hid_size = (0, 0)

    #     #print 'Hidden Text File: ' + file_name
    #     #print 'Hidden Image File: ' + img_name
    #     #print 'Hidden Image Size: ' + str(hid_size)
    #     #print 'Stego Image File: ' + stego_name
    #     #print 'Output Image File: ' + output_name

    #     with open(file_name, 'r') as f:
    #         ht = f.read()
    #     f.close()
    #     # ht = ''
    #     start_time = datetime.datetime.now()

    #     img = enc_info_2('Lenna.png', img_name, ht, 'Jimmy')

    #     if img:
    #         im = Image.new('RGB', (512, 512))
    #         im.putdata(img)
    #         im.save(stego_name)
    #         hid_im, hid_text = dec_info_2(stego_name, hid_size, len(ht), 'Jimmy')

    #         if len(hid_im) != 0:
    #             pxs = list(get_rgb_bs(hid_im))

    #             im = Image.new('RGB', hid_size)
    #             im.putdata(pxs)
    #             im.save(output_name)

    #         st = ''.join(list(get_text_bs(hid_text)))

    #         end_time = datetime.datetime.now()
    #         td = end_time - start_time
    #         # print td.seconds

    #         mse = cal_mse('Lenna.png', stego_name)
    #         max_i = 255
    #         # print cal_psnr(max_i, mse)
    #         with open('results.txt', 'a') as f:
    #             f.write('Hidden Image: ' + str(hid_size) + '\t' + 'Hidden Text Length: ' + str(len(ht)) + '\t' + 'Time: ' +
    #                     str(td.total_seconds()) + '\t' + 'PSNR: ' + str(cal_psnr(max_i, mse)) + '\n')
    #         f.close()
    #     else:
    #         print('Hidden information is too much!')
