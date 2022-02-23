import sys
import signal

def killtrap_handler(signum, frame) -> None:
    print("trapped. signum={} frame={}".format(signum, frame))
    sys.exit(1)
        
class UtilSignal():
    def __init__(self) -> None:
        try:
            pass
        except Exception as err:
            print(err)
            raise
    
    def __del__(self) -> None:
        try:
            pass
        except Exception as err:
            print(err)
            raise

    @classmethod
    def pause_kill(cls) -> None:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    @classmethod
    def resume_kill(cls) -> None:
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    @classmethod
    def set_killtrap_handler(cls) -> None:
        signal.signal(signal.SIGTERM, killtrap_handler)
    

