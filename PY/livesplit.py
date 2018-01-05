import text
import threading as threads
from queue import Queue, Empty

class LiveSplitClient(object):
    def __init__(self, conn):   
        self.conn = conn
        self.queue = Queue()
        self.thread = threads.Thread(target=self._worker)
        #self.thread.start() # Unused for now. 
    def run_command(self, name, *args, block=True, callback=lambda res:None):
        cmdl = ' '.join([name]+args).replace('\r\n','\n')
        self.send(bytearray(cmdl+'\r\n','UTF-8'))
        
        if block:
            #byts = self.conn.recv(1024)
            #resp = byts.decode('UTF-8')
            
            resp = self._readline()
            
            callback(resp)
            return resp
        else:
            pass#self.queue.put(callback)
        
    def _readline(self):
        import StringIO
        buff = StringIO.StringIO(2048)          # Some decent size, to avoid mid-run expansion
        while True:
            data = self.conn.recv()             # Pull what it can
            buff.write(data.decode('UTF-8'))    # Append that segment to the buffer
            if '\n' in data: break              # If that segment had '\n', break

        # Get the buffer data, split it over newlines, print the first line
        return buff.getvalue().splitlines()[0]
        
    def _worker(self):
        try:
            while True:
                byts = self.conn.recv(1024)
                resp = byts.decode('UTF-8')
                cb = lambda t: print("WARN: Unexpected message from LiveSplit: " + t)
                qg = False
                try:
                    cb = self.queue.get(False)
                    qg = True
                except Empty:
                    pass
                cb(resp)
                if qg:
                    self.queue.task_done()
        except:
            pass
            
    def get_split_time(self):
        return self.run_command('getcomparisonsplittime')
    def get_current_time(self):
        return self.run_command('getcurrenttime')
    def get_delta(self):
        return self.run_command('getdelta')
    def get_split_index(self):
        return self.run_command('getsplitindex')
    def get_best_possible_time(self):
        return self.run_command('getbestpossibletime')
    def get_final_time(self):
        return self.run_command('getfinaltime')
    def get_last_split_time(self):
        return self.run_command('getlastsplittime')
    def get_comparison_time(self):
        return self.run_command('getcomparisonsplittime') # idfk man, thats what the original had
    def get_timer_phase(self):
        return self.run_command('getcurrenttimerphase')
    def get_prev_split_name(self):
        return self.run_command('getprevioussplitname')
    def split(self):
        return self.run_command('split')