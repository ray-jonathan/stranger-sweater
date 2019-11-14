from shift import Shifter
import requests


def main(text="ho ho ho "):
    shift.spell(text)
    r = requests.get('http://sweater.jonathan-ray.com/')
    parsed = r.json()
    text = parsed["msg"]
    main(text)


main()

exit()
