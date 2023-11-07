from piano_tools import play_note
import mido

with mido.open_input() as port:
    for message in port:
        if message.velocity != 0:
            play_note(message.note)