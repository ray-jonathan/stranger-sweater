from shift import Shifter
import requests


shift = Shifter()
# should_prompt = True
# while should_prompt:
#     shift.spell(input('What to say? ').upper())
#     if input("Again? y/n ").upper() != "Y":
#         print("Bye!")
#         should_prompt = False
r = requests.get('http://sweater.jonathan-ray.com/')
parsed = r.json()
shift.spell(parsed["msg"])
exit()
