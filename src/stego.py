from PIL import Image
import math
import datetime

def str2bs(s):
    """
    Convert string to bit stream
    :param s: A string
    :return: 1D bit stream
    """
    result = [bin(ord(ch))[2:].zfill(8) for ch in s]
    return ''.join(result)

def dec2bs(n):
    """
    Convert decimal to bit stream
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
    else:
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
    # Variables declaration and initialization
    # c_img = Image.open(cover_img)
    # pxs = list(c_img.getdata())

    # # Get hidden information bit stream
    # hid_bs = get_bs_img(hid_img) + str2bs(hid_text)

    # # Get secret key bit stream
    # sec_bs = str2bs(sec_key)

    # if len(pxs) < len(hid_bs):
    #     return False

    # print('Number of Pixels in Cover Image:', len(pxs))
    # print('Length of Hidden Information:', len(hid_bs))

    # # s XOR r
    # cnt = 0
    # len_sec_bs = len(sec_bs)

    # while cnt < len(hid_bs):
    #     idx = cnt % len_sec_bs
    #     px = pxs[cnt]
    #     lsb_cr = px[0] & 1
    #     xor = lsb_cr ^ int(sec_bs[idx])

    #     # 1
    #     # Replace LSB of Green by 1 bit hidden information
    #     if xor == 1:
    #         pxs[cnt] = (px[0], replace_lsb(px[1], int(hid_bs[cnt])), px[2])

    #     # 0
    #     # Replace LSB of Blue by 1 bit hidden information
    #     else:
    #         pxs[cnt] = (px[0], px[1], replace_lsb(px[2], int(hid_bs[cnt])))
    #     cnt += 1

    # return pxs


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


def enc_info_2(cover_img, hid_img, hid_text, sec_key):
    """
    Encrypt image and/or text into cover image.
    With this method the hidden image and text bits are hidden in the same pixels of cover image.
    :param cover_img: Path of cover image
    :param hid_img: Path of hidden image
    :param hid_text: Value of hidden text
    :param sec_key: Value of secret key
    :return: RGB values(Pixels) of Stego image
    """
    # Variables declaration and initialization
    c_img = Image.open(cover_img)
    pxs = list(c_img.getdata())

    # Get hidden information bit stream
    hid_img_bs = get_bs_img(hid_img)
    hid_text_bs = str2bs(hid_text)
    len_hid_bs = max(len(hid_text_bs), len(hid_img_bs))

    # Get secret key bit stream
    sec_bs = str2bs(sec_key)

    print('Number of Pixels in Cover Image:', len(pxs))
    print('Length of Hidden Information:', len_hid_bs)

    if len(pxs) < len_hid_bs:
        return False

    # Generate new pixels after encrypting hidden information into cover image
    pxs = gen_new_pxs(pxs, sec_bs, hid_img_bs, hid_text_bs) if len(hid_img_bs) == len_hid_bs \
        else gen_new_pxs(pxs, sec_bs, hid_text_bs, hid_img_bs)

    return pxs


def gen_new_pxs(pxs, sec_bs, hid_bs_lg, hid_bs_sh):
    """
    Generate new pixel RGB values based on hidden information.
    This function is used to avoid duplicate code in enc_info_2 while doing bit replacement
    since it's not sure which hidden information is longer, image or text.
    :param pxs: RGB values of cover image pixels
    :param sec_bs: Secret key string
    :param hid_bs_lg: The longer hidden bit stream, image/text
    :param hid_bs_sh: The shorter hidden bit stream, image/text
    :return: RGB values after embedding hidden information
    """
    # s XOR r
    cnt = 0
    len_sec_bs = len(sec_bs)
    len_hid_bs = len(hid_bs_lg)
    len_hid_bs_sh = len(hid_bs_sh)

    while cnt < len_hid_bs:
        idx = cnt % len_sec_bs
        px = pxs[cnt]
        lsb_cr = px[0] & 1
        xor = lsb_cr ^ int(sec_bs[idx])

        # 1
        # Replace LSB of Green by 1 bit hidden information
        if xor == 1:
            if cnt < len_hid_bs_sh:
                pxs[cnt] = (px[0], replace_lsb(px[1], int(hid_bs_lg[cnt])), replace_lsb(px[2], int(hid_bs_sh[cnt])))
            else:
                pxs[cnt] = (px[0], replace_lsb(px[1], int(hid_bs_lg[cnt])), px[2])

        # 0
        # Replace LSB of Blue by 1 bit hidden information
        else:
            if cnt < len_hid_bs_sh:
                pxs[cnt] = (px[0], replace_lsb(px[1], int(hid_bs_sh[cnt])), replace_lsb(px[2], int(hid_bs_lg[cnt])))
            else:
                pxs[cnt] = (px[0], px[1], replace_lsb(px[2], int(hid_bs_lg[cnt])))
        cnt += 1

    return pxs


def dec_info_2(img, hid_img_size, hid_text_size, sec_key):
    """
    Extract the hidden information, image and/or text, from an image.
    This function is opposed to enc_info_2 which embeds hidden image and/or text bits
    into the same pixels in cover image.
    :param img: Stego image
    :param hid_img_size: A tuple representing the size of hidden image, eg. (100, 100)
    :param hid_text_size: Number of characters in hidden text
    :param sec_key: Secret key, usually is a word or sentence
    :return:
    """
    # Open the Stego image
    c_img = Image.open(img)
    pxs = list(c_img.getdata())

    # Get secret key bit stream
    sec_bs = str2bs(sec_key)
    len_sec_bs = len(sec_bs)

    # Get length of hidden image and text bits
    hid_img_len = hid_img_size[0] * hid_img_size[1] * 3 * 8
    hid_text_len = hid_text_size * 8

    # Get hidden bits for image and/or text
    if hid_img_len > hid_text_len:
        hid_img_bs, hid_text_bs = ext_hidden_bits(pxs, sec_bs, hid_img_len, hid_text_len)
    else:
        hid_text_bs, hid_img_bs = ext_hidden_bits(pxs, sec_bs, hid_text_len, hid_img_len)

    return hid_img_bs, hid_text_bs


def ext_hidden_bits(pxs, sec_bs, hid_len_lg, hid_len_sh):
    """
    Extract hidden information based on pixel values.
    This function is used to avoid duplicate code in dec_info_2 while doing bit extraction
    since it's not sure which hidden information is longer, image or text.
    :param pxs: RGB values of cover image pixels
    :param sec_bs: Secret key string
    :param hid_len_lg: The length of longer hidden bit stream, image/text
    :param hid_len_sh: The length of shorter hidden bit stream, image/text
    :return: RGB values after embedding hidden information
    """
    cnt = 0
    len_sec_bs = len(sec_bs)
    hid_bs_lg, hid_bs_sh = '', ''

    for px in pxs[:hid_len_lg]:

        idx = cnt % len_sec_bs
        xor = int(sec_bs[idx]) ^ (px[0] & 1)

        # 1
        # Get LSB of Green and append to 1 bit hidden bit stream
        if xor == 1:
            if cnt < hid_len_sh:
                hid_bs_sh += str(px[2] & 1)
            hid_bs_lg += str(px[1] & 1)

        # 0
        # Get LSB of Blue and append to 1 bit hidden bit stream
        else:
            if cnt < hid_len_sh:
                hid_bs_sh += str(px[1] & 1)
            hid_bs_lg += str(px[2] & 1)
        cnt += 1
    # for px in pxs[:hid_len_lg]:
    #     idx = cnt % len_sec_bs
    #     xor = int(sec_bs[idx]) ^ (px[0] & 1)
    #     if cnt < hid_len_sh:
    #         hid_bs_sh = hid_bs_sh + str(px[2] & 1) if xor == 1 else hid_bs_sh + str(px[1] & 1)
    #     hid_bs_lg = hid_bs_lg + str(px[1] & 1) if xor == 1 else hid_bs_lg + str(px[2] & 1)
    #     print cnt
    #     cnt += 1

    return hid_bs_lg, hid_bs_sh


def cal_mse(img1, img2):
    """
    Calculate Mean Squared Errors between two images
    :param img1: Path of image1
    :param img2: Path of image2
    :return: MSE of two images
    """
    i1, i2 = Image.open(img1), Image.open(img2)
    i1_pxs, i2_pxs = list(i1.getdata()), list(i2.getdata())

    i1_size, i2_size = i1.size, i2.size

    if i1_size != i2_size:
        print('Two images are not the same size!')
        return False

    m, n = i1_size[0], i1_size[1]
    mser, mseg, mseb = 0, 0, 0

    for i in xrange(m*n):
        i1_rgb, i2_rgb = i1_pxs[i], i2_pxs[i]
        i1_r, i1_g, i1_b = i1_rgb[0], i1_rgb[1], i1_rgb[2]
        i2_r, i2_g, i2_b = i2_rgb[0], i2_rgb[1], i2_rgb[2]
        mser += math.pow((i1_r - i2_r), 2)
        mseg += math.pow((i1_g - i2_g), 2)
        mseb += math.pow((i1_b - i2_b), 2)

    mser, mseg, mseb = mser / (m*n), mseg / (m*n), mseb / (m*n)
    mse = (mser + mseg + mseb) / 3

    return mse


def cal_psnr(max_i, mse):
    """
    Calculate the Peak Signal to Noise Ratio
    :param max_i: Max Pixel Intensity Value -- 8 bit is 255
    :param mse: Mean Squared Errors
    :return: PSNR value
    """
    return 10 * math.log10(math.pow(max_i, 2) / mse)

if __name__ == '__main__':

    for i in xrange(1):
        # file_name = 'text_' + str(i*10) + '.txt'
        file_name = 'text_100.txt'
        # img_name = 'Mercedes_' + str(i*10) + '.jpg'
        img_name = 'Mercedes_50.jpg'
        # stego_name = 'stego_' + str(i*10) + '.png'
        stego_name = 'stego.png'
        # output_name = 'output_' + str(i*10) + '.png'
        output_name = 'output.png'
        imgg = Image.open(img_name)
        hid_size = imgg.size
        # hid_size = (0, 0)

        #print 'Hidden Text File: ' + file_name
        #print 'Hidden Image File: ' + img_name
        #print 'Hidden Image Size: ' + str(hid_size)
        #print 'Stego Image File: ' + stego_name
        #print 'Output Image File: ' + output_name

        with open(file_name, 'r') as f:
            ht = f.read()
        f.close()
        # ht = ''
        start_time = datetime.datetime.now()

        img = enc_info_2('Lenna.png', img_name, ht, 'Jimmy')

        if img:
            im = Image.new('RGB', (512, 512))
            im.putdata(img)
            im.save(stego_name)
            hid_im, hid_text = dec_info_2(stego_name, hid_size, len(ht), 'Jimmy')

            if len(hid_im) != 0:
                pxs = list(get_rgb_bs(hid_im))

                im = Image.new('RGB', hid_size)
                im.putdata(pxs)
                im.save(output_name)

            st = ''.join(list(get_text_bs(hid_text)))

            end_time = datetime.datetime.now()
            td = end_time - start_time
            # print td.seconds

            mse = cal_mse('Lenna.png', stego_name)
            max_i = 255
            # print cal_psnr(max_i, mse)
            with open('results.txt', 'a') as f:
                f.write('Hidden Image: ' + str(hid_size) + '\t' + 'Hidden Text Length: ' + str(len(ht)) + '\t' + 'Time: ' +
                        str(td.total_seconds()) + '\t' + 'PSNR: ' + str(cal_psnr(max_i, mse)) + '\n')
            f.close()
        else:
            print('Hidden information is too much!')
