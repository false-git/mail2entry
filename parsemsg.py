#! /usr/bin/env python2.2

"""Parse a mail message"""

from email import *
from email.Header import *
import types
import re

class ParseMsgError(Exception): pass
class ImageTypeNotAllowed(ParseMsgError): pass
class UnexpectedMimeType(ParseMsgError): pass

class EntryError(Exception): pass
class BodyEmpty(EntryError): pass
class TitleNotUTF8(EntryError): pass
class BodyNotUTF8(EntryError): pass

TextType  = re.compile("^text$",re.IGNORECASE)
ImageType = re.compile("^image$",re.IGNORECASE)

class messageContent :
    def __init__ ( this, title ) :
        this.__title = title
        this.__description = u''
        this.__entry = u''
        this.__images = []

    def getTitle(this) :
        return this.__title
    def getDescription(this) :
        return this.__description
    def addDescription(this,text) :
        this.__description += text
    def getImages(this) :
        return this.__images
    def addImage(this,image) :
        this.__images.append(image)
    def getEntry(this) :
        return this.__entry
    def setEntry(this,entry) :
        this.__entry = entry
    def check(this) :
        if not this.__description :
            raise BodyEmpty
        if type(this.__description) is not types.UnicodeType :
            raise BodyNotUTF8

        if type(this.__title) is not types.UnicodeType :
            raise TitleNotUTF8

def parse(fileObject):
    """Parse a MIME multi-part message, where the first one contains
    text (ISO-2022-JP or ASCII) and the rest contain images,
    w/ an optional subject header (decoded to ISO-2022-JP or ASCII).
    Successful parsing should return a tuple w/ a content dictionary
    suitable for posting and a list of binary content for each extracted
    image."""

    msg = message_from_file(fileObject)
    subject = msg['Subject']
    results = decode_header(subject)

    title = " ".join([unicodify(decoded_subject, charset) \
                      for decoded_subject, charset in results])

    content = messageContent(title)
    parseMultiPart(msg,content)

    return content

def parseMultiPart(msg,content) :
    """Recursively process a (potentially) multi-part
       MIME message. Populates a content structure
       with image and description information."""

    if msg.is_multipart() :
        parts = msg.get_payload()
        for part in parts :
            parseMultiPart(part,content)
    else :
        partType = msg.get_content_maintype()
        if TextType.match(partType) :
            textContent = parse_text_part(msg)
            content.addDescription(textContent)
        elif ImageType.match(partType) :
            imageinfo = parse_image_part(msg)
            content.addImage(imageinfo)
        else :
            raise UnexpectedMimeType

def parse_text_part(msg_part) :
    """Process part of a message known to be text."""
    charset = msg_part.get_param("charset")
    body = msg_part.get_payload(decode=1)

    # drop first line if it begins w/ cell phone number (11 digits)
    body = re.sub("^\d{11}[^\n]*\n", "", body)

    body = unicodify(body, charset)
    return body

def parse_image_part(msg_part) :
    """Process part of a message known to be an image."""

    imgtype = msg_part.get_content_subtype()
    imgtype = imgtype.lower()
    if imgtype not in ( "pjpeg", "jpeg", "gif" ) :
        raise ImageTypeNotAllowed
            
    image = msg_part.get_payload(decode=1)

    return (image,imgtype)

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
        elif charset == 'iso-8859-1':
            result = unicode(string,"iso-8859-1")
        else:
            result = ""
    else:
        result = unicode(string, "us-ascii")

    return result
