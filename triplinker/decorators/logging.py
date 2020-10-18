# Python modules.
import os
from datetime import datetime, date


# Logs the requests to views: creates dir: 'logs' -> triplinker/triplinker/logs.
# Creates new file(txt) with logs every day.
# There 2 log levels: INFO and DEBUG.
def log_decorator(log_level: str):
    def dec(func):
        def wrapper(request, *args, **kwargs):
            cur_path_raw = os.path.dirname(__file__).rstrip('decorators')
            cur_path = cur_path_raw + 'logs'
            is_dir = os.path.isdir(cur_path)
            if not is_dir:
                os.mkdir(cur_path)

            # datetime object containing current date and time
            now = datetime.now()
            date_ = str(date.today())

            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            view = func.__name__
            data_dict = {}
            if log_level == 'INFO':
                data_dict['New log'] = f'[{view}] {dt_string}'
                data_dict['Path'] = f'{request.path}\n'
                data_dict['Method'] = f'{request.method}\n'
                data_dict['User'] = f'{request.user}\n'

                with open(cur_path + '/' + 'log_' + date_ + '.txt', 'a') as f:
                    f.write('\n')
                    str_ = ('*' * 10) + data_dict['New log'] + ('*' * 10)
                    f.write(str_ + '\n')
                    f.write('Type of log: INFO\n')
                    f.write('Path: ' + data_dict['Path'])
                    f.write('Method: ' + data_dict['Method'])
                    f.write('User: ' + data_dict['User'])
                    len_ = len(data_dict['New log'])
                    str_ = ('*' * 10) + ('*' * len_) + ('*' * 10)
                    f.write(str_ + '\n')
                return func(request, *args, **kwargs)

            elif log_level == 'DEBUG':
                data_dict['New log'] = f'[{view}] {dt_string}'
                data_dict['Shcheme'] = f'{request.scheme}\n'
                data_dict['Path'] = f'{request.path}\n'
                data_dict['Method'] = f'{request.method}\n'
                data_dict['User'] = f'{request.user}\n'
                cookie_dict = request.COOKIES
                del cookie_dict['csrftoken']
                data_dict['Cookies'] = f'{cookie_dict}\n'
                data_dict['User-agent'] = f"{request.headers['User-Agent']}\n"

                with open(cur_path + '/' + 'log_' + date_ + '.txt', 'a') as f:
                    f.write('\n')
                    str_ = ('*' * 10) + data_dict['New log'] + ('*' * 10)
                    f.write(str_ + '\n')
                    f.write('Type of log: DEBUG\n')
                    f.write('Shcheme: ' + data_dict['Shcheme'])
                    f.write('Path: ' + data_dict['Path'])
                    f.write('Method: ' + data_dict['Method'])
                    f.write('User: ' + data_dict['User'])
                    f.write('Cookies: ' + data_dict['Cookies'])
                    f.write('User-agent: ' + data_dict['User-agent'])
                    len_ = len(data_dict['New log'])
                    str_ = ('*' * 10) + ('*' * len_) + ('*' * 10)
                    f.write(str_ + '\n')
                return func(request, *args, **kwargs)
        return wrapper
    return dec
