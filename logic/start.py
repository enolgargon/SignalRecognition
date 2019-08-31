from logic import SignalExecutor
from proyect_util import LoggerControl

if __name__ == '__main__':
    nets = ['1', '2b', '2bis']
    LoggerControl().get_logger('logic_signal').info('Launching Signal identification service with nets ' +
                                                    ', '.join(nets))
    SignalExecutor(nets).create_threads()()
