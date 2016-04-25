import unittest
from .. import stego
import os
from PIL import Image

class TestStego(unittest.TestCase):
    def setUp(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.fp_cimg = os.path.join(cur_dir, 'corvette.jpg')
        self.fp_himg = os.path.join(cur_dir, 'lenna.png')
        self.fp_hstr = os.path.join(cur_dir, 'test_file.txt')
        self.sec_key = 'Very Secure!'
        pass

    def test_str2bs(self):
        msg = 'abcd'
        bs = '01100001011000100110001101100100'
        self.assertEqual(stego.str2bs(msg), bs)

    def test_bs2str(self):
        bs = '01100001011000100110001101100100'
        msg = 'abcd'
        self.assertEqual(stego.bs2str(bs), msg)

    def test_bs2dec(self):
        bs = '01111011'
        num = 123
        self.assertEqual(stego.bs2dec(bs), num)

    def test_dec2bs(self):
        num = 123
        bs = '01111011'
        self.assertEqual(stego.dec2bs(num), bs)

    def test_img2bs(self):
        '''Used a dummy image to test for now'''
        img = [(255, 253, 252), (200, 156, 168), (134, 28, 33)]
        bs = '111111111111110111111100110010001001110010101000100001100001110000100001'
        self.assertEqual(stego.img2bs(img), bs)

    def test_bs2img(self):
        bs = '111111111111110111111100110010001001110010101000100001100001110000100001'
        img = [(255, 253, 252), (200, 156, 168), (134, 28, 33)]
        self.assertEqual(stego.bs2img(bs), img)

    def test_enc__dec_info(self):
        stego.enc_info(self.fp_cimg, self.fp_himg, self.fp_hstr, self.sec_key)
        hid_img, hid_str = stego.dec_info(self.fp_cimg, self.sec_key)
        himg = Image.open(self.fp_himg)
        hstr = ''.join(open(self.fp_hstr).readlines())
        self.assertEqual(hid_str, hstr)
        self.assertEqual(himg, hid_img)