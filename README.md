# Thai ORCHID Corpus Cooker
#### _orchid_cooker_

tool for extracting words from Thai POS-tagged ORCHID corpus.

#### Data formats
- **sl**: sentence line
- **wl**: word line

#### Usage
```
usage: orchid_cooker.py [-h] [--quiet] --input_data INPUT_DATA
                        [--output_data OUTPUT_DATA]
                        [--input_data_format INPUT_DATA_FORMAT]
                        [--output_data_format OUTPUT_DATA_FORMAT]
                        [--sentence_len_threshold SENTENCE_LEN_THRESHOLD]

optional arguments:
  -h, --help            show this help message and exit
  --quiet, -q           Do not output log file
  --input_data INPUT_DATA, -i INPUT_DATA
                        File path to input data
  --output_data OUTPUT_DATA, -o OUTPUT_DATA
                        File path to output data
  --input_data_format INPUT_DATA_FORMAT, -f INPUT_DATA_FORMAT
                        Choose format of input data among from 'bin' and 'txt'
                        (Default: txt)
  --output_data_format OUTPUT_DATA_FORMAT
                        Choose format of output data among from 'wl' and 'sl'
                        (Default: sl)
  --sentence_len_threshold SENTENCE_LEN_THRESHOLD
                        Sentence length threshold. Sentences whose length are
                        lower than the threshold are ignored (Default: 1)
  ```
