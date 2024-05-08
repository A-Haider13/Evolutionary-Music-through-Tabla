from pydub import AudioSegment
import os

data_folder = 'Algorithm'
tabla_sounds = {
            'dha': AudioSegment.from_file(os.path.join(data_folder, 'dha.wav'), format='wav'),
            'dhin': AudioSegment.from_file(os.path.join(data_folder, 'dhin.wav'), format='wav'),
            'na': AudioSegment.from_file(os.path.join(data_folder, 'na.wav'), format='wav'),
            'ta': AudioSegment.from_file(os.path.join(data_folder, 'ta.wav'), format='wav'),
            'tinak': AudioSegment.from_file(os.path.join(data_folder, 'tinak.wav'), format='wav'),
            'ke': AudioSegment.from_file(os.path.join(data_folder, 'ke.wav'), format='wav'),
            're': AudioSegment.from_file(os.path.join(data_folder, 're.wav'), format='wav'),
            'tun': AudioSegment.from_file(os.path.join(data_folder, 'tun.wav'), format='wav'),
}


def generate_audio_from_chromosome(chromosome):
        print("generating for")
        intervals = [x[1] for x in chromosome]
        max_int = max(intervals)
        min_int = min(intervals)
        print("Range of intervals: ", min_int, max_int)
        # print(chromosome)
        total_time = 0
        for i in range(len(chromosome)):
            total_time += chromosome[i][1]
        bol_time = length * 100
        total_time += bol_time
        audio = AudioSegment.silent(duration=total_time) 
        start_time = 0
        for sound_name, interval, volume_db in chromosome:
            start_time += interval
            sound_clip = tabla_sounds[sound_name]
            # Apply volume adjustment
            sound_clip = sound_clip + volume_db
            # Overlay sound at the specified start time
            audio = audio.overlay(sound_clip, position=int(start_time))
        return audio

chromosome = [(tabla_sounds['dha'], 200, 0), (tabla_sounds['dhin'], 200, 0),(tabla_sounds['dha'], 200, 0), (tabla_sounds['dhin'], 200, 0)]
length = len(chromosome)
generate_audio_from_chromosome(chromosome).export("output.wav", format="wav")