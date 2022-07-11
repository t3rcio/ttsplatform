# ttsplatform
A simple "text to speech" converter tool.

**How it works:**
Submit the text's URL and the tool do the rest; after few seconds you get a mp3 file to listen or download.

**To build**
1.    git clone https://github.com/t3rcio/ttsplatform
2.    cd ttsplatform
3.    docker-compose -f docker-compose.yml -up --build

Open your browser and access:
http://172.45.0.5
That is it ;-)

**Ingredients**  
 - Python3 
 - Django 
 - BeatifulSoup 4 
 - gTTS 
 - Requests
 - Docker