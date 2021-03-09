youtube-dl (https://github.com/rg3/youtube-dl/blob/master/README.md)
$ sudo apt-get install ffmpeg # converts WAV to MP3 files

$ pip install youtube_dl # converts youtube to MP3 files
$ pip install pydub # python library for converting MP3 to WAV and v.v.
$ pip install scipy # for manipulating WAV files
$ pip install matplotlib # for visualising wavforms
$ pip install librosa # audio analysis library



One can use Sonic Visualiser to play and visualize waveforms. It can also be used to annotate the music.
https://www.sonicvisualiser.org/

Workflow:
1. Open an audio file
2. Add a new Time Instance Layer
3. While playing the song, tap on the keyboard ";". A tap can represent a motion primitive, LED pattern, etc. By default annotations will be Cyclical Two-Level Counter (measure/beat). This can be changed under Edit > Number New Instants With
4. Annotations can be exported (CTRL + Y) to a CSV file, which can then be read in by a Python script to generate the dance protocol.

