import argparse
import math

from PIL import Image

from stego.utility import *

def stege(fp_cover_img, fp_hid_img, fp_hid_text, sec_key):
    """Encrypt image and/or text into cover image serially. With this method, hidden image and hidden text bit streams are concatenated before being encrypted.
    :param fp_cover_img: Path of cover image
    :param fp_hid_img: Path of hidden image
    :param fp_hid_text: Value of hidden text
    :param sec_key: Value of secret key
    """

    if not sec_key:
        raise ValueError('Secure Key is needed!')

    if not fp_hid_img and not fp_hid_text:
        raise ValueError('Nothing to hide!')

    try:
        cimg = Image.open(fp_cover_img)
        cov_pxs = list(cimg.getdata())
    except:
        raise IOError('Can\'t open cover image!')

    # hidden text and image are initialized to empty strings
    hid_img_width, hid_img_height = 0, 0
    hid_pxs = []
    hid_text, ht_bs, hm_bs = '', '', ''

    # encode the size of hidden image and text
    l = math.ceil(math.log(len(cov_pxs)/8, 2))

    if fp_hid_img:
        try:
            with Image.open(fp_hid_img) as himg:
                # get pixels of images
                hid_pxs = [px[:3] for px in himg.getdata()]
                hid_img_width = himg.size[0]
                hid_img_height = himg.size[1]

        except:
            raise IOError('Can\'t open hidden image!')
        else:
            # the number of pixels in hidden image cannot exceed one third of the number of pixels in cover image
            if len(hid_pxs) * 3 * 8 > len(cov_pxs) - l:
                raise ValueError('Hidden image is too big!')
            hm_bs = ''.join([bin(val)[2:].zfill(8) for px in hid_pxs for val in px])

    if fp_hid_text:
        try:
            with open(fp_hid_text) as ht_file:
                hid_text = ht_file.read().strip()
        except:
            raise IOError('Can\'t open hidden text file!')
        else:
            # hidden text cannot be longer than the number of pixels in cover image
            if len(hid_text) * 8 > len(cov_pxs) - l:
                raise ValueError('Hidden text is too long!')
            ht_bs = str2bs(hid_text)

    hm_width_bs = bin(hid_img_width)[2:].zfill(l)
    hm_height_bs = bin(hid_img_height)[2:].zfill(l)
    ht_len_bs = bin(len(hid_text))[2:].zfill(l)

    # ret stores the pixels of encoded cover image
    ret = []
    i = 0

    # hidden image and text sizes are encoded in the first l pixels
    # text size is hidden in red, image size is hidden in blue and green
    for px in cov_pxs[:l]:
        ret.append((replace_lsb(px[0], ht_len_bs[i]), replace_lsb(px[1], hm_width_bs[i]), replace_lsb(px[2], hm_height_bs[i])))
        i += 1

    # encode the content
    hid_lg_bs, hid_sh_bs = hm_bs, ht_bs
    if len(hid_text) > len(hid_pxs) * 3:
        hid_lg_bs, hid_sh_bs = ht_bs, hm_bs

    len_lg_bs = len(hid_lg_bs)
    len_hm_bs = len(hid_sh_bs)

    # convert secure key to binary bit stream
    sk_bs = [int(k) for k in str2bs(sec_key)]
    len_sk_bs, i = len(sk_bs), 0

    for px in cov_pxs[l:]:
        new_gpx, new_bpx = px[1], px[2]
        if px[0] ^ sk_bs[i % len_sk_bs]:
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

    # save encoded image
    img = Image.new('RGB', cimg.size)
    img.putdata(ret + cov_pxs[i+l:])
    img.save('-'.join([fp_cover_img.split('.')[0], 'encoded.png']))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='Path of cover image')
    parser.add_argument('-s', help='Secure key')
    parser.add_argument('-hi', help='Path of hidden image')
    parser.add_argument('-ht', help='Path of hidden text file')

    args = parser.parse_args()
    try:
        stege(args.c, args.hi, args.ht, args.s)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()