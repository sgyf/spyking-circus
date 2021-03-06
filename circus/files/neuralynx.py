import h5py, numpy, re, sys, os, datetime, warnings
from datafile import DataFile

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split('(\d+)', text) ]

class NeuraLynxFile(DataFile):

    description    = "neuralynx"    
    extension      = [".ncs"]
    parallel_write = True
    is_writable    = True

    # constants
    NUM_HEADER_BYTES   = 16 * 1024  # 16 kilobytes of header
    SAMPLES_PER_RECORD = 512
    RECORD_SIZE        = 8 + 4 + 4 + 4 + SAMPLES_PER_RECORD*2 # size of each continuous record in bytes
    OFFSET_PER_BLOCK   = ((8 + 4 + 4 + 4)/2, 0)

    _params            = {'data_dtype'   : 'int16',
                          'dtype_offset' : 0,
                          'data_offset'  : NUM_HEADER_BYTES}


    def parse_neuralynx_time_string(self, time_string):
        # Parse a datetime object from the idiosyncratic time string in Neuralynx file headers
        try:
            tmp_date = [int(x) for x in time_string.split()[4].split('/')]
            tmp_time = [int(x) for x in time_string.split()[-1].replace('.', ':').split(':')]
            tmp_microsecond = tmp_time[3] * 1000
        except:
            warnings.warn('Unable to parse time string from Neuralynx header: ' + time_string)
            return None
        else:
            return datetime.datetime(tmp_date[2], tmp_date[0], tmp_date[1],  # Year, month, day
                                     tmp_time[0], tmp_time[1], tmp_time[2],  # Hour, minute, second
                                     tmp_microsecond)


    def _get_sorted_channels_(self):
        
        directory = os.path.dirname(self.file_name)
        all_files = os.listdir(directory)
        alist     = []
        for f in all_files:
            if f.find('.ncs') > 0:
                alist += [os.path.join(directory, f)]
        alist.sort(key=natural_keys)
        
        return alist

    def _read_header_(self, file):
        header = { }

        f = open(file, 'rb')
        raw_hdr = f.read(self.NUM_HEADER_BYTES).strip(b'\0')
        f.close()

        raw_hdr = raw_hdr.decode('iso-8859-1')

        # Neuralynx headers seem to start with a line identifying the file, so
        # let's check for it
        hdr_lines = [line.strip() for line in raw_hdr.split('\r\n') if line != '']
        if hdr_lines[0] != '######## Neuralynx Data File Header':
            warnings.warn('Unexpected start to header: ' + hdr_lines[0])

        # Try to read the original file path
        try:
            assert hdr_lines[1].split()[1:3] == ['File', 'Name']
            header[u'FileName']  = ' '.join(hdr_lines[1].split()[3:])
            # hdr['save_path'] = hdr['FileName']
        except:
            warnings.warn('Unable to parse original file path from Neuralynx header: ' + hdr_lines[1])

        # Process lines with file opening and closing times
        header[u'TimeOpened'] = hdr_lines[2][3:]
        header[u'TimeOpened_dt'] = self.parse_neuralynx_time_string(hdr_lines[2])
        header[u'TimeClosed'] = hdr_lines[3][3:]
        header[u'TimeClosed_dt'] = self.parse_neuralynx_time_string(hdr_lines[3])

        # Read the parameters, assuming "-PARAM_NAME PARAM_VALUE" format
        for line in hdr_lines[4:]:
            try:
                name, value = line[1:].split()  # Ignore the dash and split PARAM_NAME and PARAM_VALUE
                header[name] = value
            except:
                warnings.warn('Unable to parse parameter line from Neuralynx header: ' + line)

        return header


    def _read_from_header(self):

        folder_path       = os.path.dirname(os.path.abspath(self.file_name))
        self.all_files    = self._get_sorted_channels_()

        regexpr           = re.compile('\d+')
        self.all_channels = []
        for f in self.all_files:
            self.all_channels += [int(regexpr.findall(f)[0])]

        self.header             = self._read_header_(self.all_files[0])
        
        header                  = {}
        header['sampling_rate'] = float(self.header['SamplingFrequency'])        
        header['nb_channels']   = len(self.all_files)
        header['gain']          = float(self.header['ADBitVolts'])*1000000        

        self.inverse     = self.header.has_key('InputInverted') and (self.header['InputInverted'] == 'True')
        if self.inverse:
            header['gain'] *= -1

        g                = open(self.all_files[0], 'rb')
        self.size        = ((os.fstat(g.fileno()).st_size - self.NUM_HEADER_BYTES)//self.RECORD_SIZE - 1) * self.SAMPLES_PER_RECORD
        self._shape      = (self.size, header['nb_channels'])
        g.close()
        
        return header


    def _get_slice_(self, t_start, t_stop):

        x_beg = numpy.int64(t_start // self.SAMPLES_PER_RECORD)
        r_beg = numpy.mod(t_start, self.SAMPLES_PER_RECORD)
        x_end = numpy.int64(t_stop // self.SAMPLES_PER_RECORD)
        r_end = numpy.mod(t_stop, self.SAMPLES_PER_RECORD)

        data_slice  = []

        if x_beg == x_end:
            g_offset = x_beg * self.SAMPLES_PER_RECORD + self.OFFSET_PER_BLOCK[0]*(x_beg + 1) + self.OFFSET_PER_BLOCK[1]*x_beg
            data_slice = numpy.arange(g_offset + r_beg, g_offset + r_end, dtype=numpy.int64)
        else:
            for count, nb_blocks in enumerate(numpy.arange(x_beg, x_end + 1, dtype=numpy.int64)):
                g_offset = nb_blocks * self.SAMPLES_PER_RECORD + self.OFFSET_PER_BLOCK[0]*(nb_blocks + 1) + self.OFFSET_PER_BLOCK[1]*nb_blocks
                if count == 0:
                    data_slice += numpy.arange(g_offset + r_beg, g_offset + self.SAMPLES_PER_RECORD, dtype=numpy.int64).tolist()
                elif (count == (x_end - x_beg)):
                    data_slice += numpy.arange(g_offset, g_offset + r_end, dtype=numpy.int64).tolist()
                else:
                    data_slice += numpy.arange(g_offset, g_offset + self.SAMPLES_PER_RECORD, dtype=numpy.int64).tolist()
        return data_slice


    def read_chunk(self, idx, chunk_size, padding=(0, 0), nodes=None):
        
        t_start, t_stop = self._get_t_start_t_stop(idx, chunk_size, padding)
        local_shape     = t_stop - t_start

        if nodes is None:
            nodes = numpy.arange(self.nb_channels)

        local_chunk = numpy.zeros((local_shape, len(nodes)), dtype=self.data_dtype)
        data_slice  = self._get_slice_(t_start, t_stop) 

        self._open()
        for count, i in enumerate(nodes):
            local_chunk[:, count] = self.data[i][data_slice]
        self._close()

        return self._scale_data_to_float32(local_chunk)

    def write_chunk(self, time, data):

        t_start     = time
        t_stop      = time + data.shape[0]

        if t_stop > self.duration:
            t_stop  = self.duration

        data_slice  = self._get_slice_(t_start, t_stop) 
        data        = self._unscale_data_from_float32(data)
        
        self._open(mode='r+')
        for i in xrange(self.nb_channels):
            self.data[i][data_slice] = data[:, i]
        self._close()

    def _open(self, mode='r'):
        self.data = [numpy.memmap(self.all_files[i], offset=self.data_offset, dtype=self.data_dtype, mode=mode) for i in xrange(self.nb_channels)]
        
    def _close(self):
        self.data = None
