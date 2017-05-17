import st
from .. import SignalSender


def process(target, args=(), finished=None):
    if finished is not None:
        finished_signal = SignalSender()
        finished_signal.connect(finished)
        st.process(target, args=args, finished=finished_signal.emit)
    else:
        st.process(target, args=args)
