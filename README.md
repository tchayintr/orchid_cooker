# Thai ORCHID Corpus Cooker
#### _orchid_cooker_

A tool for extracting segmented words from Thai POS-tagged ORCHID corpus.

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

  #### Example outputs
  ```
  Start time: 20200708_2307
  
  ### arguments
  # quiet=False
  # input_data=data/orchid97.crp.gz
  # output_data=cooked/
  # input_data_format=bin
  # output_data_format=sl
  # sentence_len_threshold=1
  
  save cooked data: ./cooked_orchid_20200708_2307.sl
  ### report
  # [PRE] line: 391285 ...
  # [PRE] sent: 23176 ...
  # [POST] sent: 23125 ...
  # [POST] word: 297851 ...
  # [POST] char: 1422081 ...
  # [POST] words/sent: min=1 max=90 avg=12.880043243243243
  # [POST] chars/sent: min=50 max=468 avg=61.49539459459459
  # [POST] chars/word: min=1 max=64 avg=4.77447112818154
  ```
