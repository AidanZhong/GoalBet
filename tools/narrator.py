# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 23:40

@author: Aidan
@project: GoalBet
@filename: narrator
@description: 
- Python 
"""
from pathlib import Path
import openai

# Define the script for narration
script_text = """
Deep inside every one of us… lives an ancient beast --
a force that doesn't care about survival… but only about pleasure.

In 1953, James Olds discovered it by accident.
A rat… with an electrode misplaced in its brain… found a lever that gave it pleasure.
It pressed that lever thousands of times… forgetting food… forgetting sleep…
trapped in a cage of its own desire.

Years later, humans were tested too.
A patient… called B-19… begged doctors for “just a few more stimulations.”
The button of pleasure… became a prison.

For decades, we thought dopamine was the molecule of happiness.
But then Wolfram Schultz studied monkeys…
When the juice reward came, dopamine didn't fire.
Instead, it spiked at the light -- the promise of juice… and crashed when the reward failed.

Dopamine wasn't pleasure. It was expectation. The fuel of wanting… not liking.

Then Kent Berridge showed the truth:
The brain splits wanting… and liking.
Dopamine drives the chase. Endorphins fuel the joy.
Addiction is when wanting grows wild… while liking fades.

But there's hope.
In the 1980s, Bruce Alexander built Rat Park.
Rats given freedom, toys, and friends… ignored the drug water.
Even Vietnam soldiers, addicted in war, quit naturally when they returned home… to love, and to purpose.

Here's the lesson:
If your environment is a cage… desire will enslave you.
But if your environment is rich with meaning, connection, and growth… your ancient beast can be tamed -- and its power becomes fuel.

Don't just fight addiction to screens, to habits, to comfort.
Build your own Rat Park.
Surround yourself with people and purpose.
Create meaning so deep… that wanting serves you -- instead of controlling you.

Because freedom isn't the absence of desire. It's the mastery of it.
"""

# Generate TTS with OpenAI's gpt-4o-mini-tts (deep cinematic style)
output_file = Path("/mnt/data/motivation_voiceover.mp3")

with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",  # Alloy is deep & cinematic
        input=script_text
) as response:
    response.stream_to_file(output_file)

output_file.as_posix()
