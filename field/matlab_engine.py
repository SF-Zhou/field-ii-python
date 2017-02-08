import matlab.engine


class MatlabEngine:
    def __init__(self, session_name: str=None):
        if session_name:
            self.engine = matlab.engine.connect_matlab(session_name)
        else:
            self.engine = matlab.engine.start_matlab()
