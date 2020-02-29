from datetime import timedelta, datetime, date

import project_util as util
from models import database, Signal, type_to_code


def create_tables():
    database.connect()
    with database:
        database.create_tables([Signal])
    database.close()


create_tables()

speed_signals_code = [0, 1, 2, 3, 4, 5, 7, 8]
prohibition_signals_code = [9, 10, 15, 16, 17]
warning_signals_code = [11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
other_signals_code = [12, 13, 14, 33, 34, 35, 36, 37, 38, 39, 40]


def register_signal(code):
    invalid_signal(code)
    signal_type = None
    valid = -1

    if code in speed_signals_code:
        invalid_speeds_signal()
        signal_type = 'speed'
    elif code in prohibition_signals_code:
        signal_type = 'prohibition'
    elif code in warning_signals_code:
        signal_type = 'warning'
        valid = 2
    elif code in other_signals_code:
        signal_type = 'other'
        valid = 1
    else:
        print(code)
        signal_type = 'prohibition'
        valid = 0
        switch = {
            6: lambda: invalid_signal(5),  # Fin de límite 80km/h
            32: invalid_prohibition_signals,  # Fin de todas las prohibiciones
            41: lambda: invalid_signal(5),  # Fin de prohibicion adelantar
            42: lambda: invalid_signal(5),  # Fin de prohibicion adelantar (camiones)
        }
        switch.get(code, lambda: util.LoggerControl().get_logger('control_screen')
                   .error(f"Error while register image with code {code}. Code not found"))()

    if not signal_type:
        return
    else:
        signal_type = type_to_code[signal_type]

    try:
        if database.is_closed():
            database.connect()
        with database.atomic():
            print(valid)
            Signal.create(
                code=code,
                name=util.codification[code],
                appearance_time=datetime.now(),
                expiration_time=None if valid == -1 else (datetime.now() + timedelta(minutes=valid)),
                type=signal_type
            )
        if not database.is_closed():
            database.close()
    except Exception as e:
        print(e)
        util.LoggerControl().get_logger('control_screen').error(f'Error during the creation of signal with code {code}')


def invalid_signal(code):
    if database.is_closed():
        database.connect()

    query = Signal.update(expiration_time=datetime.now()).where(Signal.code == code and
                                                                (Signal.expiration_time is None or
                                                                 Signal.appearance_time < datetime.now() < Signal.expiration_time))
    query.execute()
    if not database.is_closed():
        database.close()


def invalid_speeds_signal():
    for code in speed_signals_code:
        invalid_signal(code)


def invalid_prohibition_signals():
    invalid_speeds_signal()
    for code in prohibition_signals_code:
        invalid_signal(code)


def get_current_signals():
    if database.is_closed():
        database.connect()

    signals = Signal.select().where(
        Signal.expiration_time.is_null() | (Signal.appearance_time < datetime.now() < Signal.expiration_time))
    if not database.is_closed():
        database.close()

    return list(signals)


def datetime_wrapper(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()
