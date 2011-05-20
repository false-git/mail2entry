import os
import stat
import time
from PIL import Image
from StringIO import StringIO

from settings import *
import postimage

def save ( images ) :
    imageurls = []
    extension = { 'pjpeg' : 'jpg', 'jpeg' : 'jpg', 'gif' : 'gif' }

    # XXX: come up w/ unique filename -- Python doesn't have
    #      a very good way to do this w/o leakage ;-(
    imagetemplate = "".join(['photo-',
                             time.strftime("%Y%m%d-%H%M%S", time.gmtime()),
                             '-%s'])
    thumbtemplate = imagetemplate + "s.%s"
    imagetemplate = imagetemplate + ".%s"

    for index in range(len(images)) :
        (image,imgtype) = images[ index ]
        imagefilename = imagetemplate % (index,extension[imgtype])
        thumbfilename = thumbtemplate % (index,extension[imgtype])

        # rotate
        img = Image.open(StringIO(image))
        orientation = img._getexif()[0x0112]
        if orientation == 3:
            img = img.rotate(180)
        elif orientation == 6:
            img = img.rotate(270)
        elif orientation == 8:
            img = img.rotate(90)
        out = StringIO()
        img.save(out, imgtype)
        image = out.getvalue()
        # make thumbnail
        zoom = min(400.0 / max(img.size[0], img.size[1]), 1.0)
        img.thumbnail((int(img.size[0] * zoom), int(img.size[1] * zoom)), Image.ANTIALIAS)
        out = StringIO()
        img.save(out, imgtype)
        thumbnail = out.getvalue()

        if savelocal :
            # XXX: what if the user doesn't want now.jpg and a timestamp?
            imagefilepath = imagesdirpath + '/' + imagefilename
            nowfilepath = imagesdirpath + '/' + "now." + extension[imgtype]
            for imagepath in [ imagefilepath, nowfilepath ] :
                fp = open(imagepath, "w")
                fp.write(image)
                fp.close()
            timefilepath = imagesdirpath + '/' + "now.time"
            fileTimeString = time.strftime("%b %d %H:%M", time.gmtime())
            timeStamp = fileTimeString + ' ' + time.tzname[0]

            tfp = open(timefilepath, "w")
            tfp.write(timeStamp)
            tfp.close()

            imageurl = imageurldir + '/' + imagefilename
        else :
            imageremotepath = imagesdirpath + '/' + imagefilename
            import xmlrpclib
            imagedata = xmlrpclib.Binary(image)
            # XXX: what if the image isn't a jpg?
            imageinfo = { 'name' : imageremotepath,
                          'type' : "image/jpeg",
                          'bits' : imagedata }
            postdata = postimage.post(imageinfo)
            imageurl = postdata['url']

            imageremotepath = imagesdirpath + '/' + thumbfilename
            import xmlrpclib
            imagedata = xmlrpclib.Binary(thumbnail)
            # XXX: what if the image isn't a jpg?
            imageinfo = { 'name' : imageremotepath,
                          'type' : "image/jpeg",
                          'bits' : imagedata }
            postdata = postimage.post(imageinfo)
            thumburl = postdata['url']

        imageurls.append([imageurl, thumburl])
    return imageurls
