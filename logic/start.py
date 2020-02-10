from logic import SignalExecutor
from project_util import LoggerControl

nets = ['1_1', '2_1', '3_1', '4_1', '5_1']
LoggerControl().get_logger('logic_signal').info('Launching Signal identification service with nets ' +
                                                ', '.join(nets))
SignalExecutor(nets).create_threads()()
