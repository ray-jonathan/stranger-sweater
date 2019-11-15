from shift import Shifter
import requests
from regex import convert


def main(text="ho ho ho "):
    text = convert(text)
    shift.spell(text)
    r = requests.get('https://sweater.jonathan-ray.com/')
    parsed = r.json()
    text = parsed["msg"]
    main(text)


main()

exit()
