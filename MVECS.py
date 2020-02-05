'''
    Project  : Stegenography
    Team No  : 10
    Members  : Prem Kumar
               Vasavi
               Gopi
               Pratyusha
    Language : Python
    Packages : OpenCV, AES in Crypto.Cipher, struct, os
'''

# Importing Packages
import cv2
from Crypto.Cipher import DES3
import struct
import os
import datetime
from speech_recognition import Recognizer,Microphone
from PIL import Image

#Creating to Audio File
def Audio():
    r = Recognizer()
    with Microphone() as source:
        print("Recording...")
        audio = r.record(source, duration=5)
        print("Recorded")
    open("audio.wav", "wb").write(audio.get_wav_data())

# Class for the Encryption
class Encryption:
    def __init__(self,key,infile,outfile):
        self.key=key
        self.infile=infile
        self.outfile=outfile
        self.chunksize=64*8192

    #Method for Encrypt File
    def Encrypt(self):
        if not self.outfile:
            self.outfile = self.infile + os.path.splitext(self.infile)[1]
        __iv = os.urandom(8) # Initialization Vector
        encryptor = DES3.new(self.key, DES3.MODE_CBC, __iv)
        filesize = os.path.getsize(self.infile)
        with open(self.infile, 'rb') as infile:
            with open(self.outfile, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(__iv)
                while True:
                    chunk = infile.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        spaces= b' '*(16 - len(chunk) % 16)
                        chunk += spaces
                    outfile.write(encryptor.encrypt(chunk))
# Class for the Decryption
class Decryption:
    def __init__(self,key,infile,outfile):
        self.key=key
        self.infile=infile
        self.outfile=outfile
        self.chunksize=64*8192

    #Method for Encrypt File
    def Decrypt(self):
        if not self.outfile:
            self.outfile = os.path.splitext(self.infile)[0]
        with open(self.infile, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            __iv = infile.read(8)
            decryptor = DES3.new(self.key, DES3.MODE_CBC, __iv)
            with open(self.outfile, 'wb') as outfile:
                while True:
                    chunk = infile.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))
                outfile.truncate(origsize)

ch=int(input("1 Encrypt to Image\n2 Decrypt from Image\n3 Exit\nChoose: "))
    
if(ch==1):
    print("Speak Now")
    Audio()
    img = cv2.imread("stega.png")
    outimg="stegnoid.png"
    key=input("Enter Key of length 24: ")
    while(len(key)!=24):
        print("Key length should be 24")
        key=input("Enter Key of length 24: ")
    print("Encrypting...")
    infile="audio.wav"
    time1=datetime.datetime.now()
    tech=Encryption(key,infile,"dec.wav")
    tech.Encrypt()
    print("Encryption of data Succeed... :)")
    file=open("dec.wav",'rb')
    Binary_Data=[]
    file.seek(0)
    length=len(file.read())
    file.seek(0)
    for i in range(0,length):
        byte=file.read(1)
        if(len(byte)!=0):
            decimal=ord(byte)
            Binary_Data.append(f'{decimal:08b}')
        else:
            break
    maximum=len(img[0])*len(img)
    if(maximum>=len(Binary_Data)*2):
        print("Sufficient Pixels")
    else:
        print("Insufficient Pixels")
        exit(0)
    total=0
    row=0
    col=0
    index=0
    print("Storing data to Image...")
    for data in Binary_Data:
        num=0
        while(num<8):
            #print(row,col,index)
            img[row][col][index]=int(f'{img[row][col][index]:08b}'[:4]+data[num:num+4],2)
            num+=4
            index+=1
            total+=1
            if(index==3):
                col+=1
                index=0
            if(col==len(img[0])):
                row+=1
                col=0
    file.close()
    print("Updated Pixels Count: ",total)
    #os.remove("dec.wav")
    print("Data Stored.")
    cv2.imwrite(outimg,img)
    cv2.imshow('stega',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    image = Image.open('stegnoid.png')
    image.save('shrink.png',quality=10,optimize=True)
    os.remove('stegnoid.png')
    print("Image Created")
    print("Time Taken: ",(datetime.datetime.now()-time1).total_seconds(),"Seconds\n")

elif(ch==2):
    img=cv2.imread("shrink.png")
    total=int(input("Total nof Pixels: "))
    key=input("Enter Decryption Key: ")
    time1=datetime.datetime.now()
    outfile="output.wav"
    data=""
    row=0
    col=0
    index=0
    print("Reading data from Image")
    while(total>0):
        data=data+f'{img[row][col][index]:08b}'[4:]
        index+=1
        total-=1
        if(index==3):
            col+=1
            index=0
        if(col==len(img[0])):
            row+=1
            col=0
    length=int(len(data)/8)
    print("Data Read Completed")
    index=0
    mine=[]
    while(length>0 and index<len(data)):
        mine.append(int(data[index:index+8],2))
        index+=8
        length-=1
    file=open("decrypted.wav",'wb')
    binarymine=bytearray(mine)
    file.write(binarymine)
    file.close()
    tech=Decryption(key,"decrypted.wav",outfile)
    tech.Decrypt()
    os.remove("decrypted.wav")
    print("Successfully Data Retrieved")
    print("Time Taken: ",(datetime.datetime.now()-time1).total_seconds(),"Seconds\n")
