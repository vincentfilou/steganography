from PIL import Image, ImageFilter

#renvoie le nieme bit d'une chaine de caracteres
def getBit(string,n):
    byteIndex = int(n/8)
    bitIndex = n % 8
    return ((ord(string[byteIndex])>>(7-bitIndex)) &0x1) 

#transforme un tableau de 8 éléments en un caractere
def bitArrayToChar(bitArray):
    assert( len(bitArray) == 8 )
    char = 0
    for index in range(0,8):
        char += bitArray[index]<<(7-index)
    return chr(char)

#transforme un tableau dont la taille est un multiple de 8 en une chaine de caracteres
def bitArrayToString(bitArray):
    assert( len(bitArray)%8 == 0 )
    string = ""
    for index in range(0,len(bitArray),8):
        string += bitArrayToChar(bitArray[index:index+8])
    return string

#test le resultat
def test_bitArrayToString(string):
    bitArray = []
    for index in range(0,len(string) * 8):
        bitArray.append(getBit(string,index))
    assert(bitArrayToString(bitArray) == string)

def encode_size(n,size):
    #definition of the format: a string of bits, of minimum size n
    ft = '{0:0'+str(n)+'b}'
    return ft.format(size)

def encodeBit(value,bit):
    if bit == 1:
        return value | 0x1
    if bit == 0:
        return value & ~0x1
    raise Exception()

def encode(image,string):
    assert(len(image.getbands()) == 3)
    numBits = len(string) * 8
    (width,height) = image.size
    encoded_size = encode_size(width,numBits)
    #if we cannot encode the size in width bits
    # or if the image is too small to contain our text 
    if (width < len(encoded_size)) or (height < numBits/width): 
        raise Exception("Image too small")
    for row in range(0,width):
        r,g,b = image.getpixel((row,0))
        image.putpixel((row,0), (r,g,encodeBit(b,int(encoded_size[row]))))
    line = 1
    row = 0
    bitIndex = 0
    while bitIndex < numBits:
        line = 1+ int(bitIndex/width)
        row = bitIndex % width
        (r,g,b) = image.getpixel((row,line))
        image.putpixel((row,line),(r,g,encodeBit(b,getBit(string,bitIndex))))
        bitIndex += 1
    return image

def decode(image):
    assert(len(image.getbands()) == 3)
    bits = []
    (width,height) = image.size
    size = 0
    for row in range(0,width):
        r,g,b = image.getpixel((row,0))
        size = (size<<1)|(b&0x1)
    print(size)
    bitIndex = 0
    while bitIndex < size:
        line = 1+ int(bitIndex/width)
        row = bitIndex % width
        (r,g,b) = image.getpixel((row,line))
        bits.append(b&0x1)
        bitIndex += 1
    return bitArrayToString(bits)

img = Image.open("rarebeat.jpg")
encode(img,"rabbit\tegg\nspam100").save("rarebeat.png")
img2 = Image.open("rarebeat.png")
print(decode(img2))
