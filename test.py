import os, sys, tempfile, shutil, contextlib
import flask
import urllib
import urllib.parse
import urllib.request
import hashlib
import collections
import mimetypes
import cv2

import flask
def view_page():
    #value = flask.request.args.get("url")
    o = urllib.parse.urlparse("alexquinn.org")
    if o.scheme == '':
        print("invalid url")
        exit(2)
    if o.netloc == '':
        print("123")
        return False
    print(o)
    return



def face_size(face):
    size = face[2]*face[3]
    return size


def get_image_info(filename):
    FACE_DATA_PATH = '/home/ecegridfs/a/ee364/site-packages/cv2/data/haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(FACE_DATA_PATH)
    image_info = dict()
    faces = list()
    img = cv2.imread(filename)   #Use the function cv2.imread() to read an image. The image should be in the working directory or a full path of image should be given.
    height, width = img.shape[:2]  #Shape of image is accessed by img.shape. It returns a tuple of number of rows, columns and channels (if image is color):
    img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(img_grayscale, 1.3, 5)
    face = sorted(face, key=face_size, reverse=True)
    #print(face)
    for f in face:
        ff = dict()
        ff["w"] = f[2]
        ff["h"] = f[3]
        ff["x"] = f[0]
        ff["y"] = f[1]
        faces.append(ff)
    image_info["w"] = width
    image_info["h"] = height
    image_info["faces"] = faces
    return image_info

def make_filename(url,extension):
    filename = hashlib.sha1(url.encode('utf8'))+"."+extension
    return filename

@contextlib.contextmanager
def pushd_temp_dir(base_dir=None, prefix="tmp.hpo."):
    '''
    Create a temporary directory starting with {prefix} within {base_dir}
    and cd to it.

    This is a context manager.  That means it can---and must---be called using
    the with statement like this:

        with pushd_temp_dir():
            ....   # We are now in the temp directory
        # Back to original directory.  Temp directory has been deleted.

    After the with statement, the temp directory and its contents are deleted.


    Putting the @contextlib.contextmanager decorator just above a function
    makes it a context manager.  It must be a generator function with one yield.

    - base_dir --- the new temp directory will be created inside {base_dir}.
                   This defaults to {main_dir}/data ... where {main_dir} is
                   the directory containing whatever .py file started the
                   application (e.g., main.py).

    - prefix ----- prefix for the temp directory name.  In case something
                   happens that prevents
    '''
    if base_dir is None:
        proj_dir = sys.path[0]
        # e.g., "/home/ecegridfs/a/ee364z15/hpo"

        main_dir = os.path.join(proj_dir, "data")
        # e.g., "/home/ecegridfs/a/ee364z15/hpo/data"

    # Create temp directory
    temp_dir_path = tempfile.mkdtemp(prefix=prefix, dir=base_dir)

    try:
        start_dir = os.getcwd()  # get current working directory
        os.chdir(temp_dir_path)  # change to the new temp directory

        try:
            yield
        finally:
            # No matter what, change back to where you started.
            os.chdir(start_dir)
    finally:
        # No matter what, remove temp dir and contents.
        shutil.rmtree(temp_dir_path, ignore_errors=True)




@contextlib.contextmanager
def fetch_images(etree):
    with pushd_temp_dir():
        filename_to_node = collections.OrderedDict()
        for node in etree.iter():
            if node.tag == "img":
                url = node.get("src")
                #req = urllib.request.Request(url)
                with urllib.request.urlopen(url) as response:
                    type = response.info().get('Content-Type')
                    extension = mimetypes.guess_extension(type)
                    filename = make_filename(url,extension)
                    filename_to_node[filename] = node
                    with open(filename) as file:
                        file.write(response.read())
        yield filename_to_node

def read_image(photo):
    img_content = cv2.imread(photo)
    print(img_content)
    return

#image_in = get_image_info("College_of_Science_ROG-c.svg")
#print(image_in)
read_image("43cdcd7c62213cf0af22cef70f330af53987d490.jpg")