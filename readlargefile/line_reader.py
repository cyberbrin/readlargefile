from queue import Queue


class LineBuffer:
    """
    Line buffer
    """

    def __init__(self, max_size: int):
        self._queue = Queue(max_size)

    def add_byte(self, one_byte: bytes):
        data_size = len(one_byte)
        if data_size != 1:
            raise ValueError('LineBuffer.add_byte: len(one_byte) != 1')
        if self._queue.full():
            self._queue.get()
        self._queue.put(int(one_byte[0]))

    def get_bytes(self) -> bytes:
        return bytes(self._queue.queue)

    def clear(self):
        self._queue.queue.clear()


class LineReader:
    """
    Read large file by line.

    constructor:
        file_name (str): File path.
        max_line (int): Maximum length of the line.
        sep (bytes): Separate byte, default is b'\\n'.
    usage:
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
    """

    def __init__(self, file_name: str, max_line: int, sep: bytes = b'\n'):
        if len(sep) != 1:
            raise ValueError('LineReader.__init__: len(sep) != 1')
        self._file_name = file_name
        self._max_line = max_line
        self._sep = sep
        self._line_buffer = LineBuffer(max_line)
        self._pos = 0
        self._start_line = 0
        self._file = None
        self._is_finished = False

    def open(self):
        if not self._file:
            self._file = open(self._file_name, 'rb')

    def close(self):
        if self._file:
            self._file.close()
            self._line_buffer.clear()
            self._pos = 0
            self._start_line = 0
            self._file = None
            self._is_finished = False

    def reset(self):
        self._line_buffer.clear()
        self._pos = 0
        self._start_line = 0
        self._is_finished = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _read(self, one_byte: bytes) -> bytes:
        self._pos += 1
        line_len = self._pos-self._start_line-1
        result = None
        if one_byte != self._sep:
            if line_len <= self._max_line:
                self._line_buffer.add_byte(one_byte)
        else:
            if line_len <= self._max_line:
                result = self._line_buffer.get_bytes()
                self._line_buffer.clear()
                self._start_line = self._pos
            else:
                self._line_buffer.clear()
                self._start_line = self._pos
                result = None
        return result

    def __next__(self) -> bytes:
        if self._is_finished:
            raise StopIteration
        while True:
            self._file.seek(self._pos)
            one_byte = self._file.read(1)
            if one_byte:
                if one_byte == self._sep:
                    return self._read(one_byte)
                else:
                    self._read(one_byte)
            else:
                self._is_finished = True
                return self._read(self._sep)

    def __iter__(self):
        return self
