# SCP-079 AI Fan Project

This repository is a fan-made Windows port of an SCP-079–inspired conversational AI interface. It combines a Groq-based GPT-style chat workflow with SBAITSO text-to-speech playback via DOSBox-X.

## Overview

- The core behavior is driven by `sbaitso_ai.py`, which uses a Groq chat completion model to simulate SCP-079.
- Speech output is produced by `sbaitso_tts.py`, which launches DOSBox-X and drives the original `READ.EXE` from the bundled `ressources/SBAITSO` directory.
- The launcher is `launch_sbaitso.bat`, which starts `launch_sbaitso.ps1` and handles dependency checks.

## Important Disclaimer

- This project is a fan-made recreation and is not affiliated with the SCP Foundation.
- The SCP-079 character, related lore, and trademarks belong to the SCP community.
- The SBAITSO TTS assets are not owned by this project and remain the property of their original rights holders.

## Requirements

- Windows 10 / 11
- Python installed and available on `PATH`
- DOSBox-X executable available in `ressources/dosbox-x/` or on `PATH`
- Groq API key
- `ressources/SBAITSO/` containing `READ.EXE`, `SBTALKER.EXE`, `SBTALK.BAT`, and related files

## Running the Project

### Recommended: Double-click `launch_sbaitso.bat`

This is the intended startup method. The batch file launches the PowerShell launcher with execution policy bypass and performs dependency checks.

### Alternative: Run the PowerShell launcher directly

```powershell
powershell -ExecutionPolicy Bypass -File launch_sbaitso.ps1
```

## API Key Setup

The launcher can prompt for your Groq API key and optionally save it to your Windows user environment variables.

You may also provide the key via:

- `GROQ_API_KEY` environment variable
- `api.key` file in the repository root

## How It Works

1. `launch_sbaitso.bat` / `launch_sbaitso.ps1` validates the environment.
2. `sbaitso_ai.py` loads the SCP-079 system prompt and user conversation history.
3. Chat responses are generated through Groq’s chat completions endpoint.
4. `sbaitso_tts.py` converts the response text into speech by launching DOSBox-X with a temporary config that runs `READ.EXE`.

## Project Structure

- `sbaitso_ai.py` — main application logic and Groq chat integration
- `sbaitso_tts.py` — DOSBox-X based TTS wrapper for SBAITSO speech
- `launch_sbaitso.bat` — easy double-click launcher for Windows
- `launch_sbaitso.ps1` — dependency checker and startup helper
- `ressources/dosbox-x/` — bundled DOSBox-X binaries
- `ressources/SBAITSO/` — original SBAITSO runtime files
- `api.key` — optional file for storing the Groq API key

## Usage

Once launched, type messages into the console. Common session commands:

- `quit`
- `exit`
- `bye`

The assistant will speak responses using the bundled SBAITSO voice.

## Notes

- The voice synthesis uses the original DOS-based `READ.EXE` program via DOSBox-X.
- The repository is intended to be a Windows-compatible fan port, not a reimplementation of the original IBM PC software.
- The `.bat` launcher is the simplest way to start the application.

## Acknowledgements

- SCP Foundation community content and SCP-079 character inspiration
- Dr. SBAITSO for the classic vintage TTS style
- Groq for the chat completion model endpoint

## License

This repository is provided as a fan project and a technical demonstration. It does not claim ownership of SCP-079, the SCP Foundation IP, or the original SBAITSO software.
