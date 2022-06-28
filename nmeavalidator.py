import re
from tqdm import tqdm
import codecs

# Example string

# $GPGGA,054917.000,5100.0000,N,00400.0000,E,1,06,1.23,-24.7,M,47.1,M,,*71

# Match only lines starting with $ and ending with *<checksum>

# pattern = re.compile("^\$(.*)\*[0-9a-fA-F]{2}")

#put file name which you want to check
with open("220620_min.log", 'r') as f:
    for line in f:
        # print(line)
        #GPGLL,3539.12138653,N,13946.26305002,E,005729.00,A,D
        nmea_data = re.search(r'\$(.*)\*', line)
        # *6F
        checksum = re.search(r'\*(.*)', line)

        # if nmea_data:
        #     print(nmea?data.group(1))
        # if checksum:
        #     print(checksum.group())
# Calculate XOR sum, print only invalid lines
        sum = 0
        if nmea_data:
            # print(nmea.group())
            for char in nmea_data.group(1):

                sum = sum ^ ord(char)
                # print('{:02X}'.format(sum))
        if checksum:
            if '{:02X}'.format(sum) != checksum.group(1):
                print(line, end='')