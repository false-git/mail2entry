#! /usr/bin/env python

"""Post a new MT entry from a mail message"""

import sys, os, time
import traceback

def main():
    """"""
    # finding and loading things from settings.py
    if len(sys.argv) > 0:
        settings_path = sys.argv[1]
        settings_abspath = os.path.abspath(settings_path)
        if os.access(settings_abspath, os.F_OK):
            sys.path.insert(-1, settings_abspath)
            from settings import *
        else:
            print "Path error"
            sys.exit(1)
    else:
        usage()
        sys.exit(1)

    try:
        import parsemsg
        import postentry

        content, imagefilename = parsemsg.parse(sys.stdin)

        content['description'] = template % \
                                 {'caption': content['description'], \
                                  'imagefilename': imagefilename}

        result = postentry.post(content)
    except:
        lfo = open(logfilepath, "a")
        lfo.write(time.strftime("%Y-%m-%d %H:%M\n\n"))
        traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], \
                                  sys.exc_info()[2], 100, lfo)
        lfo.write("--------------------------------------------------------\n")
        lfo.close()

    return result

def usage():
    """"""
    print "mail2entry.py profile-directory"

if __name__ == "__main__":
    main()
