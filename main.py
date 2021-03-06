import time

from flask import Flask, request, jsonify

from src.my_functions import get_latency_value, check_anomaly, compute_prime
from src.window_type_updater import WindowTypeUpdater

ANOMALY_SPLIT = 0.3
LATENCY_MEAN = 10000
LATENCY_STD = 50
WINDOW_TIME_SECONDS = 20

app = Flask(__name__)
updater = WindowTypeUpdater(WINDOW_TIME_SECONDS)
updater.start()


@app.route('/')
def info():
    return "Sample app to imitate latency..."


@app.route('/echo', methods=['POST'])
def normal_echo():
    content = request.get_json()
    print(content)
    return jsonify(content)


@app.route('/echo-with-anomaly', methods=['POST'])
def anomaly_echo():
    content = request.get_json()
    print(content)
    delay = get_latency_value(LATENCY_MEAN, LATENCY_STD)
    time.sleep(delay / 1000)
    return jsonify(content)


@app.route('/echo-with-rand-anomaly', methods=['POST'])
def rand_anomaly_echo():
    content = request.get_json()
    print(content)
    if check_anomaly(ANOMALY_SPLIT):
        delay = get_latency_value(LATENCY_MEAN, LATENCY_STD)
        time.sleep(delay / 1000)
        content['anomaly_flag'] = True
    else:
        content['anomaly_flag'] = False
    return jsonify(content)


@app.route('/echo-with-periodic-rand-anomaly', methods=['POST'])
def periodic_rand_anomaly_echo():
    content = request.get_json()
    w, p = updater.get_w_p()
    print(w, " : ", p)
    if w == 0:
        content['anomaly_flag'] = False
    elif w == 1:
        delay = get_latency_value(LATENCY_MEAN, LATENCY_STD)
        time.sleep(delay / 1000)
        content['anomaly_flag'] = True
    else:
        if check_anomaly(p):
            delay = get_latency_value(LATENCY_MEAN, LATENCY_STD)
            time.sleep(delay / 1000)
            content['anomaly_flag'] = True
        else:
            content['anomaly_flag'] = False
    return jsonify(content)


@app.route('/echo-with-process', methods=['POST'])
def echo_with_process():
    content = request.get_json()
    v = compute_prime(500000)
    return jsonify(content)


@app.route('/set-anomaly-split', methods=['POST'])
def set_anomaly_split():
    global ANOMALY_SPLIT
    content = request.get_json()
    print(content)
    try:
        val = float(content['value'])
    except KeyError:
        return jsonify(resp='invalid keys'), 400
    except TypeError:
        return jsonify(resp='invalid value'), 400
    else:
        ANOMALY_SPLIT = val
        return jsonify(resp='success')


@app.route('/set-latency-distribution', methods=['POST'])
def set_latency_distribution():
    global LATENCY_MEAN, LATENCY_STD
    content = request.get_json()
    print(content)
    try:
        mean = float(content['mean'])
        std = float(content['std'])
    except KeyError:
        return jsonify(resp='invalid keys'), 400
    except TypeError:
        return jsonify(resp='invalid value'), 400
    else:
        LATENCY_MEAN, LATENCY_STD = mean, std
        return jsonify(resp='success')


@app.route('/set-window-time', methods=['POST'])
def set_window_time():
    global WINDOW_TIME_SECONDS
    content = request.get_json()
    print(content)
    try:
        val = float(content['value'])
    except KeyError:
        return jsonify(resp='invalid keys'), 400
    except TypeError:
        return jsonify(resp='invalid value'), 400
    else:
        WINDOW_TIME_SECONDS = val
        updater.window_time_second = WINDOW_TIME_SECONDS
        return jsonify(resp='success')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, threaded=True)
