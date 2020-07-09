############################################
# byte input

INPUT_DATA=data/orchid97.crp.gz
OUTPUT_DATA=cooked/
INPUT_FORMAT=bin
OUTPUT_FORMAT=sl
SENTENCE_LEN_THRESHOLD=1

python3 src/orchid_cooker.py \
    --input_data $INPUT_DATA \
    --output_data $OUTPUT_DATA \
    --input_data_format $INPUT_FORMAT \
    --output_data_format $OUTPUT_FORMAT \
    --sentence_len_threshold $SENTENCE_LEN_THRESHOLD \


############################################
# txt input

INPUT_DATA=data/orchid97.crp.utf.gz
OUTPUT_DATA=cooked/
INPUT_FORMAT=txt
OUTPUT_FORMAT=sl
SENTENCE_LEN_THRESHOLD=1

# python3 src/orchid_cooker.py \
#     --input_data $INPUT_DATA \
#     --output_data $OUTPUT_DATA \
#     --input_data_format $INPUT_FORMAT \
#     --output_data_format $OUTPUT_FORMAT \
#     --sentence_len_threshold $SENTENCE_LEN_THRESHOLD \
