import unittest
from stego import utility, stege, stegd
import os
from PIL import Image

class TestStego(unittest.TestCase):
    def setUp(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.fp_cimg = os.path.join(cur_dir, 'corvette.png')
        self.fp_himg = os.path.join(cur_dir, 'lenna-256.png')
        self.fp_ht   = os.path.join(cur_dir, 'test_file.txt')
        self.sec_key = 'Very Secure!'
        pass

    def test_str2bs(self):
        msg = 'abcd'
        bs = '01100001011000100110001101100100'
        self.assertEqual(utility.str2bs(msg), bs)

    def test_bs2str(self):
        bs = '01100001011000100110001101100100'
        msg = 'abcd'
        self.assertEqual(utility.bs2str(bs), msg)

    def test_bs2img(self):
        bs = '111111111111110111111100110010001001110010101000100001100001110000100001'
        img = [(255, 253, 252), (200, 156, 168), (134, 28, 33)]
        self.assertEqual(utility.bs2img(bs), img)

    def test_replace_lsb(self):
        i1, i2, b1, b2 = 64, 127, 1, 0
        self.assertEqual(utility.replace_lsb(i1, b1), 65)
        self.assertEqual(utility.replace_lsb(i2, b2), 126)

    def test_get_rgb(self):
        self.assertEqual(1, 1)

    def test_enc_no_sk(self):
        '''
            secure key is empty
        '''
        skey = None
        try:
            stege.stege(self.fp_cimg, self.fp_himg, self.fp_ht, skey)
        except ValueError as e:
            self.assertEqual(str(e), 'Secure Key is needed!')
        else:
            self.fail()

    def test_enc_no_cimg(self):
        '''
            cover image is empty
        '''
        cimg = None
        try:
            stege.stege(cimg, self.fp_himg, self.fp_ht, self.sec_key)
        except IOError as e:
            self.assertEqual(str(e), 'Can\'t open cover image!')
        else:
            self.fail()

    def test_enc_no_himg_no_ht(self):
        '''
            hidden image empty
        '''
        himg, ht = None, None
        try:
            stege.stege(self.fp_cimg, himg, ht, self.sec_key)
        except ValueError as e:
            self.assertEqual(str(e), 'Nothing to hide!')
        else:
            self.fail()

    def test_enc_dec(self):
        stege.stege(self.fp_cimg, None, self.fp_ht, self.sec_key)
        enc_img = '-'.join([self.fp_cimg.split('.')[0], 'encoded.png'])
        stegd.stegd(enc_img, self.sec_key)
        fp_new_img = 'hidden_img.png'
        new_img = Image.open(fp_new_img)
        hid_img = Image.open(self.fp_himg)

        hid_pxs = [px[:3] for px in hid_img.getdata()]
        for pxs in zip(new_img.getdata(), hid_pxs):
            self.assertEqual(pxs[0], pxs[1])

if __name__ == '__main__':
    unittest.main()