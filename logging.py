def logging(s, status='none'):
    if status == 'WARN':
        full_s = '\33[31m\33[40m' + s + '\33[0m'
        print full_s
        return
    elif status == 'SUCCESS':
        full_s = '\33[32m\33[40m' + s + '\33[0m'
        print full_s
        return
    elif status == 'SPECIAL':
        full_s = '\33[34m\33[40m' + s + '\33[0m'
        print full_s
        return
    else:
        full_s = '\33[33m' + s + '\33[0m'
        print full_s
        return
