#! /usr/bin/env python

"""Parse a mail message"""

from settings import imagesdirpath

import sys
from email import *
from email.Header import *

from time import *
import os
from stat import *

import re

class ParseMsgError(Exception): pass
class UnexpectedNumOfMIMEParts(ParseMsgError): pass
class FirstMIMEPartNotText(ParseMsgError): pass
class SecondMIMEPartNotImage(ParseMsgError): pass
class TextMIMEPartCharsetError(ParseMsgError): pass
class ImageNotJPEG(ParseMsgError): pass

def parse(fileObject):
    """Parse a MIME message w/ two parts, where the first one contains
    text (ISO-2022-JP or ASCII) and the second one contains an image,
    w/ an optional subject header (decoded to ISO-2022-JP or ASCII).
    Successful parsing should return a tuple w/ a content dictionary
    suitable for posting and filename for a file containing the extracted
    image."""
    msg = message_from_file(fileObject)
    subject = msg['Subject']
    results = decode_header(subject)

    title = " ".join([unicodify(decoded_subject, charset) \
                      for decoded_subject, charset in results])
    
    content = {'title': title}

    if msg.is_multipart():
        parts = msg.get_payload()
        num_parts = len(parts)
        
        if num_parts == 2:
            first_part = parts[0]
            
            if not(re.match("^text$", first_part.get_content_maintype(), \
                            re.IGNORECASE)):
                raise FirstMIMEPartNotText

            # XXX: bug in email.Message.get_charset()?
#            first_charset = first_part.get_charset()
            first_charset = first_part.get_param("charset")
            body = first_part.get_payload(decode=1)

            # drop first line if it begins w/ cell phone number (11 digits)
            body = re.sub("^\d{11}[^\n]*\n", "", body)

            body = unicodify(body, first_charset)

            content['description'] = body
            
            second_part = parts[1]

            imagefilename = handle_image_portion(second_part)
        else:
            raise UnexpectedNumOfMIMEParts
    else:
        imagefilename = handle_image_portion(msg)

        content['description'] = u''

    return content, imagefilename

def handle_image_portion(msg_part):
    """"""
    if not(re.match("^image$", msg_part.get_content_maintype(), \
                    re.IGNORECASE)):
        raise SecondMIMEPartNotImage

    if not(re.match("^jpeg$", msg_part.get_content_subtype(), \
                    re.IGNORECASE)):
        raise ImageNotJPEG
            
    # XXX: come up w/ unique filename -- Python doesn't have
    #      a very good way to do this w/o leakage ;-(
    imagefilename = 'blog-photo-' + str(time()) + '.jpg'

    imagefilepath = imagesdirpath + '/' + imagefilename
    nowfilepath = imagesdirpath + '/' + "now.jpg"
            
    fp = open(imagefilepath, "w")
    nfp = open(nowfilepath, "w")
            
    # XXX: exceptions here?
    image = msg_part.get_payload(decode=1)
    # XXX: exceptions here?            
    fp.write(image)
    nfp.write(image)

    fp.close()            
    nfp.close()

    timefilepath = imagesdirpath + '/' + "now.time"

    timestamp = strftime("%b %d %H:%M", localtime(os.stat(nowfilepath)[ST_MTIME])) + ' ' + tzname[0]

    tfp = open(timefilepath, "w")
    tfp.write(timestamp)
    tfp.close()    

    return imagefilename

def unicodify(string, charset):
    """Converts an ISO-2022-JP or US-ASCII string to unicode.  A string using
       another charset results in an empty string being returned."""
    
    result = ""
    
    if charset:
        charset = charset.lower()
        if charset == 'iso-2022-jp':
            result = unicode(string, "japanese.iso-2022-jp")
        elif charset == 'us-ascii':
            result = unicode(string, "us-ascii")
        else:
            result = ""
    else:
        result = unicode(string, "us-ascii")

    return result
