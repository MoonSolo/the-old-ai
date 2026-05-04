# SBAITSO TTS Synthesizer

SBAITSO TTS is a reverse-engineered, formant-based speech synthesizer inspired by the original Dr. SBAITSO text-to-speech program. It is implemented in portable C and is intended for educational and nostalgic use.

## Project Description

This repository contains an independent implementation of a vintage-style synthetic speech engine. It generates 16-bit mono WAV audio using a mathematical model of the vocal tract and ARPABET phonemes rather than modern machine learning techniques.

The project is not affiliated with, endorsed by, or owned by the creators of the original Dr. SBAITSO program.

## Disclaimer

- The original Dr. SBAITSO program and associated intellectual property remain the property of their respective rights holders.
- This project does not claim ownership of the original software, brand, or audio assets.
- The included TTS implementation is a reverse-engineered recreation intended for research, preservation, and experimentation.

## Features

- Formal formant synthesis engine with controlled formant frequencies and bandwidths
- Support for 44 ARPABET phonemes covering English speech sounds
- Vintage robotic voice character with minimal co-articulation and steady pitch
- Pure C implementation with no external runtime dependencies
- 22050 Hz 16-bit PCM WAV output by default
- Cross-platform build support for Windows, Linux, and macOS

## Requirements

- Windows: MinGW, MSVC, or compatible C compiler
- Linux/macOS: GCC or Clang

## Building

### Windows Batch

```cmd
build.bat
```

### Makefile (Windows, Linux, macOS)

```bash
make
```

### CMake (Cross-platform)

```bash
mkdir build
cd build
cmake ..
cmake --build .
```

## Usage

```bash
./tts "Your text here"
./tts "Hello world" output.wav
```

### Examples

```bash
./tts "Hello, how are you today?"
./tts "I am SBAITSO" sbaitso_intro.wav
./tts "Good day. I am SBAITSO. How can I help you?" greeting.wav
```

## Design Overview

### Synthesis Model

The engine uses a formant synthesis approach that models speech production as a sequence of phonemes. Each phoneme is defined by:

- F1, F2, F3 target frequencies
- Bandwidth and resonance properties
- Voicing state (voiced or unvoiced)
- Relative amplitude
- Default duration

### Signal Generation

- Voiced phonemes are synthesized from sine waves at the formant frequencies plus a steady fundamental frequency (F0)
- Unvoiced phonemes use filtered noise shaped by the same formant structure
- Envelope shaping is applied with brief attack and release phases to create a mechanical, retro vocal quality

### Output

- 16-bit signed PCM
- 22050 Hz sample rate
- Mono channel

## Architecture

```
src/
├── main.c              # CLI interface and entry point
├── phonemes.c          # Phoneme definitions and ARPABET parsing
├── synthesizer.c       # Formant synthesis engine and waveform generation
├── wav.c               # WAV file output
└── text_to_phoneme.c   # Text normalization and phoneme conversion

include/
├── phonemes.h
├── synthesizer.h
├── wav.h
└── text_to_phoneme.h
```

## Phoneme Set

- Vowels: AA, AE, AH, AO, AW, AY, EH, ER, EY, IH, IY, OW, OY, UH, UW
- Semivowels: L, R, W, Y
- Fricatives: F, S, SH, TH, DH, V, Z, ZH
- Affricates: CH, JH
- Stops: K, P, T, B, D, G
- Nasals: M, N, NG
- Special: SIL (silence/pause)

## Dictionary

The text-to-phoneme converter includes a limited dictionary of common English words. Words that are not present in the dictionary are handled conservatively to preserve intelligibility.

## Customization

### Adjust Sample Rate

Modify `SAMPLE_RATE` in `include/synthesizer.h`:

```c
#define SAMPLE_RATE 11050  /* Use a lower sample rate for a more retro sound */
```

### Modify Phoneme Parameters

Change formant frequencies and bandwidths in `src/phonemes.c` to alter the voice timbre.

### Extend the Dictionary

Add entries in `src/text_to_phoneme.c`:

```c
{"word", "W ER D"},
```

### Change Voice Behavior

Adjust synthesis parameters in `src/synthesizer.c`, such as:

- `f0` for base pitch
- `formant_amplitude` for overall loudness
- envelope attack and release values

## Known Limitations

- Monotonic pitch without natural prosody
- Limited vocabulary and dictionary coverage
- Simple co-articulation, producing a deliberately mechanical sound
- Formant-based synthesis is not equivalent to modern neural TTS systems

## Original SBAITSO Capture

This project also documents a pathway for running the original SBAITSO program inside DOSBox‑X and capturing authentic WAV output. This workflow is provided for comparison and preservation, not as a claim of ownership.

## References

- ARPABET phoneme set
- Klatt, D. H. (1980). "Software for a cascade/parallel formant synthesizer"
- Dr. SBAITSO, Sensible Software (1990s)

## License and Ownership

This repository is a reverse-engineered recreation for education and archival purposes. The original Dr. SBAITSO application and trademark are not owned by this project.

## Credits

Inspired by the original Dr. SBAITSO speech synthesizer and the early era of vintage text-to-speech technology.

