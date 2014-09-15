# requires `youtube-dl`
from requests import get
from bs4 import BeautifulSoup
from subprocess import call

# change this
savedir = '/Users/henry/Documents/Books/ConvexOptimizationVideos/'

url = 'http://web.stanford.edu/class/ee364a/'
r = get(url + 'videos.html')

soup = BeautifulSoup(r.text)

links = soup.find('table', attrs={'id': 'videos'}).findAll('tr')

num = 0
for row in links:
    cells = row.findAll('td')

    if cells[0].text != 'Lecture ':
        link = cells[0].a
        date = link.text.replace(' ', '-')

        slides = cells[1].text.strip()
        slides = '--'.join(slides.split(' to '))

        filename = str(num).zfill(2) + '_' + date + '_' + slides
        num += 1

        vidurl = url + link['href']
        vidpage = get(vidurl)
        vidsoup = BeautifulSoup(vidpage.text)

        video = vidsoup.find('object')
        yourl = video.embed['src'].split('&')[0]

        cmd = 'youtube-dl -o "%s%s.%%(ext)s" %s' % (savedir, filename, yourl)
        call(cmd, shell=True)

        print 'Finished %s' % filename
