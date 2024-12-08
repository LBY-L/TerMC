import urllib.request
UserAgent = {'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'}
def DowloadJar(dowloadUrl, path, fileName):
    request = urllib.request.Request(dowloadUrl, headers=UserAgent)
    
    with urllib.request.urlopen(request) as response, open(path + fileName, "wb") as outFile:
        # Leer y escribir el contenido en bloques
        outFile.write(response.read())
DowloadJar("https://github.com/Moosync/Moosync/releases/download/v10.3.2/Moosync-10.3.2-linux-x86_64.AppImage", "./", "nose.appimage")