"""Profile settings"""

username      = "Photo User"
password      = "somethingrelevant"
blogid        = 3
publish       = True
uri           = "https://blog.example.org/cgi-bin/mt-xmlrpc.cgi"
imagesdirpath = "/var/www/blog/archives/images"
imageurldir   = "/blog/archives/images"
template      = "<div class=\"caption\">%(caption)s</div>\n" + \
                "<div class=\"photo\"><img src=\"" + \
                imageurldir + "/%(imagefilename)s\"></div>"
logfilepath   = "/tmp/log-tracebacks.log"
