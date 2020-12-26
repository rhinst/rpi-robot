# Robot server

## Requirements
   The following programs must be installed and in the PATH of the user executing the server application:
   
  * [SWIG](http://www.swig.org) - Required to install the pocketsphinx speech recognition engine
  * [mpg123](https://www.mpg123.de) - Required for the google text-to-speech (gTTS) engine
  
## Note about PyAudio
  * As of December 2020 there are no official pre-built wheels for pyaudio on python 3.8+.  You will need 
    to build from source or download a pre-built wheel from elsewhere (such as [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)).
  
