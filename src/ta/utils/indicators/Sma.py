import logging
import logging.config

class Sma:
    def __init__(self, parameter, *args):
        self.parameter = parameter
        self.row = 4 # close
        if args: self.row = args[0]
        self.input = []
        self.output = []
        
        logging.config.fileConfig("logging.conf")
        self.logger = logging.getLogger("Indicator")
        
    def append(self, value):
        # check if valid input
        if not self._validate(value): return
        if type(value) is tuple: value = value[self.row]
        if self._calculate(value): return self.output[-1]
        
    def _validate(self, value):
        if not type(value) is float and not type(value) is int and not type(value) is tuple:
            self.logger.debug('invalid input: %s; should be either float or int or tuple' % value) 
            return False
        else: return True
        
    def _calculate(self, value):
        self.input.append(float(value))
        outputvalue = None
        if len(self.input) >= self.parameter:
            try:    
                outputvalue = sum(self.input[(len(self.input)-self.parameter):len(self.input)]) / self.parameter
            except:
                self.logger.debug('error calculating sma value; reverting input data back to previous state')
                self.input = self.input[:-1]
                return False
        self.output.append(outputvalue)
        return True
    
    # overloads
    def __str__(self):
        string = ''
        for i in xrange(len(self.input)):
            string+='%s\t%s\t%s\n' % (i+1, self.input[i], self.output[i])
        return 'Sma(%s):\n%s' % (self.parameter, string)
    def __repr__(self):
        return 'Sma(%s)' % self.parameter
    def __len__(self):
        return len(self.output)
    def __getitem__(self, offset):
        return self.output[offset]
    def __getslice__(self, low, high):
        return self.output[low:high]

if __name__=='__main__':
    ind = Sma(6)
    #input = [12.23, 12.34, 12.33, 12.35, 12.37, 12.24, 12.21, 12.11, 12.05, 11.85]
    import datetime
    input = [(datetime.datetime(2006, 5, 1), 12.34, 12.56, 12.11, 12.20, 2010912),
             (datetime.datetime(2006, 5, 2), 12.24, 12.48, 12.20, 12.22, 8791029),
             (datetime.datetime(2006, 5, 3), 12.18, 12.20, 11.88, 12.16, 5434255),
             (datetime.datetime(2006, 5, 4), 12.24, 12.68, 12.24, 12.38, 8734251),
             (datetime.datetime(2006, 5, 5), 12.30, 12.88, 12.28, 12.57, 3637262),
             (datetime.datetime(2006, 5, 8), 12.34, 12.56, 12.11, 12.20, 2010912),
             (datetime.datetime(2006, 5, 9), 12.24, 12.48, 12.20, 12.22, 8791029),
             (datetime.datetime(2006, 5, 10), 12.18, 12.20, 11.88, 12.16, 5434255),
             (datetime.datetime(2006, 5, 11), 12.24, 12.68, 12.24, 12.38, 8734251),
             (datetime.datetime(2006, 5, 12), 12.30, 12.88, 12.28, 12.57, 3637262),
             (datetime.datetime(2006, 5, 15), 12.34, 12.56, 12.11, 12.20, 2010912),
             (datetime.datetime(2006, 5, 16), 12.24, 12.48, 12.20, 12.22, 8791029),
             (datetime.datetime(2006, 5, 17), 12.18, 12.20, 11.88, 12.16, 5434255),
             (datetime.datetime(2006, 5, 18), 12.24, 12.68, 12.24, 12.38, 8734251),
             (datetime.datetime(2006, 5, 19), 12.30, 12.88, 12.28, 12.57, 3637262),
          ]
    for i in input:
        ind.append(i)
    print ind