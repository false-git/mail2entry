import os
import stat
import time

from settings import *
import postimage

def save ( images ) :
    imageurls = []
    extension = { 'pjpeg' : 'jpg', 'jpeg' : 'jpg', 'gif' : 'gif' }

    # XXX: come up w/ unique filename -- Python doesn't have
    #      a very good way to do this w/o leakage ;-(
    imagetemplate = "".join(['photo-',
                             time.strftime("%Y%m%d-%H%M%S", time.gmtime()),
                             '-%s.%s'])

    for index in range(len(images)) :
        (image,imgtype) = images[ index ]
        imagefilename = imagetemplate % (index,extension[imgtype])
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

        imageurls.append(imageurl)
    return imageurls
