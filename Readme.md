### SPEAC-analysis python libray
* [David Cope's](http://artsites.ucsc.edu/faculty/cope/) SPEAC-analysis rewritten from Common Lisp to Python
* David Cope's book: [Computer Models of Musical Creativity](https://books.google.de/books?id=rnEJAQAAMAAJ). Cambridge, MA: MIT Press. 2006.
* Original code source: https://github.com/HeinrichApfelmus/david-cope-cmmc 
* Each function has been rewritten using unittests
* Currently, the code coverage is 78%
--------------------------------------

### INSTALLATION
To install the spec, run `pip install speac` 

### QUICK START
The main function of the analysis is `get_the_levels`. This function performs 4-level analysis based on Schenker's terms. 
Example:
 
 ```Python
from speac.chopin_33_3 import CHOPIN_33_3
from speac.speac_settings import SpeacSettings
from speac.top_level import get_the_levels

my_speac_settings = SpeacSettings()
my_speac_settings.set_pattern_size(8)
my_speac_settings.set_cadence_minimum(12000)
print(get_the_levels(CHOPIN_33_3, 3, my_speac_settings))

```
 
