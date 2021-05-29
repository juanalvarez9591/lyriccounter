import bs4 as bs
import urllib.request
import matplotlib.pyplot as plt
import random

searchseed = "https://search.azlyrics.com/search.php?q="

print("Este programa utiliza y depende de la pagina AZLYRICS.COM, no hay intencion de infringir derechos de autor")
print("Escribi el nombre de la cancion que queres buscar")
print("Podes agregar tambien el nombre del artista para buscar con mas precision")
si1 = input("> ")

searchinput = si1.replace(" ","+")

search = searchseed+searchinput

sauce = urllib.request.urlopen(search)
soup = bs.BeautifulSoup(sauce, "lxml")

try:
    table = soup.find("table")
    tr = table.find_all("tr")
except:
    print("No se han encontrado resultados, revise errores de tipeo")
    print("o es posible que AZLYRICS.COM no tenga la letra de la cancion")
    exit()


# Creating two lists that contain the names of the search, and the corresponding URL
results = []
links = []

for i in tr:
    try:
        results.append(i.b.text+"- "+i.b.find_next("b").text)
        links.append(i.a["href"])
    except: 
        pass

# Stuff to setting up the comand stuff

length = len(results)

for i in range(0,length):
    print(str(i)+" "+results[i])

selection = input("Selecciona el numero que corresponde a tu cancion: > ")

thelink = links[int(selection)]

sauce = urllib.request.urlopen(thelink)

soup = bs.BeautifulSoup(sauce, "lxml")


thediv = soup.find("div", class_="col-xs-12 col-lg-8 text-center")
lyricsdiv = thediv.find("div", {"class": None})

# eso lo que hace es ver si estan las tags <a>, <i> y si es asi eliminarlas
# que suelen incluir el nombre del artista o quien habla en el medio de la cancion
ai = ["a","i"]
for x in ai:
    for n in lyricsdiv.find_all(x):
        n.clear()

file = lyricsdiv.text

#Aca comienza el sistema de procesado de liricas

data = file.lower() #Ponerlo en minuscula

# Aca borramos caracteres que suelen haber en las canciones que rompen la estructura
# desde una coma que rompe el sistema de listas, hasta un simbolo que la complica

forbidden = [",","'",'"',"@","#","&","-","(",")","!","¡","?","¿",".","[","]"]
for i in forbidden:
    data = data.replace(i,"")

data = data.replace("$","s") # Excepcion fuera del loop

#Esto pasa a transformar el texto a una lista con todas las palabras
#por eso es importante tratar el texto antes de transformalo en lista
#porque al texto no se le pueden hacer las mismas cosas q a una lista en python
words = data.split()

counter = {}
for i in words:
    counter[i] = words.count(i)


#Sorts dictionary by descending order, so we can use popitem to keep only 25 items
counter = {k: v for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)} 
print(counter) # This prints the words before removing, so we can have the data on our console
# The reason to keep only 25 elements is merely aesthetic, and because if we have more, matplotlib starts stacking the stuff
while (len(list(counter.keys())) > 25):
    counter.popitem() # Only works in versions up to 3.7, in 3.7 it removes the last element added which is the thing we want to do, if the version is lower it will remove a random dictionary completely breaking the system

# This now sorts by ascending order just for displaying it nicely on matplotlib
counter = {k: v for k, v in sorted(counter.items(), key=lambda item: item[1])} 


countervalues = list(counter.values())
countermin = min(countervalues)
countermax = max(countervalues)

# This implements random bar colors just for fun
# If you have the bad luck to get white, the bar will be invisible D:
randbarcolor = "#"+"".join(random.choice('0123456789ABCDEF') for i in range(6))
bar = plt.barh(*zip(*counter.items()), color=randbarcolor)
plt.xticks(range(countermin, countermax+1))
plt.title((results[int(selection)]))

#  This puts  the numbers in front of the letters in a barh
for rect in bar:
    width = rect.get_width()
    y = rect.get_y()
    plt.text(width+.2, y, width)

# This deletes the axis values from the bottom
plt.xticks([]) 

plt.show()
