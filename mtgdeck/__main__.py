import sys
import json
import mtgdeck


if __name__ == '__main__':
    json.dump(mtgdeck.load(sys.stdin), sys.stdout)
