from DrissionPage import ChromiumPage, ChromiumOptions
import time

DEBUG_MODE = True

def sleep_func(value,debug_mode = DEBUG_MODE):
    if debug_mode:
        for i in range(value):
            time.sleep(1)
            print(i)
    else:
        time.sleep(value)

# create a new instance of Chrome
options = ChromiumOptions()
options._headless = False

driver = ChromiumPage(options)
driver.clear_cache()
driver.refresh()
driver.get("https://www.tubber.com/us")

# Wait for 5 seconds for the page to load
sleep_func(5, DEBUG_MODE)
# Finding the main div where the Cloudflare IFrame is located...
sr_parent_div = driver.ele(".cf-turnstile-wrapper")
# Finding the Shadow-root element under which the iframe object is located...
sr_child_div = sr_parent_div.sr('tag:iframe')

# 10 seconds wait to avoid cloudflare security...
sleep_func(10, DEBUG_MODE)
sr_child_div.ele("tag:input").click()

# Waiting for homepage to load...
sleep_func(15, DEBUG_MODE)
search_box = driver.ele(".section__footer").child("tag:div").child("tag:form").child("tag:div")
search_box.child("tag:div").child(
    "tag:span"
).ele("tag:input").input("Oosterschelde")
# Handling if signup modal opens up...
if driver.ele('.modal__container'):
    driver.ele('.modal__container').ele('tag:button').click()
sleep_func(3,DEBUG_MODE)
dropdown_box = search_box.child('tag:div').child("tag:span", index=3).ele(".v-select__options")
dropdown_box.click()
for child in dropdown_box.ele('tag:ul').children():
    if child.ele('@text():Sailing Yacht'):
        print('element found...')
        child.click()
        break
search_box.child(".form__footer").ele("tag:button").click()
sleep_func(10,DEBUG_MODE)
# Print the HTML source code
print("ran successfully.")
# driver.quit()
