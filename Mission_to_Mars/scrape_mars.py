{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b5f6e873",
   "metadata": {},
   "outputs": [],
   "source": [
    "pip install splinter"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "413c6142",
   "metadata": {},
   "outputs": [],
   "source": [
    "pip install lxml"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d5f275bc",
   "metadata": {},
   "outputs": [],
   "source": [
    "pip install flask_pymongo"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "89ed0811",
   "metadata": {},
   "outputs": [],
   "source": [
    "pip install pymongo"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "daa88068",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "pip install bs4"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5898436d",
   "metadata": {},
   "outputs": [],
   "source": [
    "pip install webdriver_manager"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "3246b6ca",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Dependencies\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup\n",
    "from webdriver_manager.chrome import ChromeDriverManager\n",
    "import pandas as pd\n",
    "import json\n",
    "import time\n",
    "from IPython.display import Image, display\n",
    "import requests\n",
    "import pymongo\n",
    "from flask import Flask, render_template, redirect\n",
    "from flask_pymongo import PyMongo"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "317184e5",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "====== WebDriver manager ======\n",
      "Current google-chrome version is 93.0.4577\n",
      "Get LATEST driver version for 93.0.4577\n",
      "Driver [C:\\Users\\mariabe\\.wdm\\drivers\\chromedriver\\win32\\93.0.4577.63\\chromedriver.exe] found in cache\n"
     ]
    }
   ],
   "source": [
    "executable_path = {'executable_path': ChromeDriverManager().install()}\n",
    "browser = Browser('chrome', **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "6170aa51",
   "metadata": {},
   "outputs": [],
   "source": [
    "news_url = 'https://mars.nasa.gov/news/'\n",
    "\n",
    "browser.visit(news_url)\n",
    "\n",
    "html = browser.html\n",
    "\n",
    "news_soup = BeautifulSoup(html, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "93cb9866",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Mars Now\n",
      "--------------------------------------------------------------------\n",
      "The rotorcraft captures nuances of rocky outcrop during aerial reconnaissance.   \n",
      "\n"
     ]
    }
   ],
   "source": [
    "# Retrieve the latest news title and paragraph\n",
    "news_title = news_soup.find_all('div', class_='content_title')[0].text\n",
    "news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text\n",
    "\n",
    "print(news_title)\n",
    "print(\"--------------------------------------------------------------------\")\n",
    "print(news_p)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "bd47e5e8",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Mars Image to be scraped\n",
    "jpl_nasa_url = 'https://www.jpl.nasa.gov'\n",
    "images_url = 'https://spaceimages-mars.com/'\n",
    "browser.visit(images_url)\n",
    "\n",
    "html = browser.html\n",
    "\n",
    "images_soup = BeautifulSoup(html, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "bd602366",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "https://www.jpl.nasa.govimage/mars/Proctor Crater Dunes 7.jpg\n"
     ]
    }
   ],
   "source": [
    "# Retrieve featured image link\n",
    "relative_image_path = images_soup.find_all('img')[3][\"src\"]\n",
    "featured_image_url = jpl_nasa_url + relative_image_path\n",
    "print(featured_image_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "237ab5a9",
   "metadata": {},
   "outputs": [],
   "source": [
    "# --- visit the Mars Weather twitter account ---\n",
    "MarsWeather_url = 'https://twitter.com/marswxreport'\n",
    "browser.visit(MarsWeather_url)\n",
    "time.sleep(5)\n",
    "\n",
    "# --- create HTML object ---\n",
    "html = browser.html\n",
    "\n",
    "# --- parse HTML with BeautifulSoup ---\n",
    "soup = BeautifulSoup(html, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "id": "647f10fd",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'Perseverance sol 201 (Sep 12, 2021), high -18.7ºC/-1.7ºF, low -80.7ºC/-113.3ºF, pressure at 6.93 hPa and falling, daylight 05:06:29-18:18:35'"
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# --- save the latest tweet in a variable (found in the text of the first element <span> \n",
    "# under the <div> tag with lang=\"en\" ---\n",
    "tweet = soup.find_all('div', lang='en')[0].text\n",
    "\n",
    "# --- clean up the tweet (remove newline) ---\n",
    "latest_tweet = tweet.replace('\\n', '')\n",
    "        \n",
    "latest_tweet"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "9b245129",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[                      0                              1\n",
       " 0  Equatorial Diameter:                       6,792 km\n",
       " 1       Polar Diameter:                       6,752 km\n",
       " 2                 Mass:  6.39 × 10^23 kg (0.11 Earths)\n",
       " 3                Moons:            2 (Phobos & Deimos)\n",
       " 4       Orbit Distance:       227,943,824 km (1.38 AU)\n",
       " 5         Orbit Period:           687 days (1.9 years)\n",
       " 6  Surface Temperature:                   -87 to -5 °C\n",
       " 7         First Record:              2nd millennium BC\n",
       " 8          Recorded By:           Egyptian astronomers,\n",
       "   Mars - Earth Comparison             Mars            Earth\n",
       " 0               Diameter:         6,779 km        12,742 km\n",
       " 1                   Mass:  6.39 × 10^23 kg  5.97 × 10^24 kg\n",
       " 2                  Moons:                2                1\n",
       " 3      Distance from Sun:   227,943,824 km   149,598,262 km\n",
       " 4         Length of Year:   687 Earth days      365.24 days\n",
       " 5            Temperature:     -87 to -5 °C      -88 to 58°C,\n",
       "                       0                              1\n",
       " 0  Equatorial Diameter:                       6,792 km\n",
       " 1       Polar Diameter:                       6,752 km\n",
       " 2                 Mass:  6.39 × 10^23 kg (0.11 Earths)\n",
       " 3                Moons:            2 (Phobos & Deimos)\n",
       " 4       Orbit Distance:       227,943,824 km (1.38 AU)\n",
       " 5         Orbit Period:           687 days (1.9 years)\n",
       " 6  Surface Temperature:                   -87 to -5 °C\n",
       " 7         First Record:              2nd millennium BC\n",
       " 8          Recorded By:           Egyptian astronomers]"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Mars facts to be scraped\n",
    "facts_url = 'https://space-facts.com/mars/'\n",
    "tables = pd.read_html(facts_url)\n",
    "tables"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "ee65c619",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Description</th>\n",
       "      <th>Value</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Equatorial Diameter:</td>\n",
       "      <td>6,792 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Polar Diameter:</td>\n",
       "      <td>6,752 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Mass:</td>\n",
       "      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Moons:</td>\n",
       "      <td>2 (Phobos &amp; Deimos)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Orbit Distance:</td>\n",
       "      <td>227,943,824 km (1.38 AU)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>Orbit Period:</td>\n",
       "      <td>687 days (1.9 years)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>Surface Temperature:</td>\n",
       "      <td>-87 to -5 °C</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>First Record:</td>\n",
       "      <td>2nd millennium BC</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>Recorded By:</td>\n",
       "      <td>Egyptian astronomers</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "            Description                          Value\n",
       "0  Equatorial Diameter:                       6,792 km\n",
       "1       Polar Diameter:                       6,752 km\n",
       "2                 Mass:  6.39 × 10^23 kg (0.11 Earths)\n",
       "3                Moons:            2 (Phobos & Deimos)\n",
       "4       Orbit Distance:       227,943,824 km (1.38 AU)\n",
       "5         Orbit Period:           687 days (1.9 years)\n",
       "6  Surface Temperature:                   -87 to -5 °C\n",
       "7         First Record:              2nd millennium BC\n",
       "8          Recorded By:           Egyptian astronomers"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "mars_facts_df = tables[2]\n",
    "mars_facts_df.columns = [\"Description\", \"Value\"]\n",
    "mars_facts_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "685cebc7",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'<table border=\"1\" class=\"dataframe\">\\n  <thead>\\n    <tr style=\"text-align: right;\">\\n      <th></th>\\n      <th>Description</th>\\n      <th>Value</th>\\n    </tr>\\n  </thead>\\n  <tbody>\\n    <tr>\\n      <th>0</th>\\n      <td>Equatorial Diameter:</td>\\n      <td>6,792 km</td>\\n    </tr>\\n    <tr>\\n      <th>1</th>\\n      <td>Polar Diameter:</td>\\n      <td>6,752 km</td>\\n    </tr>\\n    <tr>\\n      <th>2</th>\\n      <td>Mass:</td>\\n      <td>6.39 × 10^23 kg (0.11 Earths)</td>\\n    </tr>\\n    <tr>\\n      <th>3</th>\\n      <td>Moons:</td>\\n      <td>2 (Phobos &amp; Deimos)</td>\\n    </tr>\\n    <tr>\\n      <th>4</th>\\n      <td>Orbit Distance:</td>\\n      <td>227,943,824 km (1.38 AU)</td>\\n    </tr>\\n    <tr>\\n      <th>5</th>\\n      <td>Orbit Period:</td>\\n      <td>687 days (1.9 years)</td>\\n    </tr>\\n    <tr>\\n      <th>6</th>\\n      <td>Surface Temperature:</td>\\n      <td>-87 to -5 °C</td>\\n    </tr>\\n    <tr>\\n      <th>7</th>\\n      <td>First Record:</td>\\n      <td>2nd millennium BC</td>\\n    </tr>\\n    <tr>\\n      <th>8</th>\\n      <td>Recorded By:</td>\\n      <td>Egyptian astronomers</td>\\n    </tr>\\n  </tbody>\\n</table>'"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "mars_html_table = mars_facts_df.to_html()\n",
    "mars_html_table"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "df33fd9a",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'<table border=\"1\" class=\"dataframe\">  <thead>    <tr style=\"text-align: right;\">      <th></th>      <th>Description</th>      <th>Value</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>Equatorial Diameter:</td>      <td>6,792 km</td>    </tr>    <tr>      <th>1</th>      <td>Polar Diameter:</td>      <td>6,752 km</td>    </tr>    <tr>      <th>2</th>      <td>Mass:</td>      <td>6.39 × 10^23 kg (0.11 Earths)</td>    </tr>    <tr>      <th>3</th>      <td>Moons:</td>      <td>2 (Phobos &amp; Deimos)</td>    </tr>    <tr>      <th>4</th>      <td>Orbit Distance:</td>      <td>227,943,824 km (1.38 AU)</td>    </tr>    <tr>      <th>5</th>      <td>Orbit Period:</td>      <td>687 days (1.9 years)</td>    </tr>    <tr>      <th>6</th>      <td>Surface Temperature:</td>      <td>-87 to -5 °C</td>    </tr>    <tr>      <th>7</th>      <td>First Record:</td>      <td>2nd millennium BC</td>    </tr>    <tr>      <th>8</th>      <td>Recorded By:</td>      <td>Egyptian astronomers</td>    </tr>  </tbody></table>'"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "mars_html_table.replace('\\n', '')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "4ce9e826",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<table border=\"1\" class=\"dataframe\">\n",
      "  <thead>\n",
      "    <tr style=\"text-align: right;\">\n",
      "      <th></th>\n",
      "      <th>Description</th>\n",
      "      <th>Value</th>\n",
      "    </tr>\n",
      "  </thead>\n",
      "  <tbody>\n",
      "    <tr>\n",
      "      <th>0</th>\n",
      "      <td>Equatorial Diameter:</td>\n",
      "      <td>6,792 km</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>1</th>\n",
      "      <td>Polar Diameter:</td>\n",
      "      <td>6,752 km</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>2</th>\n",
      "      <td>Mass:</td>\n",
      "      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>3</th>\n",
      "      <td>Moons:</td>\n",
      "      <td>2 (Phobos &amp; Deimos)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>4</th>\n",
      "      <td>Orbit Distance:</td>\n",
      "      <td>227,943,824 km (1.38 AU)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>5</th>\n",
      "      <td>Orbit Period:</td>\n",
      "      <td>687 days (1.9 years)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>6</th>\n",
      "      <td>Surface Temperature:</td>\n",
      "      <td>-87 to -5 °C</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>7</th>\n",
      "      <td>First Record:</td>\n",
      "      <td>2nd millennium BC</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <th>8</th>\n",
      "      <td>Recorded By:</td>\n",
      "      <td>Egyptian astronomers</td>\n",
      "    </tr>\n",
      "  </tbody>\n",
      "</table>\n"
     ]
    }
   ],
   "source": [
    "print(mars_html_table)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "56955774",
   "metadata": {},
   "outputs": [],
   "source": [
    "usgs_url = 'https://astrogeology.usgs.gov'\n",
    "hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "\n",
    "browser.visit(hemispheres_url)\n",
    "\n",
    "hemispheres_html = browser.html\n",
    "\n",
    "hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "11f07852",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[{'title': 'Cerberus Hemisphere Enhanced', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, {'title': 'Schiaparelli Hemisphere Enhanced', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}, {'title': 'Syrtis Major Hemisphere Enhanced', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, {'title': 'Valles Marineris Hemisphere Enhanced', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]\n"
     ]
    }
   ],
   "source": [
    "all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')\n",
    "mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')\n",
    "\n",
    "hemisphere_image_urls = []\n",
    "\n",
    "# Iterate through each hemisphere data\n",
    "for i in mars_hemispheres:\n",
    "    # Collect Title\n",
    "    hemisphere = i.find('div', class_=\"description\")\n",
    "    title = hemisphere.h3.text\n",
    "    \n",
    "    # Collect image link by browsing to hemisphere page\n",
    "    hemisphere_link = hemisphere.a[\"href\"]    \n",
    "    browser.visit(usgs_url + hemisphere_link)\n",
    "    \n",
    "    image_html = browser.html\n",
    "    image_soup = BeautifulSoup(image_html, 'html.parser')\n",
    "    \n",
    "    image_link = image_soup.find('div', class_='downloads')\n",
    "    image_url = image_link.find('li').a['href']\n",
    "\n",
    "    # Create Dictionary to store title and url info\n",
    "    image_dict = {}\n",
    "    image_dict['title'] = title\n",
    "    image_dict['img_url'] = image_url\n",
    "    \n",
    "    hemisphere_image_urls.append(image_dict)\n",
    "\n",
    "print(hemisphere_image_urls)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "id": "6b873fb5",
   "metadata": {},
   "outputs": [],
   "source": [
    "mars_dict = {\n",
    "        \"news_title\": news_title,\n",
    "        \"news_p\": news_p,\n",
    "        \"featured_image_url\": featured_image_url,\n",
    "        \"tweet\": tweet,\n",
    "        \"fact_table\": str(mars_html_table),\n",
    "        \"hemisphere_images\": hemisphere_image_urls\n",
    "    }"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "id": "316e3fae",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'news_title': 'Mars Now',\n",
       " 'news_p': 'The rotorcraft captures nuances of rocky outcrop during aerial reconnaissance.   \\n',\n",
       " 'featured_image_url': 'https://www.jpl.nasa.govimage/mars/Proctor Crater Dunes 7.jpg',\n",
       " 'tweet': 'Perseverance sol 201 (Sep 12, 2021), high -18.7ºC/-1.7ºF, low -80.7ºC/-113.3ºF, pressure at 6.93 hPa and falling, daylight 05:06:29-18:18:35',\n",
       " 'fact_table': '<table border=\"1\" class=\"dataframe\">\\n  <thead>\\n    <tr style=\"text-align: right;\">\\n      <th></th>\\n      <th>Description</th>\\n      <th>Value</th>\\n    </tr>\\n  </thead>\\n  <tbody>\\n    <tr>\\n      <th>0</th>\\n      <td>Equatorial Diameter:</td>\\n      <td>6,792 km</td>\\n    </tr>\\n    <tr>\\n      <th>1</th>\\n      <td>Polar Diameter:</td>\\n      <td>6,752 km</td>\\n    </tr>\\n    <tr>\\n      <th>2</th>\\n      <td>Mass:</td>\\n      <td>6.39 × 10^23 kg (0.11 Earths)</td>\\n    </tr>\\n    <tr>\\n      <th>3</th>\\n      <td>Moons:</td>\\n      <td>2 (Phobos &amp; Deimos)</td>\\n    </tr>\\n    <tr>\\n      <th>4</th>\\n      <td>Orbit Distance:</td>\\n      <td>227,943,824 km (1.38 AU)</td>\\n    </tr>\\n    <tr>\\n      <th>5</th>\\n      <td>Orbit Period:</td>\\n      <td>687 days (1.9 years)</td>\\n    </tr>\\n    <tr>\\n      <th>6</th>\\n      <td>Surface Temperature:</td>\\n      <td>-87 to -5 °C</td>\\n    </tr>\\n    <tr>\\n      <th>7</th>\\n      <td>First Record:</td>\\n      <td>2nd millennium BC</td>\\n    </tr>\\n    <tr>\\n      <th>8</th>\\n      <td>Recorded By:</td>\\n      <td>Egyptian astronomers</td>\\n    </tr>\\n  </tbody>\\n</table>',\n",
       " 'hemisphere_images': [{'title': 'Cerberus Hemisphere Enhanced',\n",
       "   'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},\n",
       "  {'title': 'Schiaparelli Hemisphere Enhanced',\n",
       "   'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},\n",
       "  {'title': 'Syrtis Major Hemisphere Enhanced',\n",
       "   'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},\n",
       "  {'title': 'Valles Marineris Hemisphere Enhanced',\n",
       "   'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]}"
      ]
     },
     "execution_count": 28,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "mars_dict"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "33160fdb",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
