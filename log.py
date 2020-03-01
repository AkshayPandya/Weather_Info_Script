import logging
from functools import wraps

# Example 1:
#   log=Logger(logfile="file.log")
#   log.C(line="PROBLEM IN METHOD")

# Example 2:
#   Log = Logger(logfile="LogFiles\\logReport.log")
#   Log.Sep_Logger_path = "LogFiles\\SepLogFiles\\"
#
# @Log.Sep_Logger
# def display_info(name, age):
#    pass
#
# display_info("str", int)

class Logger:
    
    def __init__(self, logger_name="__name__", logfile="logReport.log", list_=[4, 4, 4]):
    
        self.LOG = logging.getLogger(logger_name)
        self.filehandler = logging.FileHandler(logfile)
        
        formatterF = "%(asctime)s:%(module)s:%(name)s:%(levelname)s:%(message)s"
        
        self.filehandler.setFormatter(logging.Formatter(formatterF))
        
        self.streamhandler = logging.StreamHandler()
        
        formatterS = "%(name)s:%(levelname)s:%(message)s"
        
        self.streamhandler.setFormatter(logging.Formatter(formatterS))
        
        if list_[0] == 0:
            self.LOG.setLevel(logging.CRITICAL)
        elif list_[0] == 1:
            self.LOG.setLevel(logging.ERROR)
        elif list_[0] == 2:
            self.LOG.setLevel(logging.WARNING)
        elif list_[0] == 3:
            self.LOG.setLevel(logging.INFO)
        elif list_[0] == 4:
            self.LOG.setLevel(logging.DEBUG)
        else:
            pass
            
        if list_[1] == 0:
            self.filehandler.setLevel(logging.CRITICAL)
        elif list_[1] == 1:
            self.filehandler.setLevel(logging.ERROR)
        elif list_[1] == 2:
            self.filehandler.setLevel(logging.WARNING)
        elif list_[1] == 3:
            self.filehandler.setLevel(logging.INFO)
        elif list_[1] == 4:
            self.filehandler.setLevel(logging.DEBUG)
        else:
            pass

        if list_[2] == 0:
            self.streamhandler.setLevel(logging.CRITICAL)
        elif list_[2] == 1:
            self.streamhandler.setLevel(logging.ERROR)
        elif list_[2] == 2:
            self.streamhandler.setLevel(logging.WARNING)
        elif list_[2] == 3:
            self.streamhandler.setLevel(logging.INFO)
        elif list_[2] == 4:
            self.streamhandler.setLevel(logging.DEBUG)
        else:
            pass

    @property
    def File_Formatter(self):
        pass

    @property
    def Stream_Formatter(self):
        pass

    @File_Formatter.setter
    def File_Formatter(self, frmtF):
        self.filehandler.setFormatter(logging.Formatter(frmtF))

    @Stream_Formatter.setter
    def Stream_Formatter(self,frmtS):
        self.streamhandler.setFormatter(logging.Formatter(frmtS))
    
    def C(self, line="CRITICAL"):
        return self.LOG.critical("[{}]".format(line))
    
    def E(self, line="ERROR"):
        return self.LOG.error("[{}]".format(line))

    def W(self, line="WARNING"):
        return self.LOG.warning("[{}]".format(line))
    
    def I(self, line="INFO"):
        return self.LOG.info("[{}]".format(line))

    def D(self, line="DEBUG"):
        return self.LOG.debug("[{}]".format(line))

    def Sep_Logger(self, original_function):

        self.path = ""
        self.LOGD = logging.getLogger(original_function.__name__)
        
        self.filehandlerD = logging.FileHandler("{}{}.log".format(self.path, original_function.__name__))
        self.filehandlerD.setFormatter(logging.Formatter("%(asctime)s:%(module)s:%(name)s:%(levelname)s:%(message)s"))
        self.filehandlerD.setLevel(logging.CRITICAL)

        self.LOGD.setLevel(logging.CRITICAL)

        self.LOGD.addHandler(self.filehandlerD)

        @wraps(original_function)
        def wrapper(*args, **kwargs):
            self.LOGD.critical("function used with ARGS: {}, KWARGS: {}".format(args, kwargs))
            original_function(*args, **kwargs)
        return wrapper
    
    @property
    def Sep_Logger_path(self):
        pass

    @Sep_Logger_path.setter
    def Sep_Logger_path(self, root=""):
        self.path = root

    @property
    def Set_File(self):
        pass

    @property
    def Set_Stream(self):
        pass

    @Set_File.setter
    def Set_File(self, permission):
        if permission == True:
            self.LOG.addHandler(self.filehandler)
        else:
            pass

    @Set_Stream.setter
    def Set_Stream(self, permission):
        if permission == True:
            self.LOG.addHandler(self.streamhandler)
        else:
            pass