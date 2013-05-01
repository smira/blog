
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

##############################################
# Configuration, please edit
##############################################


# Data about this site
BLOG_AUTHOR = "Андрей"
BLOG_TITLE = "Блог Андрея Смирнова"
# This is the main URL for your site. It will be used
# in a prominent link
SITE_URL = "http://www.smira.ru"
# This is the URL where nikola's output will be deployed.
# If not set, defaults to SITE_URL
# BASE_URL = "http://www.smira.ru"
BLOG_EMAIL = "Smirnov.Andrey@gmail.com"
BLOG_DESCRIPTION = "None"

# Nikola is multilingual!
#
# Currently supported languages are:
#   English -> en
#   Greek -> gr
#   German -> de
#   French -> fr
#   Polish -> pl
#   Russian -> ru
#   Spanish -> es
#   Italian -> it
#   Simplified Chinese -> zh-cn
#
# If you want to use Nikola with a non-supported language you have to provide
# a module containing the necessary translations
# (p.e. look at the modules at: ./nikola/data/themes/default/messages/fr.py).
# If a specific post is not translated to a language, then the version
# in the default language will be shown instead.

# What is the default language?
DEFAULT_LANG = "ru"

# What other languages do you have?
# The format is {"translationcode" : "path/to/translation" }
# the path will be used as a prefix for the generated pages location
TRANSLATIONS = {
    DEFAULT_LANG: "",
    # Example for another language:
    # "es": "./es",
}

# Links for the sidebar / navigation bar.
# You should provide a key-value pair for each used language.
SIDEBAR_LINKS = {
    DEFAULT_LANG: (
        ('/archive.html', 'Archives'),
        ('/categories/index.html', 'Tags'),
        ('/rss.xml', 'RSS'),
    ),
}


##############################################
# Below this point, everything is optional
##############################################


# post_pages contains (wildcard, destination, template, use_in_feed) tuples.
#
# The wildcard is used to generate a list of reSt source files
# (whatever/thing.txt).
# That fragment must have an associated metadata file (whatever/thing.meta),
# and opcionally translated files (example for spanish, with code "es"):
#     whatever/thing.txt.es and whatever/thing.meta.es
#
# From those files, a set of HTML fragment files will be generated:
# cache/whatever/thing.html (and maybe cache/whatever/thing.html.es)
#
# These files are combinated with the template to produce rendered
# pages, which will be placed at
# output / TRANSLATIONS[lang] / destination / pagename.html
#
# where "pagename" is specified in the metadata file.
#
# if use_in_feed is True, then those posts will be added to the site's
# rss feeds.
#

post_pages = (
            ("posts/*.wp", "posts", "post.tmpl", True),
            ("posts/*.rst", "posts", "post.tmpl", True),
            ("stories/*.wp", "stories", "story.tmpl", False),
        )

# One or more folders containing files to be copied as-is into the output.
# The format is a dictionary of "source" "relative destination".
# Default is:
# FILES_FOLDERS = {'files': '' }
# Which means copy 'files' into 'output'

# A mapping of languages to file-extensions that represent that language.
# Feel free to add or delete extensions to any list, but don't add any new
# compilers unless you write the interface for it yourself.
#
# 'rest' is reStructuredText
# 'markdown' is MarkDown
# 'html' assumes the file is html and just copies it
post_compilers = {
        "rest": ('.txt', '.rst'),
        "markdown": ('.md', '.mdown', '.markdown', '.wp'),
        "html": ('.html', '.htm')
        }


# Create by default posts in one file format?
# Set to False for two-file posts, with separate metadata.
# ONE_FILE_POSTS = True

# If this is set to True, then posts that are not translated to a language
# LANG will not be visible at all in the pages in that language.
# If set to False, the DEFAULT_LANG version will be displayed for
# untranslated posts.
# HIDE_UNTRANSLATED_POSTS = False

# Paths for different autogenerated bits. These are combined with the
# translation paths.

# Final locations are:
# output / TRANSLATION[lang] / TAG_PATH / index.html (list of tags)
# output / TRANSLATION[lang] / TAG_PATH / tag.html (list of posts for a tag)
# output / TRANSLATION[lang] / TAG_PATH / tag.xml (RSS feed for a tag)
# TAG_PATH = "categories"

# If TAG_PAGES_ARE_INDEXES is set to True, each tag's page will contain
# the posts themselves. If set to False, it will be just a list of links.
# TAG_PAGES_ARE_INDEXES = True

# Final location is output / TRANSLATION[lang] / INDEX_PATH / index-*.html
# INDEX_PATH = ""

# Create per-month archives instead of per-year
# CREATE_MONTHLY_ARCHIVE = False
# Final locations for the archives are:
# output / TRANSLATION[lang] / ARCHIVE_PATH / ARCHIVE_FILENAME
# output / TRANSLATION[lang] / ARCHIVE_PATH / YEAR / index.html
# output / TRANSLATION[lang] / ARCHIVE_PATH / YEAR / MONTH / index.html
# ARCHIVE_PATH = ""
# ARCHIVE_FILENAME = "archive.html"

# Final locations are:
# output / TRANSLATION[lang] / RSS_PATH / rss.xml
# RSS_PATH = ""

# Slug the Tag URL easier for users to type, special characters are
# often removed or replaced as well.
# SLUG_TAG_PATH = True

# A list of redirection tuples, [("foo/from.html", "/bar/to.html")].
#
# A HTML file will be created in output/foo/from.html that redirects
# to the "/bar/to.html" URL. notice that the "from" side MUST be a
# relative URL.
#
# If you don't need any of these, just set to []
REDIRECTIONS = [(u'2006/07/16/duo/index.html', u'/posts/20060716duo.html'), (u'2009/04/19/vks-country/index.html', u'/posts/20090419vks-country.html'), (u'2006/12/29/%d0%a0%d0%b0%d0%b1%d0%be%d1%82%d0%b0-%d0%bd%d0%b0%d0%b4-%d0%be%d1%88%d0%b8%d0%b1%d0%ba%d0%b0%d0%bc%d0%b8/index.html', u'/posts/20061229d0a0d0b0d0b1d0bed182d0b0-d0bdd0b0d0b4-d0bed188d0b8d0b1d0bad0b0d0bcd0b8.html'), (u'2006/12/29/sun/index.html', u'/posts/20061229sun.html'), (u'2006/12/28/%d0%9f%d1%80%d0%b5%d0%b4%d0%bb%d0%be%d0%b6%d0%b5%d0%bd%d0%b8%d0%b5/index.html', u'/posts/20061228d09fd180d0b5d0b4d0bbd0bed0b6d0b5d0bdd0b8d0b5.html'), (u'2006/12/28/mist/index.html', u'/posts/20061228mist.html'), (u'2009/05/11/fire-in-moscow-no-information/index.html', u'/posts/20090511fire-in-moscow-no-information.html'), (u'2008/10/28/web-caching-memcached-4/index.html', u'/posts/20081028web-caching-memcached-4.html'), (u'2008/11/01/open-source-deferred-qooxdoo/index.html', u'/posts/20081101open-source-deferred-qooxdoo.html'), (u'2008/09/30/highload-2008/index.html', u'/posts/20080930highload-2008.html'), (u'2008/04/25/why-high-level-languages/index.html', u'/posts/20080425why-high-level-languages.html'), (u'2009/02/10/deferred-async-programming/index.html', u'/posts/20090210deferred-async-programming.html'), (u'2008/04/09/rit-2008/index.html', u'/posts/20080409rit-2008.html'), (u'2008/12/20/mts-debt-1000-ruble/index.html', u'/posts/20081220mts-debt-1000-ruble.html'), (u'2006/12/31/%d0%af-%d0%b1%d0%be%d1%8e%d1%81%d1%8c/index.html', u'/posts/20061231d0af-d0b1d0bed18ed181d18c.html'), (u'2006/06/25/betraxxyal/index.html', u'/posts/20060625betraxxyal.html'), (u'2008/04/28/coolered-rai/index.html', u'/posts/20080428coolered-rai.html'), (u'2006/06/25/%d0%96%d0%b5%d0%bd%d1%89%d0%b8%d0%bd%d1%8b-%d1%80%d0%b0%d0%b7%d1%80%d1%83%d1%88%d0%b0%d1%8e%d1%82-%d0%b4%d1%80%d1%83%d0%b6%d0%b1%d1%83/index.html', u'/posts/20060625d096d0b5d0bdd189d0b8d0bdd18b-d180d0b0d0b7d180d183d188d0b0d18ed182-d0b4d180d183d0b6d0b1d183.html'), (u'2008/08/13/commit-log/index.html', u'/posts/20080813commit-log.html'), (u'2008/02/07/cpp-fun-virtual-inheritance/index.html', u'/posts/20080207cpp-fun-virtual-inheritance.html'), (u'2007/01/09/touching-each-other/index.html', u'/posts/20070109touching-each-other.html'), (u'2007/02/14/52/index.html', u'/posts/2007021452.html'), (u'2007/10/13/61/index.html', u'/posts/2007101361.html'), (u'2008/02/04/unit-test-miracle/index.html', u'/posts/20080204unit-test-miracle.html'), (u'2009/10/13/hl-2009-twisted-framework/index.html', u'/posts/20091013hl-2009-twisted-framework.html'), (u'2006/10/19/how-steel-hardened/index.html', u'/posts/20061019how-steel-hardened.html'), (u'2010/10/28/highload-2010-twisted-python-development/index.html', u'/posts/20101028highload-2010-twisted-python-development.html'), (u'2006/12/08/director-of-our-life/index.html', u'/posts/20061208director-of-our-life.html'), (u'2006/12/30/bird/index.html', u'/posts/20061230bird.html'), (u'2007/01/02/its-all-you/index.html', u'/posts/20070102its-all-you.html'), (u'2006/06/21/to-my-friend/index.html', u'/posts/20060621to-my-friend.html'), (u'2007/01/18/%d0%9b%d1%8e%d0%b1%d0%b8%d0%bc%d0%b0%d1%8f/index.html', u'/posts/20070118d09bd18ed0b1d0b8d0bcd0b0d18f.html'), (u'2006/11/17/girls-and-mathematics/index.html', u'/posts/20061117girls-and-mathematics.html'), (u'2009/06/07/flash-media-server-in-python-alpha-release/index.html', u'/posts/20090607flash-media-server-in-python-alpha-release.html'), (u'2006/06/27/love/index.html', u'/posts/20060627love.html'), (u'2008/06/03/index-selectivity-postgresql/index.html', u'/posts/20080603index-selectivity-postgresql.html'), (u'2009/06/08/amqp-in-russian/index.html', u'/posts/20090608amqp-in-russian.html'), (u'2006/12/29/yellow-light/index.html', u'/posts/20061229yellow-light.html'), (u'2008/06/26/straustroup-beginner-programmer-advices/index.html', u'/posts/20080626straustroup-beginner-programmer-advices.html'), (u'2011/08/24/guppy-heapy-usage/index.html', u'/posts/20110824guppy-heapy-usage.html'), (u'2009/02/27/spamfighter-dot-two-release/index.html', u'/posts/20090227spamfighter-dot-two-release.html'), (u'2006/07/25/%d0%a8%d1%83%d1%82%d0%bb%d0%b8%d0%b2%d0%b0%d1%8f-%d0%b8%d1%81%d1%82%d0%be%d1%80%d0%b8%d1%8f-%d0%bc%d0%be%d0%b5%d0%b9-%d0%b6%d0%b8%d0%b7%d0%bd%d0%b8/index.html', u'/posts/20060725d0a8d183d182d0bbd0b8d0b2d0b0d18f-d0b8d181d182d0bed180d0b8d18f-d0bcd0bed0b5d0b9-d0b6d0b8d0b7d0bdd0b8.html'), (u'2007/10/11/60/index.html', u'/posts/2007101160.html'), (u'2009/09/25/hl2009-twisted-framework-python/index.html', u'/posts/20090925hl2009-twisted-framework-python.html'), (u'2008/10/16/web-caching-memcached-1/index.html', u'/posts/20081016web-caching-memcached-1.html'), (u'2008/02/02/about-me/index.html', u'/posts/20080202about-me.html'), (u'2007/05/27/%d0%9a%d0%b0%d0%ba-%d1%8d%d1%82%d0%be/index.html', u'/posts/20070527d09ad0b0d0ba-d18dd182d0be.html'), (u'2007/03/17/%d0%a1%d1%82%d0%be%d0%bf/index.html', u'/posts/20070317d0a1d182d0bed0bf.html'), (u'2008/02/09/python-memory-leak-resolved/index.html', u'/posts/20080209python-memory-leak-resolved.html'), (u'2006/12/31/%d0%a1-%d0%9d%d0%be%d0%b2%d1%8b%d0%bc-%d0%b3%d0%be%d0%b4%d0%be%d0%bc/index.html', u'/posts/20061231d0a1-d09dd0bed0b2d18bd0bc-d0b3d0bed0b4d0bed0bc.html'), (u'2006/12/24/34/index.html', u'/posts/2006122434.html'), (u'2008/03/30/teaching-c-plus-plus/index.html', u'/posts/20080330teaching-c-plus-plus.html'), (u'2007/02/01/%d0%a6%d0%b5%d0%bb%d1%8c-%d0%b6%d0%b8%d0%b7%d0%bd%d0%b8/index.html', u'/posts/20070201d0a6d0b5d0bbd18c-d0b6d0b8d0b7d0bdd0b8.html'), (u'2009/10/05/mongrel-vs-phusion-passenger-obvious-choice/index.html', u'/posts/20091005mongrel-vs-phusion-passenger-obvious-choice.html'), (u'2006/12/24/%d0%9e%d1%88%d0%b8%d0%b1%d0%ba%d0%b8-%d0%b2-%d0%b6%d0%b8%d0%b7%d0%bd%d0%b8/index.html', u'/posts/20061224d09ed188d0b8d0b1d0bad0b8-d0b2-d0b6d0b8d0b7d0bdd0b8.html'), (u'2009/04/27/ffmpeg-lame-output-buffer-too-small/index.html', u'/posts/20090427ffmpeg-lame-output-buffer-too-small.html'), (u'2007/02/25/star-at-the-sky/index.html', u'/posts/20070225star-at-the-sky.html'), (u'2009/01/06/postgresql-vs-mysql/index.html', u'/posts/20090106postgresql-vs-mysql.html'), (u'2008/10/21/web-caching-memcached-2/index.html', u'/posts/20081021web-caching-memcached-2.html'), (u'2007/04/15/tale/index.html', u'/posts/20070415tale.html'), (u'2008/07/10/mts-euroset-beeline/index.html', u'/posts/20080710mts-euroset-beeline.html'), (u'2009/03/18/opel-astra-16-cosmo-2006/index.html', u'/posts/20090318opel-astra-16-cosmo-2006.html'), (u'2010/10/30/mysql-udf-json-memcacheq/index.html', u'/posts/20101030mysql-udf-json-memcacheq.html'), (u'2008/08/27/mdc-to-be-launched-soon/index.html', u'/posts/20080827mdc-to-be-launched-soon.html'), (u'2008/12/03/cdn-content-delivery/index.html', u'/posts/20081203cdn-content-delivery.html'), (u'2009/05/29/deferred-in-javascript-for-prototype/index.html', u'/posts/20090529deferred-in-javascript-for-prototype.html'), (u'2008/06/22/web-cache-memcached-1/index.html', u'/posts/20080622web-cache-memcached-1.html'), (u'2008/09/28/rit-highload-2008/index.html', u'/posts/20080928rit-highload-2008.html'), (u'2008/12/19/djb/index.html', u'/posts/20081219djb.html'), (u'2006/12/24/%d0%92%d1%80%d0%b5%d0%bc%d1%8f/index.html', u'/posts/20061224d092d180d0b5d0bcd18f.html'), (u'2008/10/24/web-caching-memcached-3/index.html', u'/posts/20081024web-caching-memcached-3.html'), (u'2008/02/19/valhenson-insight/index.html', u'/posts/20080219valhenson-insight.html'), (u'2008/12/02/video-broadcast-delivery/index.html', u'/posts/20081202video-broadcast-delivery.html'), (u'2010/02/15/profiling-twisted-applications/index.html', u'/posts/20100215profiling-twisted-applications.html'), (u'2009/01/21/data-structures-in-memcached-memcachedb/index.html', u'/posts/20090121data-structures-in-memcached-memcachedb.html'), (u'2008/03/23/%d1%80%d0%b5%d0%bb%d0%b8%d0%b7-12-%d0%b9-%d0%b2%d0%b5%d1%80%d1%81%d0%b8%d0%b8-loadup/index.html', u'/posts/20080323d180d0b5d0bbd0b8d0b7-12-d0b9-d0b2d0b5d180d181d0b8d0b8-loadup.html'), (u'2007/04/02/%d0%9f%d1%80%d0%be%d1%81%d1%82%d0%b8-%d0%bc%d0%b5%d0%bd%d1%8f/index.html', u'/posts/20070402d09fd180d0bed181d182d0b8-d0bcd0b5d0bdd18f.html'), (u'2009/02/24/more-about-deferred/index.html', u'/posts/20090224more-about-deferred.html'), (u'2008/10/08/highload-plus-plus-2008/index.html', u'/posts/20081008highload-plus-plus-2008.html'), (u'2006/07/06/flight-of-life/index.html', u'/posts/20060706flight-of-life.html'), (u'2006/12/31/43/index.html', u'/posts/2006123143.html'), (u'2008/11/17/russian-vim-spell-checking/index.html', u'/posts/20081117russian-vim-spell-checking.html'), (u'2008/10/31/web-caching-memcached-6/index.html', u'/posts/20081031web-caching-memcached-6.html'), (u'2008/06/23/web-cache-memcached-2/index.html', u'/posts/20080623web-cache-memcached-2.html'), (u'2008/10/24/twisted-log-and-trial-fun/index.html', u'/posts/20081024twisted-log-and-trial-fun.html'), (u'2008/10/29/web-caching-memcached-5/index.html', u'/posts/20081029web-caching-memcached-5.html'), (u'2008/02/03/bitten-trac-integration/index.html', u'/posts/20080203bitten-trac-integration.html'), (u'2009/07/12/qik-push-engine-api-private-beta/index.html', u'/posts/20090712qik-push-engine-api-private-beta.html'), (u'2008/07/10/ffmpeg-memory-leak-av_read_packet/index.html', u'/posts/20080710ffmpeg-memory-leak-av_read_packet.html'), (u'2007/01/19/%d0%96%d0%b5%d0%bd%d1%89%d0%b8%d0%bd%d0%b0/index.html', u'/posts/20070119d096d0b5d0bdd189d0b8d0bdd0b0.html'), (u'2006/12/30/%d0%a5%d0%be%d1%87%d1%83-%d1%87%d1%82%d0%be%d0%b1%d1%8b-%d0%bc%d0%bd%d0%b5-%d0%b2%d0%b5%d1%80%d0%b8%d0%bb%d0%b8/index.html', u'/posts/20061230d0a5d0bed187d183-d187d182d0bed0b1d18b-d0bcd0bdd0b5-d0b2d0b5d180d0b8d0bbd0b8.html'), (u'2008/02/04/cplusplus-miracles-constructors/index.html', u'/posts/20080204cplusplus-miracles-constructors.html'), (u'2008/02/05/musaev-microsoft-program-management/index.html', u'/posts/20080205musaev-microsoft-program-management.html'), (u'2010/10/31/dont-forget-about-escaping/index.html', u'/posts/20101031dont-forget-about-escaping.html'), (u'2010/02/15/mysql-row-statement-mixed-replication-triggers/index.html', u'/posts/20100215mysql-row-statement-mixed-replication-triggers.html')]

# Commands to execute to deploy. Can be anything, for example,
# you may use rsync:
# "rsync -rav output/* joe@my.site:/srv/www/site"
# And then do a backup, or ping pingomatic.
# To do manual deployment, set it to []
DEPLOY_COMMANDS = ["rsync -vap output/ smira.ru@smira.ru:content/"]

# Where the output site should be located
# If you don't use an absolute path, it will be considered as relative
# to the location of conf.py
# OUTPUT_FOLDER = 'output'

# where the "cache" of partial generated content should be located
# default: 'cache'
# CACHE_FOLDER = 'cache'

# Filters to apply to the output.
# A directory where the keys are either: a file extensions, or
# a tuple of file extensions.
#
# And the value is a list of commands to be applied in order.
#
# Each command must be either:
#
# A string containing a '%s' which will
# be replaced with a filename. The command *must* produce output
# in place.
#
# Or:
#
# A python callable, which will be called with the filename as
# argument.
#
# By default, there are no filters.

from nikola import filters

FILTERS = {
    ".jpg": ["jpegoptim --strip-all -m75 -v %s"],
    ".css": [filters.yui_compressor],
    ".js": [filters.yui_compressor],
}

# Create a gzipped copy of each generated file. Cheap server-side optimization.
# GZIP_FILES = False
# File extensions that will be compressed
# GZIP_EXTENSIONS = ('.txt', '.htm', '.html', '.css', '.js', '.json')

# #############################################################################
# Image Gallery Options
# #############################################################################

# Galleries are folders in galleries/
# Final location of galleries will be output / GALLERY_PATH / gallery_name
# GALLERY_PATH = "galleries"
# THUMBNAIL_SIZE = 180
# MAX_IMAGE_SIZE = 1280
# USE_FILENAME_AS_TITLE = True

# #############################################################################
# HTML fragments and diverse things that are used by the templates
# #############################################################################

# Data about post-per-page indexes
# INDEXES_TITLE = ""  # If this is empty, the default is BLOG_TITLE
# INDEXES_PAGES = ""  # If this is empty, the default is 'old posts page %d' translated

# Name of the theme to use.
# THEME = 'site'

# Color scheme to be used for code blocks. If your theme provide "assets/css/code.css" this
# is ignored.
# Can be any of autumn borland bw colorful default emacs friendly fruity manni monokai
# murphy native pastie perldoc rrt tango trac vim vs
# CODE_COLOR_SCHEME = default

# If you use 'site-reveal' theme you can select several subthemes
# THEME_REVEAL_CONGIF_SUBTHEME = 'sky' # You can also use: beige/serif/simple/night/default

# Again, if you use 'site-reveal' theme you can select several transitions between the slides
# THEME_REVEAL_CONGIF_TRANSITION = 'cube' # You can also use: page/concave/linear/none/default

# date format used to display post dates. (str used by datetime.datetime.strftime)
DATE_FORMAT = '%d.%m.%Y %H:%M'

# FAVICONS contains (name, file, size) tuples.
# Used for create favicon link like this:
# <link rel="name" href="file" sizes="size"/>
# about favicons, see: http://www.netmagazine.com/features/create-perfect-favicon
# FAVICONS = {
#     ("icon", "/favicon.ico", "16x16"),
#     ("icon", "/icon_128x128.png", "128x128"),
# }

# Show only teasers in the index pages? Defaults to False.
# INDEX_TEASERS = False

# A HTML fragment describing the license, for the sidebar. Default is "".
# I recommend using the Creative Commons' wizard:
# http://creativecommons.org/choose/
# LICENSE = """
# <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/2.5/ar/">
# <img alt="Creative Commons License BY-NC-SA"
# style="border-width:0; margin-bottom:12px;"
# src="http://i.creativecommons.org/l/by-nc-sa/2.5/ar/88x31.png"></a>"""

# A small copyright notice for the page footer (in HTML).
# Default is ''
CONTENT_FOOTER = 'Contents &copy; {date} <a href="mailto:{email}">{author}</a> - Powered by <a href="http://nikola.ralsina.com.ar">Nikola</a>'
CONTENT_FOOTER = CONTENT_FOOTER.format(email=BLOG_EMAIL,
                                       author=BLOG_AUTHOR,
                                       date=time.gmtime().tm_year)

# To enable comments via Disqus, you need to create a forum at
# http://disqus.com, and set DISQUS_FORUM to the short name you selected.
# If you want to disable comments, set it to False.
# Default is "nikolademo", used by the demo sites
DISQUS_FORUM = "smira"

# Create index.html for story folders?
# STORY_INDEX = False
# Enable comments on story pages?
# COMMENTS_IN_STORIES = False
# Enable comments on picture gallery pages?
# COMMENTS_IN_GALLERIES = False

# If a link ends in /index.html, drop the index.html part.
# http://mysite/foo/bar/index.html => http://mysite/foo/bar/
# Default = False
# STRIP_INDEX_HTML = False

# Do you want a add a Mathjax config file?
# MATHJAX_CONFIG = ""

# If you are using the compile-ipynb plugin, just add this one:
#MATHJAX_CONFIG = """
#<script type="text/x-mathjax-config">
#MathJax.Hub.Config({
#    tex2jax: {
#        inlineMath: [ ['$','$'], ["\\\(","\\\)"] ],
#        displayMath: [ ['$$','$$'], ["\\\[","\\\]"] ]
#    },
#    displayAlign: 'left', // Change this to 'center' to center equations.
#    "HTML-CSS": {
#        styles: {'.MathJax_Display': {"margin": 0}}
#    }
#});
#</script>
#"""

# Enable Addthis social buttons?
# Defaults to true
ADD_THIS_BUTTONS = False

# Modify the number of Post per Index Page
# Defaults to 10
# INDEX_DISPLAY_POST_COUNT = 10

# RSS_LINK is a HTML fragment to link the RSS or Atom feeds. If set to None,
# the base.tmpl will use the feed Nikola generates. However, you may want to
# change it for a feedburner feed or something else.
# RSS_LINK = None

# Show only teasers in the RSS feed? Default to True
# RSS_TEASERS = True

# A search form to search this site, for the sidebar. You can use a google
# custom search (http://www.google.com/cse/)
# Or a duckduckgo search: https://duckduckgo.com/search_box.html
# Default is no search form.
# SEARCH_FORM = ""
#
# This search form works for any site and looks good in the "site" theme where it
# appears on the navigation bar
#SEARCH_FORM = """
#<!-- Custom search -->
#<form method="get" id="search" action="http://duckduckgo.com/"
# class="navbar-form pull-left">
#<input type="hidden" name="sites" value="%s"/>
#<input type="hidden" name="k8" value="#444444"/>
#<input type="hidden" name="k9" value="#D51920"/>
#<input type="hidden" name="kt" value="h"/>
#<input type="text" name="q" maxlength="255"
# placeholder="Search&hellip;" class="span2" style="margin-top: 4px;"/>
#<input type="submit" value="DuckDuckGo Search" style="visibility: hidden;" />
#</form>
#<!-- End of custom search -->
#""" % BLOG_URL
#
# Also, there is a local search plugin you can use.

# Use content distribution networks for jquery and twitter-bootstrap css and js
# If this is True, jquery is served from the Google CDN and twitter-bootstrap
# is served from the NetDNA CDN
# Set this to False if you want to host your site without requiring access to
# external resources.
# USE_CDN = False

# Extra things you want in the pages HEAD tag. This will be added right
# before </HEAD>
# EXTRA_HEAD_DATA = ""
# Google analytics or whatever else you use. Added to the bottom of <body>
# in the default template (base.tmpl).
# ANALYTICS = ""

# The possibility to extract metadata from the filename by using a
# regular expression.
# To make it work you need to name parts of your regular expression.
# The following names will be used to extract metadata:
# - title
# - slug
# - date
# - tags
# - link
# - description
#
# An example re is the following:
# '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)-(?P<title>.*)\.md'
# FILE_METADATA_REGEXP = None

# Nikola supports Twitter Card summaries / Open Graph.
# Twitter cards make it possible for you to attach media to Tweets
# that link to your content.
#
# IMPORTANT:
# Please note, that you need to opt-in for using Twitter Cards!
# To do this please visit https://dev.twitter.com/form/participate-twitter-cards
#
# Uncomment and modify to following lines to match your accounts.
# Specifying the id for either 'site' or 'creator' will be preferred
# over the cleartext username. Specifying an ID is not necessary.
# Displaying images is currently not supported.
# TWITTER_CARD = {
#     # 'use_twitter_cards': True,  # enable Twitter Cards / Open Graph
#     # 'site': '@website',  # twitter nick for the website
#     # 'site:id': 123456,  # Same as site, but the website's Twitter user ID instead.
#     # 'creator': '@username',  # Username for the content creator / author.
#     # 'creator:id': 654321,  # Same as creator, but the Twitter user's ID.
# }


# If you want to use formatted post time in W3C-DTF Format(ex. 2012-03-30T23:00:00+02:00),
# set timzone if you want a localized posted date.
#
# TIMEZONE = 'Europe/Zurich'

# If webassets is installed, bundle JS and CSS to make site loading faster
USE_BUNDLES = True

# Plugins you don't want to use. Be careful :-)
# DISABLED_PLUGINS = ["render_galleries"]

# Experimental plugins - use at your own risk.
# They probably need some manual adjustments - please see their respective readme.
# ENABLED_EXTRAS = [
#     'planetoid',
#     'ipynb',
#     'localsearch',
#     'mustache',
# ]

# Put in global_context things you want available on all your templates.
# It can be anything, data, functions, modules, etc.

GLOBAL_CONTEXT = {}
