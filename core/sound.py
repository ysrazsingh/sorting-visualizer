import numpy as np
import pygame
from .constants import MAX_VAL

_SOUND_CACHE: dict = {}


def make_tone(freq: int) -> pygame.mixer.Sound:
    freq = int(freq)
    if freq in _SOUND_CACHE:
        return _SOUND_CACHE[freq]

    sr       = 44100
    duration = 0.022          # 22 ms — audible but not lingering
    t        = np.linspace(0, duration, int(sr * duration), endpoint=False)

    # Pure sine wave — no harmonics, no artifacts
    wave = np.sin(2 * np.pi * freq * t)

    # Short linear fade-out (last 5 ms) to prevent clicks
    fade = int(sr * 0.005)
    wave[-fade:] *= np.linspace(1, 0, fade)

    audio = (wave * 0.30 * 32767).astype(np.int16)
    audio = np.column_stack((audio, audio))

    _SOUND_CACHE[freq] = pygame.sndarray.make_sound(audio)
    return _SOUND_CACHE[freq]


def beep(value: float) -> None:
    freq = int(300 + (max(0.0, min(float(value), MAX_VAL)) / MAX_VAL) * 900)
    make_tone(freq).play()
