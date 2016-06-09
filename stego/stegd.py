import argparse
import math
import os

from PIL import Image

from stego.utility import *

def stegd(cover_img, sec_key):
    """Extract the hidden information, image and/or text, from an image
    :param cover_img: Path to cover image
    :param sec_key: Secret key, usually is a word or sentence
    """

    try:
        # Open the Stego image
        with Image.open(cover_img) as cimg:
            cov_pxs = list(cimg.getdata())
    except:
        raise IOError('Can\'t open image!')

    if not sec_key:
        raise ValueError('Secure Key is needed!')

    #### Get size of hidden information
    l = int(math.ceil(math.log(len(cov_pxs)//8, 2)))

    hm_wid = hm_len = ht_len = 0
    for px in cov_pxs[:l]:
        # Get size of hidden image
        hm_wid = 2 * hm_wid + (px[1] & 1)
        hm_len = 2 * hm_len + (px[2] & 1)

        # Get size of hidden text
        ht_len = 2 * ht_len + (px[0] & 1)

    # Get secret key bit stream
    sec_bs = str2bs(sec_key)
    len_sec_bs = len(sec_bs)

    #### Start to extract hidden information bit by bit
    cnt, i, ret = 0, 0, []
    
    len_lg_bs = max(hm_wid * hm_len * 3 * 8, ht_len * 8)
    len_sh_bs = min(hm_wid * hm_len * 3 * 8, ht_len * 8)

    sk_bs = [int(k) for k in str2bs(sec_key)]
    len_sk_bs = len(sk_bs)

    lg_bs, sh_bs = [], []
    for px in cov_pxs[l:]:

        if px[0] ^ sk_bs[i% len_sk_bs]:
            lg_bs.append(px[1] & 1)
            if i < len_sh_bs:
                sh_bs.append(px[2] & 1)

        else:
            lg_bs.append(px[2] & 1)
            if i < len_sh_bs:
                sh_bs.append(px[1] & 1)
        i += 1
        if i >= len_lg_bs:
            break

    lg_bs = ''.join([str(c) for c in lg_bs])
    sh_bs = ''.join([str(c) for c in sh_bs])

    if hm_wid * hm_len * 3 > ht_len:
        hid_img, hid_text = bs2img(lg_bs), bs2str(sh_bs)
    else:
        hid_img, hid_text = bs2img(sh_bs), bs2str(lg_bs)

    if len(hid_img) > 0:
        img = Image.new('RGB', (hm_wid, hm_len))
        img.putdata(hid_img)
        img.save(os.path.join(os.path.dirname(cover_img), 'hidden_img.png'))

    if len(hid_text) > 0:
        with open(os.path.join(os.path.dirname(cover_img), 'hidden_text.txt'), 'w+') as ht:
            ht.write(hid_text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='Path of cover image')
    parser.add_argument('-s', help='Secure key')

    args = parser.parse_args()
    stegd(args.c, args.s)

if __name__ == '__main__':
    main()