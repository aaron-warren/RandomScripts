import os
import pathlib
from absl import app, flags
from absl.flags import FLAGS

flags.DEFINE_string('name', None, 'name of the series')
flags.DEFINE_integer('season', None, 'season being renamed')

class Rename:
    def __init__(self, before, after, extension):
        self.before = before
        self.after = after

def main(argv):
    if FLAGS.name is None:
        print("No name defined")
        quit()
    if FLAGS.season is None:
        print("No season is defined")
        quit()

    dir = pathlib.Path(__file__).parent.absolute()
    
    file = []
    for filename in os.listdir(dir):
        if(filename != "rename.py"):
            file.append(filename)

    d = "{}/{}".format(dir, file[0])
    t, extension = os.path.splitext(d)

    file.sort()

    e = 1
    objectsToRename = []
    for f in file:
        og = "{}/{}{}".format(dir, f)
        rn = "{}/{} - S{:02d}E{:02d}{}".format(dir, FLAGS.name, FLAGS.season, e, extension)
        e = e+1
        objectsToRename.append(Rename(og, rn))

    for x in objectsToRename:
        print("{} -> {}".format(x.before, x.after))

    conf = input("Confirm (y/n)? ")

    if(conf.lower() == "y"):
        for x in objectsToRename:
            os.rename(x.before, x.after)
            print("Renamed {} -> {}".format(x.before, x.after))
    else:
        print("Exiting...")
        quit()

if __name__ == "__main__":
    try: 
        app.run(main)
    except SystemExit:
        pass