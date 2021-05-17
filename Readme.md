### SPEAC-analysis python libray
* [David Cope's](http://artsites.ucsc.edu/faculty/cope/) SPEAC-analysis rewritten from Common Lisp to Python
* David Cope's book: [Computer Models of Musical Creativity](https://books.google.de/books?id=rnEJAQAAMAAJ). Cambridge, MA: MIT Press. 2006.
* Original code source: https://github.com/HeinrichApfelmus/david-cope-cmmc 
* Each function has been rewritten using unittests
* Currently, the code coverage is 78%
--------------------------------------

### INSTALLATION
To install the spec, run `pip install speac` 

--------------------------------------

### QUICK START
SPEAC analysis is a hierarchical analysis in which music is considered as a series of nested contexts that range from local to medium, then large and global, and this is where we get this result. The main function of the SPEAC-analysis is `get_the_levels`.   
The result of this function is a list of SPEAC analyzes of different levels, first element of the list is the global analysis (ursatz in Schenker's terms), second element of the list is the large analysis (background), third - is the middle analysis (middleground), last - is foreground.

The function accepts a list of events as input, where each event includes the time the note was pressed in milliseconds, the midi number of the note, the duration (1000 - quarter, 500 - the eighth, etc.), the number of the part or instrument, and the velocity of the note:
<img src="https://github.com/GolzitskyNikolay/SPEAC_analysis/blob/master/img/1.PNG" width="512">

It is also worth noting that these events in the list are sorted by the time they were turned on, and in these events ***all trills and mordents should be deleted***.
The analysis can be started as follows:
 
 ```Python
from speac.chopin_33_3 import CHOPIN_33_3
from speac.top_level import get_the_levels

events = CHOPIN_33_3
meter = 3

get_the_levels(events, meter)
```
 Result:
 
 <img src="https://github.com/GolzitskyNikolay/SPEAC_analysis/blob/master/img/2.PNG" width="700">

Also, to change the default settings, you need to use the class ***`SpeacSettings`***. 
Нou need to give an object of this class as the third argument of this function.

Example:
 ```Python
from speac.chopin_33_3 import CHOPIN_33_3
from speac.speac_settings import SpeacSettings
from speac.top_level import get_the_levels

events = CHOPIN_33_3
meter = 3

my_speac_settings = SpeacSettings()
my_speac_settings.set_pattern_size(8)
my_speac_settings.set_cadence_minimum(12000)

get_the_levels(events, meter, my_speac_settings)
```

--------------------------------------

