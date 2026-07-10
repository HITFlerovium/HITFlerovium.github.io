import urllib.request
import re

html = urllib.request.urlopen('https://www.sfml-dev.org/tutorials/3.1/graphics/draw/').read().decode('utf-8')
main = re.search(r'<article class="md-content__inner md-typeset">(.*?)</article>', html, re.DOTALL)
if main:
    with open('d:/my-blog/sfml_article_draw.html', 'w', encoding='utf-8') as f:
        f.write(main.group(1))
