#! /usr/bin/env python

"""Post a new MT entry"""

# username, password, blogid, publish
from settings import *

from types import *

import xmlrpclib

class PostEntryError(Exception): pass
class BodyEmpty(PostEntryError): pass
class BodyNonExistent(PostEntryError): pass
class TitleNotUTF8(PostEntryError): pass
class BodyNotUTF8(PostEntryError): pass

def post(content):
    """Post an entry to a blog.  Return postid on success."""
    
    if content.has_key('description'):
        if len(content['description']) == 0:
            raise BodyEmpty
        if not(type(content['description']) is UnicodeType):
            raise BodyNotUTF8
    else:
        raise BodyNonExistent

    if content.has_key('title'):
        if not(type(content['title']) is UnicodeType):
            raise TitleNotUTF8   

    # XXX: check for exceptions?
    server = xmlrpclib.ServerProxy(uri)

    # on success, result should be an integer representing a postid
    result = server.metaWeblog.newPost(blogid, username, password, \
                                       content, publish)

    return result
