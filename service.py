import socket

import win32serviceutil

import servicemanager
import win32event
import win32service


class SMWinservice(win32serviceutil.ServiceFramework):
    #Base class to create a windows service

    """
    Variables that are displayed by the mmc console
    """
    _svc_name_ = "tweepy"
    _svc_display_name = "Twiiter Account Manager Service"
    _svc_description_ = "Twitter Account Manager"

    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):# Called when the service is requested to stop
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)


    def SvcDoRun(self):# Called when the service is requested to start
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
        servicemanager.PYS_SERVICE_STARTED,(self._svc_name_,''))
        self.main()

    def start(self):# Executes before the service starts
        pass

    def stop(self):# Executes before the service stops
        pass

    def main(self):# Main logic of the service 
        pass

if __name__ = "__main__":
    SMWinservice.parse_command_line()
