import argparse
import gzip
from pathlib import Path
import re
import sys
from datetime import datetime



'''
    Script for cooking ORCHID corpus
      - word-level
      - characteristics

'''

# ORCHID delimiters

LINE_DELIM = '\n'                       # Line
EOS_DELIM = '//'                        # End of sentence
OOS_DELIM = '\\\\'                      # Ongoing of sentence
WL_DELIM = '\n'                         # Word line
POS_ATTR_DELIM = '/'                    # POS attribute
PARAGRAPH_DELIM_PATTERN = '#P[0-9]+'    # Paragraph pattern
COMMENT_SYMS = ['%', '#']               # Comment symbols
CHAR_SYMS = {                           # Character symbols
    # '<space>': ' ',
    '<space>': '',
    '<exclamation>': '!',
    '<quotation>': '"',
    '<number>': '#',
    '<dollar>': '$',
    '<percent>': '%',
    '<ampersand>': '&',
    '<apostrophe>': '\'',
    '<left_parenthesis>': '(',
    '<right_parenthesis>': ')',
    '<asterisk>': '*',
    '<plus>': '+',
    '<comma>': ',',
    '<minus>': '-',
    '<full_stop>': '.',
    '<slash>': '/',
    '<colon>': ':',
    '<semi_colon>': ';',
    '<less_than>': '<',
    '<equal>': '=',
    '<greater_than>': '>',
    '<question_mark>': '?',
    '<at_mark>': '@',
    '<left_square_bracket>': '[',
    '<right_square_bracket>': ']',
    '<circumflex_accent>': '^',
    'low_line': '_',
    'left_curly_bracket': '{',
    'right_curly_bracket': '}',
    'tilde': '~'
}

# for data io

SL_TOKEN_DELIM = ' '
SL_ATTR_DELIM = '_'
WL_TOKEN_DELIM = '\n'
WL_ATTR_DELIM = '\t'

SL_FORMAT = 'sl'
WL_FORMAT = 'wl'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quiet', '-q', action='store_true', help='Do not output log file')
    parser.add_argument('--input_data', '-i', type=Path, required=True, help='File path to input data')
    parser.add_argument('--output_data', '-o', type=Path, default=None, help='File path to output data')
    parser.add_argument('--input_data_format', '-f', default='txt', help='Choose format of input data among from \'bin\' and \'txt\' (Default: txt)')
    parser.add_argument('--output_data_format', default='sl', help='Choose format of output data among from \'wl\' and \'sl\' (Default: sl)')
    parser.add_argument('--sentence_len_threshold', type=int, default=1, help='Sentence length threshold. Sentences whose length are lower than the threshold are ignored (Default: 1)')

    args = parser.parse_args()
    return args


def load_data(path, data_format):
    if data_format == 'bin':
        data = load_bin_data(path)

    elif data_format == 'txt':
        data = load_txt_data(path)

    else:
        print('Error: invalid data format: {}'.format(data_format), file=sys.stderr)
        sys.exit()

    return data


def load_bin_data(path):
    data_loader = gzip.open if is_gz_file(path) else open
    data = []
    with data_loader(path, 'rb') as f:
        for line in f:
            line = line.decode('tis620')
            if not any(line.startswith(comment_sym) for comment_sym in COMMENT_SYMS):
                line = line.strip(LINE_DELIM)
                data.append(line)
    return data


def load_txt_data(path):
    data_loader = gzip.open if is_gz_file(path) else open
    data = []
    with data_loader(path, 'rt', encoding='utf8') as f:
        for line in f:
            if not any(line.startswith(comment_sym) for comment_sym in COMMENT_SYMS):
                line = line.strip(LINE_DELIM)
                data.append(line)
    return data


def gen_gold_data(data, data_format, threshold=1):
    if data_format == SL_FORMAT:
        data = gen_gold_data_SL(data, threshold)

    elif data_format == WL_FORMAT:
        data = gen_gold_data_WL(data, threshold)

    return data


def gen_gold_data_SL(data, threshold=1):
    gs = []                 # gold data
    ls = data               # lines
    wss = gen_swords(ls)    # sentential segmented words (2D)
    for ws in wss:
        if len(ws) < threshold:
            continue
        l = SL_TOKEN_DELIM.join(ws)
        for k, v in CHAR_SYMS.items():
            l = re.sub(' +', ' ', l.replace(k, v))
        sl = l
        gs.append(sl)
    return gs


def gen_gold_data_WL(data, threshold=1):
    gs = []                 # gold data
    ls = data               # lines
    wss = gen_swords(ls)    # sentential segmented words (2D)
    for ws in wss:
        if len(ws) < threshold:
            continue
        l = SL_TOKEN_DELIM.join(ws)
        for k, v in CHAR_SYMS.items():
            l = re.sub(' +', ' ', l.replace(k, v))
        wls = l.split()
        wl = WL_TOKEN_DELIM.join(wls) + WL_DELIM    # concat with WL_DELIM for output data
        gs.append(wl)
    return gs


def gen_swords(lines):
    wss = []    # sentential segmented words (2D); [[s1_w1, s1_w2, .., s1_wn], ..., [sm_w1, sm_w2, ..., sm_wk]]
    ws = []     # words
    for line in lines:
        if POS_ATTR_DELIM in line and not (line.endswith(OOS_DELIM) or line.endswith(EOS_DELIM)):
            w = line.partition(POS_ATTR_DELIM)[0]
            ws.append(w)
        elif EOS_DELIM in line and ws:
            wss.append(ws)
            ws = []
    return wss


def gen_sentences(lines):
    ss = []     # sentences
    sfs = []    # sentence fragments
    for line in lines:
        if len(line) > len(EOS_DELIM) and line.endswith(OOS_DELIM):
            sf = line.partition(OOS_DELIM)[0]
            sfs.append(sf)
        elif len(line) > len(EOS_DELIM) and line.endswith(EOS_DELIM):
            sf = line.partition(EOS_DELIM)[0]
            s = ''.join(sfs) + sf if sfs else sf
            ss.append(s)
            sfs = []
    return ss


# def gen_paragraphs(lines):
#     ps = []     # paragraphs
#     ss = []     # sentences
#     sfs = []    # sentence fragments
#     PARAGRAPH_PATTERN_RE = re.compile(PARAGRAPH_DELIM_PATTERN)
#     for line in lines:
#         if (len(line) > len(EOS_DELIM) and line != EOS_DELIM) and line.endswith(OOS_DELIM):
#             sf = line.partition(OOS_DELIM)[0]
#             sfs.append(sf)
#         elif (len(line) > len(EOS_DELIM) and line != EOS_DELIM) and line.endswith(EOS_DELIM):
#             sf = line.partition(EOS_DELIM)[0]
#             s = ''.join(sfs) + sf if sfs else sf
#             ss.append(s)
#             sfs = []
#         elif PARAGRAPH_PATTERN_RE.match(line):
#             if ss:
#                 ps.append(ss)
#                 ss = []
#     return ps


def is_gz_file(path):
    return path.suffix == '.gz'


def log(message, file=sys.stderr):
    print(message, file=file)


def report(data, gold_data):
    lines = data
    sents = gold_data

    n_psents = len(gen_sentences(lines))
    n_sents = len(sents)

    ss = [s.split() for s in sents]
    ws = [w for s in ss for w in s]
    n_words = len(ws)

    cs = [c for w in ws for c in w]
    n_chars = len(cs)

    max_wps = len(max(ss, key=len))
    max_cps = sum([len(c) for w in max(ss, key=len) for c in w])
    max_cpw = len(max(ws, key=len))

    min_wps = len(min(ss, key=len))
    min_cps = sum([len(c) for w in min(ss, key=len) for c in w])
    min_cpw = len(min(ws, key=len))

    avg_wps = n_words / n_sents     # words/sentence
    avg_cps = n_chars / n_sents     # chars/sentence
    avg_cpw = n_chars / n_words     # chars/word

    log('### report')
    log('# [PRE] line: {} ...'.format(len(data)))
    log('# [PRE] sent: {} ...'.format(n_psents))
    log('# [POST] sent: {} ...'.format(n_sents))
    log('# [POST] word: {} ...'.format(n_words))
    log('# [POST] char: {} ...'.format(n_chars))
    log('# [POST] words/sent: min={} max={} avg={}'.format(min_wps, max_wps, avg_wps))
    log('# [POST] chars/sent: min={} max={} avg={}'.format(min_cps, max_cps, avg_cps))
    log('# [POST] chars/word: min={} max={} avg={}'.format(min_cpw, max_cpw, avg_cpw))


def cook(args):
    start_time = datetime.now().strftime('%Y%m%d_%H%M')
    if not args.quiet:
        log('Start time: {}\n'.format(start_time))
        log('### arguments')
        for k, v in args.__dict__.items():
            log('# {}={}'.format(k, v))
        log('')

    data_path = args.input_data
    data = load_data(data_path, data_format=args.input_data_format)
    gold_data = gen_gold_data(
        data,
        data_format=args.output_data_format,
        threshold=args.sentence_len_threshold
    )

    if args.output_data:
        output_data_path = '{}/cooked_orchid_{}.{}'.format(args.output_data, start_time, args.output_data_format)
        with open(output_data_path, 'w', encoding='utf8') as f:
            for gd in gold_data:
                print(gd, file=f)
            if not args.quiet:
                log('save cooked data: {}'.format(output_data_path))

    if not args.quiet:
        report(data, gold_data)


def main():
    args = parse_args()
    cook(args)



if __name__ == '__main__':
    main()
