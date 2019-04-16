from egissoshechka.app import app
from egissoshechka.app import time
from egissoshechka.app import set_webhook
from egissoshechka.app import threading
from egissoshechka.app import sched
from egissoshechka.app import viber

if __name__ == '__main__':
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    context = ('ssl/viber.crt', 'ssl/viber.key')
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=context)