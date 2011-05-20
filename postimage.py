#! /usr/bin/env python

"""Post an image via newMediaObject"""

# username, password, blogid, publish
from settings import *

import xmlrpclib

class ImageNameMissing(Exception) : pass
class ImageDataMissing(Exception) : pass
class ImageDataInvalid(Exception) : pass

def post(fileinfo) :
    """Uploads an image using the metaWeblog.newMediaObject interface."""

    if not fileinfo.has_key('name') :
        raise ImageNameMissing

    if fileinfo.has_key('bits') :
        if not isinstance(fileinfo['bits'],xmlrpclib.Binary) :
            raise ImageDataInvalid
    else :
        raise ImageDataMissing

    server = xmlrpclib.ServerProxy(uri)

    # on success, result will be the URL to the uploaded file.
    result = server.metaWeblog.newMediaObject(blogid, username, password,
                                              fileinfo)
    return result
