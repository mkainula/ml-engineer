import email
import sys
from os import walk

def parse_file(filename, directory, enc):
    f = open(filename, 'r', encoding=enc)
    mail = email.message_from_file(f)
    words = []
    for row in email.iterators.body_line_iterator(mail):
        row_splitted = row.strip().split(' ')
        for words_row in row_splitted:
            if words_row != '':
                words.append(words_row)
    return str("__label__" + directory + ' ' + ' '.join(words))
        
def main(argv):
    output_file = open('output.csv', 'w')
    for (dirpath, dirnames, filenames) in walk('data/sfnet/'):
        for filename in filenames:
            filtered_dirpath = dirpath.split('data/')[1]
            print(str(filtered_dirpath + ":" + filename))
            if filename != '':
                try:
                    output_file.write(parse_file(str(dirpath + "/" + filename), filtered_dirpath, 'utf-8'))
                except UnicodeDecodeError:
                    output_file.write(parse_file(str(dirpath + "/" + filename), filtered_dirpath, 'latin1'))
                output_file.write('\n')
        
if __name__ == "__main__":
    main(sys.argv[1:])
