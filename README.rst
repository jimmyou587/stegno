======
stegno
======
A cool application to hide and extract images and text into another image without any noticeable distortion.

what's it all about
-------------------
It's all about security. If you want to send images and/or text secretly via the web, this is the way to go. 

how to install
--------------

.. code:: bash

    pip install stego
    ... 
    easy_install stego

how to run
----------
1. Pick a relatively large image as the cover image and a secure key that only you and the receiver know
2. To encode the hidden information to the cover image, run 
        Stege -s SECURE_KEY -c PATH_TO_COVER_IMAGE -hi PATH_TO_HIDDEN_IMAGE -ht PATH_TO_HIDDEN_TEXT_FILE
3. To decode the hidden information from the cover iamge, run
        Stegd -s SECURE_KEY -c PATH_TO_COVER_IMAGE
   then an image named hidden_image.png and a file named hidden_file.txt will be generated in your current directory
  
how to test
-----------
python setup.py test
