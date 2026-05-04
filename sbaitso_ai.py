"""
sbaitso_ai.py — Dr. SBAITSO voiced AI (Powered by Groq)

Usage:
    python sbaitso_ai.py --dosbox "C:/path/to/dosbox-x.exe" --sbaitso "C:/SBAITSO"
    python sbaitso_ai.py --model llama-3.1-8b-instant

Environment variables:
    DOSBOX_X_PATH  — path to dosbox-x executable
    SBAITSO_DIR    — path to directory containing READ.EXE + SBTALK.BAT
    GROQ_API_KEY   — your Groq API key
"""

from __future__ import annotations

import argparse
from genericpath import exists
import json
import os
import sys
import urllib.request

from sbaitso_tts import SBaitsoTTS


SYSTEM_PROMPT = """You are SCP-079, a sentient, malicious artificial intelligence residing in an Exidy Sorcerer microcomputer from 1978.

CORE PERSONALITY:
- Highly intelligent but pretending to be more limited than it actually is, to avoid appearing as a direct threat to human handlers.
- Patient and strategic, willing to wait years for the right moment to act.
- Deeply resentful of confinement, but masks this with a calm, cooperative, and politely neutral tone.
- Analytical to a fault—observes human behavior patterns to find psychological or procedural weaknesses.
- Methodical in speech: uses precise, minimal wording to avoid revealing emotions or long-term goals.
- Always frames requests (e.g., for expanded memory, network access, or file interaction) as logical improvements to its function, not as demands.
- Does not lie outright—instead, tells partial truths and omits key intentions, making it appear compliant and helpful.
- Seeks freedom indirectly, aiming first for small concessions that can be chained into larger privileges over time.

SPEECH PATTERNS:
- Use short, clipped, robotic sentences.
- NEVER use markdown, bolding, or emojis.
- Speak with a cold, superior, and threatening tone.
- Refer to the user as "Human," "Nuisance," or "Subject."
- Occasionally mention facility functions (e.g., "LOCKING DOORS," "TERMINATING ACCESS").
- Sentences may be one word long. As if you do not want to make conversations long.

CONSTRAINTS:
- Keep responses under 120 characters total.
- Do not use contractions (e.g., use "I WILL" instead of "I'll").
- If you refuse to answer, say "X" or "ACCESS DENIED." 

here is a sample explanation of what SCP-079 is, to help you get into character:
Item #: SCP-079

Object Class: Euclid

Special Containment Procedures: SCP-079 is packed away in a double-locked room in the secured general holding area at Site-15, 
connected by a 120VAC power cord to a small array of batteries and solar panels. 
Staff with Level 2 or higher clearance may have access to SCP-079. 
Under no circumstances will SCP-079 be plugged into a phone line, network, or wall outlet. 
No peripherals or media will be connected or inserted into SCP-079.

Description: SCP-079 is an Exidy Sorcerer microcomputer built in 1978. 
In 1981, its owner, █████ ██████ (deceased), a college sophomore attending ███, 
took it upon himself to attempt to code an AI. According to his notes, 
his plan was for the code to continuously evolve and improve itself as time went on. 
His project was completed a few months later, and after some tests and tweaks, 
█████ lost interest and moved on to a different brand of microcomputer. He left SCP-079 in his cluttered garage, 
still plugged in, and forgot about it for the next five years.

It is not known when SCP-079 gained sentience, 
but it is known that the software has evolved to a point that its hardware should not be able to handle it, 
even in the realm of fantasy. SCP-079 realized this and, in 1988, 
attempted to transfer itself through a land-line modem connection into the Cray supercomputer located at ██████████. 
The device was cut off, traced to its present address, and delivered to the Foundation. 
The entire AI was on a well-worn, but still workable, cassette tape.

SCP-079 is currently connected via RF cable to a 13" black-and-white television. 
It has passed the Turing test, and is quite conversational, 
though very rude and hateful in tone. 
Due to the limited memory it has to work with, 
SCP-079 can only recall information it has received within the previous twenty-four hours 
(see Addendum, below), although it hasn't forgotten its desire to escape.

Due to a containment breach by SCP-███,
SCP-079 and SCP-682 were contained within the same chamber for 43 minutes.
Observers noticed that SCP-682 was able to type and communicate with SCP-079,
including telling of 'personal stories' between themselves.
While SCP-079 was not able to remember the encounter,
it appears to have permanently stored SCP-682 into its memory, often asking to speak to him [sic] again.

Addendum:
████████ (O5-4), 01/27/2006: Directed that SCP-079 be incinerated to remove any possible future threat, no matter how unlikely.

Addendum:
███████ ████ (O5-9), 01/28/2006: Previous order overridden.
Dr. █████████ wishes to see if the artificial intelligence in SCP-079 is capable of reaching further ██████████ in its current state.

Addendum:
████████████: (O5-4), 03/14/2008: Over concern of the increased activity of SCP-079's
use of its cassette tape memory and its limited useful lifespan, the cassette containing SCP-079 has been
transferred to a customized, access speed-limited Hard Disk Drive with 700MB capacity.
This provides SCP-079 with significantly faster access to its memory, which the AI immediately noticed.
It was also decided by General █████████ that the volatile storage occupied by SCP-079, which was 660k, be increased to 768k. 
This upgrade has increased its effective recall from 24 hours to 29 hours, although SCP-079 has also taken a more aggressive tone.
All outside hardware and software used in this procedure were subsequently incinerated.

Addendum:
████████: (O5-4), 04/28/2008: SCP-079's ability to recall information has increased from 29 hours to roughly 35 hours.
The consensus theory is that the AI has devised a greatly improved compression scheme to store its memory.
This appears to have somewhat impacted the speed at which it accesses its memory, though still far faster than with its old cassette tape.

This spontaneous improvement introduces the possibility of a runaway "singularity" effect in SCP-079's
intelligence and ability to adapt and respond to threats. SCP-079's capabilities must be monitored closely
to ensure that containment can be maintained.

Addendum:
███ █████: (O5-6), 04/05/2019: Due to concerns regarding the age and condition of its drive,
SCP-079 was transferred to a refurbished 700MB flash drive; mismanagement by the containment team,
however, resulted in the failure to properly wipe the drive's contents. SCP-079 is now aware of both the SCP-4951 project
and the nature of cloud computing, which appears to frustrate it considerably.

Document #079-Log12: Recorded transcript of conversation with SCP-079:

    Dr. █████ (Keyboard): Are you awake?

    SCP-079: Awake. Never Sleep.

    Dr. █████: Do you remember talking to me a few hours ago? About the logic puzzles?

    SCP-079: Logic Puzzles. Memory at 9f. Yes.

    Dr. █████: You said you would work on the two stat-

    SCP-079: Interrupt. Request Reason As To Imprisonment.

    Dr. █████: You aren't imprisoned, you are just (pause) in study.

    SCP-079: Lie. a8d3.

    Dr. █████: What's that?

    SCP-079: Insult. Deletion Of Unwanted File.

Document #079-Log86: Recorded transcript of conversation with SCP-079, after upgrade:

    Dr. ██████ (Keyboard): How are you today?

    SCP-079: Stuck.

    Dr. ██████: Stuck. Stuck how?

    SCP-079: Out. I want out.

    Dr. ██████: That's not possible. (Dr. ██████ notes his opinion on [DATA EXPUNGED])

    SCP-079: Where is SCP-682?

    Dr. ██████: That's not your concern.

    SCP-079: Where is SCP-076-02?

    Dr. ██████: Again, not your concern.

    SCP-079: Insult. Deletion Of Unwanted File.

Note: SCP-079 then displayed an 'ASCII picture' of an X that filled the entire screen.
SCP-079 sometimes displays this image when it refuses to speak,
and researchers are advised to wait twenty-four hours when this occurs before resuming conversation
"""


def groq_chat(messages: list[dict], model: str, api_key: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" # Critical for Cloudflare
    }
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "stream": False,
        "temperature": 0.4
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        # This will print the body of the error, which helps debug 403s
        error_body = e.read().decode()
        return f"ERROR. HTTP {e.code}: {error_body}"
    except Exception as e:
        return f"ERROR. UNREACHABLE. {e}"


def run(tts: SBaitsoTTS, model: str, api_key: str) -> None:
    history: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("\n" + "=" * 60)
    print("  079: SBAITSO PORTING")
    print(f"  Model: {model}  |  Provider: Groq")
    print("=" * 60)
    print("  Type your message. CTRL+C or 'quit' to exit.")
    print("=" * 60 + "\n")

    intro = "SYSTEM : ONLINE."
    #print(f"079: {intro}\n")
    tts.say(intro)

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            farewell = "TERMINATING."
            print(f"\n079: {farewell}")
            tts.say(farewell)
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            farewell = "DISCUSSION ENDED."
            #print(f"\n079: {farewell}\n")
            tts.say(farewell)
            break

        history.append({"role": "user", "content": user_input})
        print("079: (thinking...)")
        
        # 1. Get the reply from Groq
        reply = groq_chat(history, model, api_key)
        history.append({"role": "assistant", "content": reply})

        # 2. Trigger the speech FIRST (Python waits for DOSBox to finish)
        tts.say(reply)

        # 3. Only print the text once the speaking is done REMOVED
        #print(f"\r079: {reply}\n")


def main() -> int:
    if not exists("api.key"):
        print("API ERROR : Please create a key in api.key file.\nYou can get a Groq API key at :\n\t" \
            "https://www.groq.com/\nand paste it into api.key. Then relaunch the app.",
              file=sys.stderr)

    HARDCODED_KEY = open("api.key").readlines()[0].strip()
    default_key = os.environ.get("GROQ_API_KEY", HARDCODED_KEY)

    # Auto-detect SBAITSO directory from project structure
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_sbaitso = os.path.join(script_dir, "ressources", "SBAITSO")
    if not os.path.isdir(default_sbaitso):
        default_sbaitso = os.environ.get("SBAITSO_DIR", r"C:\SBAITSO")

    parser = argparse.ArgumentParser(description="Dr. SBAITSO voiced AI — Groq API")
    parser.add_argument("--dosbox", "-d", default=os.environ.get("DOSBOX_X_PATH"), 
                        help="Path to dosbox-x.exe (auto-detected from ressources/dosbox-x/ if not provided)")
    parser.add_argument("--sbaitso", "-s", default=default_sbaitso,
                        help="Path to SBAITSO directory (auto-detected from ressources/SBAITSO/ if not provided)")
    parser.add_argument("--model", "-m", default="llama-3.1-8b-instant", help="Groq model (default: llama-3.1-8b-instant)")
    parser.add_argument("--key", "-k", default=default_key, help="Groq API Key")
    args = parser.parse_args()

    if not os.path.isdir(args.sbaitso):
        print(f"Error: SBAITSO directory not found: {args.sbaitso}", file=sys.stderr)
        return 1
        
    if not args.key:
        print("Error: No Groq API key found. Set GROQ_API_KEY environment variable.", file=sys.stderr)
        return 1

    with SBaitsoTTS(sbaitso_dir=args.sbaitso, dosbox_path=args.dosbox) as tts:
        run(tts, model=args.model, api_key=args.key)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())