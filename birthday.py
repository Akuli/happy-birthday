# happy birthday zaab :)

import array
import io
import math
import subprocess
import wave


# these frequencies are in hertz
a = 220
g = a * 2**(-2/12)
h = a * 2**(2/12)   # also known as b in some other countries
c = a * 2**(3/12)
d = a * 2**(5/12)
e = a * 2**(7/12)
f = a * 2**(8/12)
G = a * 2**(10/12)   # 1 octave higher than lower-case g
A = a * 2**(12/12)
C = a * 2**(15/12)


SAMPLERATE = 16000
SAMPLEWIDTH = 2
NOTE_DURATION = 0.15   # seconds


happy_birthday = [     # flake8: noqa

                      g, 0, g,
    c, 0, c, c, 0, c, c, a, g,
    h, d, e, G, G, e, d, d, 0,
    G, 0, G, e, e, d, e, e, G,
    e, e, e, f, f, f, G, G, G,
    C, 0, C, C, C, A, G, G, c,
    f, f, f, e, e, e, d, d, d,
    e, 0, g, g, g, g, d, d, d,
    c
]


def notes2samples(notes):
    for frequency in notes:
        samples_len = int(SAMPLERATE * NOTE_DURATION)
        for samplenumber in range(samples_len):
            time = samplenumber / SAMPLERATE
            yield math.sin(math.tau * frequency * time)


def sample2int16(floating):
    assert -1 <= floating <= 1

    if floating > 0:
        return round(0x7fff * floating)
    return round(0x8000 * floating)


def samples2bytes(samples):
    return array.array('h', map(sample2int16, samples)).tobytes()


def samples2wav(samples):
    fakefile = io.BytesIO()

    with wave.open(fakefile, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLERATE)
        wav.writeframes(samples2bytes(samples))

    return fakefile.getvalue()


def main():
    wav = samples2wav(notes2samples(happy_birthday))
    subprocess.run(['aplay'], input=wav)


if __name__ == '__main__':
    main()
