# -*- coding: utf-8 -*-


import scipy.signal
import sys
import PIL
import numpy
import scipy.io.wavfile



class APT(object):


    muestras = 20800


    def __init__(self, filename):

#---------------- Abre y verifica si la el archivo de audio está muestreada a la frecuencia correcta-------------------#

        (rate, self.signal) = scipy.io.wavfile.read(filename)
        if rate != self.muestras:
            raise Exception("Debe usar el muestreo correcto {}".format(self.muestras))
        truncar = self.muestras * int(len(self.signal) // self.muestras)
        self.signal = self.signal[:truncar]


    def _digitize(self, signal, plow=0.5, phigh=99.5):

#----------------Convierte la señal a numeros entre 0 y 255--------------------------------------------------------------#        
       
        (low, high) = numpy.percentile(signal, (plow, phigh))
        delta = high - low
        data = numpy.round(255 * (signal - low) / delta)
        data[data < 0] = 0
        data[data > 255] = 255
        return data.astype(numpy.uint8)


    def decode(self, outfile=None):

#----------------Digitaliza el archivo de audio a una matriz de puntos--------------------------------------------------#

        hilbert = scipy.signal.hilbert(self.signal)
        filtered = scipy.signal.medfilt(numpy.abs(hilbert), 5)
        reshaped = filtered.reshape(len(filtered) // 5, 5)
        digitized = self._digitize(reshaped[:, 2])
        matrix = self._reshape(digitized)
        image = PIL.Image.fromarray(matrix)
        if not outfile is None:
            image.save(outfile)
        image.show()
        return matrix



    def _reshape(self, signal):


#-------Busca las barras de sincronizacion que trae por defecto las imagenes APT y convierte
#       la señal que está en 1ra dimension en una imagen en 2da dimensión mediante la
#       correlacion cruzada que existe entre la señal y las barras de sincronización---------#
       
        syncA = [0, 128, 255, 128]*7 + [0]*7

#       lista maxima de correlaciones encontradas
        peaks = [(0, 0)]

        # distancia mínima entre picos
        mindistance = 2000
        signalshifted = [x-128 for x in signal]
        syncA = [x-128 for x in syncA]
        for i in range(len(signal)-len(syncA)):
            corr = numpy.dot(syncA, signalshifted[i : i+len(syncA)])

            
#           Si el pico de señal es demasiado lejos entonces añadirse como uno uno nuevo
            if i - peaks[-1][0] > mindistance:
                peaks.append((i, corr))

            
            elif corr > peaks[-1][1]:
                peaks[-1] = (i, corr)

        
#       Crear una imagen o matriz de puntos a partir de los picos de señal encontrados        
        matrix = []
        for i in range(len(peaks) - 1):
            matrix.append(signal[peaks[i][0] : peaks[i][0] + 2080])

        return numpy.array(matrix)


if __name__ == '__main__':
    apt = APT(sys.argv[1])

    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    else:
        outfile = None
    apt.decode(outfile)
