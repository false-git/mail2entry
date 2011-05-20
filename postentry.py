#! /usr/bin/env python

"""Post a new MT entry"""

# username, password, blogid, publish
from settings import *

import types
import xmlrpclib

def post(content):
    """Post an entry to a blog.  Return postid on success."""
    
    content.check()
    weblogContent = { 'title' : content.getTitle(),
                      'description' : content.getEntry() }

    server = xmlrpclib.ServerProxy(uri)

    # on success, result should be an integer representing a postid
    result = server.metaWeblog.newPost(blogid, username, password, 
                                       weblogContent, publish)

    return result
