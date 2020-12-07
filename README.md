# Welcome to pyextractsum!

Start by cloning the git repository and making sure you have python 3.9.0 installed

Make sure you have Tesseract OCR installed as well, this can be found at https://github.com/tesseract-ocr/tessdoc

I recommend using a virtual enviroment with venv
(Mac/Linux)
```bash
python3 -m venv env
```
(Windows)
```bash
py -m venv env
```

Make sure the Images folder is populated with images labeled in integer order (currently .tiff, but this can be changed in the cv.py file).
Then, install the required python packages with
```bash
pip3 install -r requirements.txt
```
Next, run
```python
python3 cv.py
```
Click and drag to highlight the text you would like to include in your summary and press esc to continue!
