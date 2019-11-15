from shift import Shifter
import requests
from regex import convert

shift = Shifter()
shift.radiate()


def main(text="ho ho ho "):
    text = convert(text)
    shift.spell(text)
    shift.radiate()
    try:
        r = requests.get('https://sweater.jonathan-ray.com/msg')
        parsed = r.json()
        text = parsed["msg"]
    except:
        print("whoops")
    main(text)


main()

exit()
