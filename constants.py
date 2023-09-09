from pyaudio import paInt16

CHUNK = 1024          # форма ауди-сигнала
FRT = paInt16         # шестнадцатибитный формат для задания амплитуды
CHAN = 2              # каналы записи звука
RT = 44100            # частота
REC_SEC = 5           # длина записи
OUTPUT = "output.wav" # имя выходного файля

RED = '#E21A1A'
