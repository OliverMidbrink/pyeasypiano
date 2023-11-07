from mido import MidiFile
from note_mappings_midi import note_mappings_dict_midi
from subprocess import Popen
from playsound import playsound
from play_sounds import play_file, DEFAULT_SONG
import time
import numpy as np

def play_note_jupyter(note_midi_number):
    Popen(['afplay', note_mappings_dict_midi[note_midi_number]])

def play_note(note_number):
    play_file(note_mappings_dict_midi[note_number], block=False)
    
def play_chord(origin_note, major=True):
    y = 4 if major else 3
    
    play_note(origin_note)
    play_note(origin_note + y)
    play_note(origin_note + 7)
        
def play_midi(file_name, save=True):
    mid = MidiFile(file_name, clip=True)
    timestamp = time.time()
    
    data = []
    
    for msg in mid.play():
        try:
            if msg.velocity == 0:
                continue
            
            # - 20 because of midi numbering
            play_file(note_mappings_dict_midi[msg.note], block=False)
            
            # Make timestamp
            time_delta = time.time() - timestamp
            timestamp=time.time()
            
            # Append data (midi numbering)
            data_point = [msg.note, time_delta]
            data.append(data_point)
            
            #print(np.array(data_point))
            #print(msg)
        except:
            #print(msg)
            pass
        
    # Save data
    if save:
        np.savetxt(file_name + ".txt", np.array(data))


def play_txt(file_name):
    data = np.loadtxt(file_name)
    
    for x in data:
        time.sleep(x[1])
        play_note(int(round(x[0])))

if __name__ == "__main__":
    
    # Warmup For the play_sound library to load
    notes = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
    for x in notes:
        play_note(x)
        time.sleep(0.1)
    
    time.sleep(2)
    
    #play_txt("Fr_Elise.mid.txt")
    play_midi("Fr_Elise.mid")
    #play_midi("Merry_Go_Round_of_Life_Howls_Moving_Castle_Piano_Tutorial_.mid")
    #play_txt("Merry_Go_Round_of_Life_Howls_Moving_Castle_Piano_Tutorial_.mid.txt")