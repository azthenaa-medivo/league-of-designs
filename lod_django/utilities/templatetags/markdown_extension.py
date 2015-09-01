from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern, Pattern, LinkPattern, LINK_RE
from markdown import markdown as m, util

QUOTE_RE = "\[\{quoted\}\]\((.*)\)"

class QuotePattern(LinkPattern):
    """Since nothing seems to work to-day.
    This is an override of the Link Pattern,
    to detect {quoted} blocks in Red Posts.
    I'll try to find out what went wrong with the Extension later."""
    def handleMatch(self, m):
        if m.group(2) == "{quoted}":
            el = util.etree.Element("span")
            href = m.group(9)
            qd = {q[0]: q[1] for q in [qp.split('=') for qp in href.split(',')]}
            el.text = qd['name'] + ' said (<span data-date="'+ qd['timestamp'] + '" class="computed-date"></span>) :'
            el.set("class", "quote-op")
            # el.set("href", "http://boards."+qd['realm'].lower()+".leagueoflegends.com/en/c/"+ \
            #        qd['application-id']+"/"+qd['discussion-id']+"?comment="+qd['comment-id'])
            return el

        el = util.etree.Element("a")
        el.text = m.group(2)
        title = m.group(13)
        href = m.group(9)

        if href:
            if href[0] == "<":
                href = href[1:-1]
            el.set("href", self.sanitize_url(self.unescape(href.strip())))
            el.set("target", "_blank")
        else:
            el.set("href", "")

        if title:
            title = dequote(self.unescape(title))
            el.set("title", title)
        return el

class QuoteExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['link'] = QuotePattern(LINK_RE, md)

if __name__ == "__main__":
    print(m('[{quoted}](name=patmax17,realm=EUW,application-id=6kFXY1kR,discussion-id=hKbmq2Ta,comment-id=00040002,timestamp=2015-07-17T10:01:15.014+0000)',
            extensions=[QuoteExtension()]
            )
          )