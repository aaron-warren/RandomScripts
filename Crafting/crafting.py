from pynput.keyboard import Listener, Key
from absl import app, flags
from absl.flags import FLAGS
import time
from multiprocessing import Event, Process
from process import PID

flags.DEFINE_string('keys', None, 'path for keys')
flags.DEFINE_integer('amount', None, 'number of iterations')
flags.DEFINE_string('food', None, "hotkey for food")

class Actions:
    def __init__(self, delay, key):
        self.delay = delay
        self.key = key

def inputs(work_event, kill_event):
    def on_press(key):
        try:
            if key.char == '`':
                if work_event.is_set():
                    work_event.clear()
                else:
                    work_event.set()

        except AttributeError:
            if key == Key.esc:
                kill_event.set()
                print("Exiting key listener")
                quit()
    
    with Listener(on_press=on_press) as listener:
        listener.join()

def craft(work_event, kill_event, keys, amount, food):
    index = 0
    iterations = 0
    t0 = 0
    proc = PID()

    infinite = True
    if amount != 0:
        infinite = False

    while True:
        if work_event.is_set():
            if food is not None and index == 0 and iterations == 0:
                print(f"Using food, then waiting {food.delay} second(s)")
                proc.press_key(food.key)
                time.sleep(food.delay)
                t0 = time.time()

            action = keys[index % len(keys)].key
            delay = keys[index % len(keys)].delay

            print(f"Pressing {action}, then waiting {delay} second(s)")

            proc.press_key(action)
            time.sleep(delay)

            index = index+1
            if index == len(keys):
                index = 0
                time.sleep(3)
                iterations = iterations + 1
                if food is not None and time.time() - t0 > 1750:
                    print(f"Using food, then waiting {food.delay} second(s)")
                    proc.press_key(food.key)
                    time.sleep(food.delay)
                    t0 = time.time()

            if not infinite and iterations >= amount:
                kill_event.set();
        else:
            index = 0
        if kill_event.is_set():
            print("Exiting craft process")
            quit()

def getKeys(fileName):
    keys = []

    keys.append(Actions(2, "{VK_NUMPAD0}"))
    keys.append(Actions(2, "{VK_NUMPAD0}"))

    for line in open(fileName):
        line = line.rstrip()
        line = line.lower()

        if line[0] == '[' and line[len(line) - 1] == ']':
            key = getModifier(line[1:len(line)-1])
            keys.append(Actions(2, key))
        elif len(line) > 0:
            key = getModifier(line)
            keys.append(Actions(3, key))

    return keys

def getModifier(key):
    if "shift" in key:
        key = "+" + key[6:]
    if "ctrl" in key:
        key = "^" + key[5:]
    if "alt" in key:
        key = "%" + key[4:]

    return key
    

def main(argv):
    if FLAGS.keys is None:
        print("No file for keys specified, set with --keys='{path to file}'")
        quit()

    food = None
    if FLAGS.food is None:
        print("Warning: No food hotkey specified, set with --food='{hotkey}'")
    else:
        food = Actions(4, getModifier(FLAGS.food))

    if FLAGS.amount is None:
        print("Warning: No amount to stop set, set with --amount='{number}'")
        amount = 0
    else:
        amount = FLAGS.amount

    keys = getKeys(FLAGS.keys)

    work_event = Event()
    kill_event = Event()

    process1 = Process(target=craft, args=(work_event, kill_event, keys, amount, food))
    process2 = Process(target=inputs, args=(work_event, kill_event))

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    print("Exiting program")
    quit()


if __name__ == "__main__":
    try:
        app.run(main)
    except SystemExit:
        pass
    pass