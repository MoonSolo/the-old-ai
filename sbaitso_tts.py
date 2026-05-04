"""
sbaitso_tts.py — SBAITSO TTS

Spawns a fresh DOSBox-X process per sentence.
No polling loops, no IPC files — just mount, sbtalk, read, exit.
Matches exactly what you'd type manually.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import textwrap
import time
from pathlib import Path


def _find_dosbox() -> str | None:
    """
    Find dosbox-x executable in the following priority order:
    1. ressources/dosbox-x/ subfolder (bundled with project)
    2. Script directory (if dosbox-x executable is placed there)
    3. System PATH
    4. Common installation locations
    """
    script_dir = Path(__file__).parent
    
    # Priority 1: Check ressources/dosbox-x/ subfolder (project bundle)
    dosbox_bundle_dir = script_dir / "ressources" / "dosbox-x"
    if dosbox_bundle_dir.exists():
        for name in ["dosbox-x.exe", "dosbox-x_sdl2.exe", "dosbox-x_MinGWx64_SDL2.exe", "dosbox-x_MinGWx64_SDL1.exe"]:
            p = dosbox_bundle_dir / name
            if p.exists():
                return str(p)
    
    # Priority 2: Check script directory
    for name in ["dosbox-x.exe", "dosbox-x_sdl2.exe", "dosbox-x_MinGWx64_SDL2.exe", "dosbox-x_MinGWx64_SDL1.exe"]:
        p = script_dir / name
        if p.exists():
            return str(p)
    
    # Priority 3: System PATH
    found = shutil.which("dosbox-x")
    if found:
        return found
    
    # Priority 4: Common installation locations
    common_paths = [
        r"C:\Program Files\dosbox-x\dosbox-x.exe",
        r"C:\dosbox-x\dosbox-x.exe",
    ]
    for c in common_paths:
        if os.path.exists(c):
            return c
    
    return None


def _chunk_text(text: str, max_chars: int = 120) -> list[str]:
    import re
    import textwrap
    
    # 1. Standardize: uppercase and normalize whitespace
    # Preserve ALL punctuation (. ! ? , ; : - etc.) for TTS
    text = text.upper().strip()
    # Only remove problematic characters for DOS/READ.EXE
    for ch, rep in [("\n", " "), ("\r", " ")]:
        text = text.replace(ch, rep)
    
    # Normalize multiple spaces to single space
    text = re.sub(r'\s+', ' ', text)
    parts = re.split(r'(?<=[.!?])\s+', text) # removed :;,
    
    sentences = []
    for raw in parts:
        raw = raw.strip()
        if not raw:
            continue
            
        # Keep all punctuation in display
        if len(raw) <= max_chars:
            sentences.append(raw)
        else:
            # If a segment is still too long, wrap it by words
            for line in textwrap.wrap(raw, max_chars, break_long_words=False):
                sentences.append(line)
                
    return sentences


def _make_conf(sbaitso_dir: str, text: str) -> str:
    """Generate a DOSBox config that mounts, loads sbtalk, speaks text, and exits."""
    sbaitso_abs = os.path.abspath(sbaitso_dir)
    # Minimal escaping: only remove single quotes which break the READ command
    # All other punctuation (. ! ? , ; : - etc.) is preserved for natural TTS
    safe_text = text.replace("'", "")

    lines = [
        "[sdl]",
        "[dosbox]",
        "machine=cga",
        "[sblaster]",
        "[autoexec]",
        "@ECHO OFF",
        "SET BLASTER=A220 I7 D1 T4",
        'MOUNT T "' + sbaitso_abs + '"',
        "T:",
        "SBTALKER /dBLASTER",
        'READ "' + safe_text + '"',
        "EXIT",
    ]

    tmpdir = tempfile.mkdtemp(prefix="sbaitso_")
    conf_path = os.path.join(tmpdir, "speak.conf")
    with open(conf_path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lines))
    return conf_path


class SBaitsoTTS:
    """
    SBAITSO TTS — spawns a DOSBox process per utterance.

    Parameters
    ----------
    sbaitso_dir : str
        Directory containing READ.EXE, SBTALKER.EXE, SBTALK.BAT.
    dosbox_path : str | None
        Path to dosbox-x executable.
    timeout : float
        Max seconds to wait for DOSBox to finish speaking.
    """

    def __init__(
        self,
        sbaitso_dir: str,
        dosbox_path: str | None = None,
        timeout: float = 30.0,
    ):
        self.sbaitso_dir = sbaitso_dir
        self.dosbox_path = dosbox_path or _find_dosbox()
        self.timeout = timeout

    def start(self) -> None:
        if not self.dosbox_path or not os.path.exists(self.dosbox_path):
            raise RuntimeError("dosbox-x not found.")
        print("079 ready.")

    def stop(self) -> None:
        print("079 stopped.")

    def __enter__(self) -> "SBaitsoTTS":
        self.start()
        return self

    def __exit__(self, *_) -> None:
        self.stop()

    def say(self, text: str) -> None:
        chunks = _chunk_text(text)
        for chunk in chunks:
            self._speak(chunk)

    def say_async(self, text: str) -> None:
        import threading
        threading.Thread(target=self.say, args=(text,), daemon=True).start()

    def _speak(self, text: str) -> None:
        """Spawn DOSBox, speak one chunk, wait for it to finish."""
        conf = _make_conf(self.sbaitso_dir, text)
        cmd = [self.dosbox_path, "-conf", conf]
        print(f"079: {text!r}")
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 6 # SW_MINIMIZE
        proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE, startupinfo=si)
        
        # Calculate timeout proportional to text length
        char_count = len(text)
        dynamic_timeout = max(20.0, 5.0 + (char_count * 0.1))
        
        try:
            proc.wait(timeout=dynamic_timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            raise TimeoutError(f"DOSBox timed out speaking ({dynamic_timeout:.1f}s): {text!r}")
        finally:
            # <-- Clean up temp conf
            try:
                shutil.rmtree(os.path.dirname(conf))
            except Exception:
                pass