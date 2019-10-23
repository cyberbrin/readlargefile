
# Large text file reader.

## install

```pip install readlargefile```

## usage:
```
from readlargefile.line_reader import LineReader

with LineReader(file_name, max_line, sep) as reader:
    # line is <class 'bytes'>
    for line in reader:
        if line:
            print(line)
        elif line == b'':
            print('empty line.')
        else:
            # line == None
            print('line is too long.')
```
