from DrissionPage import ChromiumPage, ChromiumOptions
import time
from boat import Boat

DEBUG_MODE = True
DESTINATION = "Oosterschelde"
BOAT_TYPE = "Sailing Yacht"
BRANDS = ["Dufour", "Beneteau", "Jeanneau"]


def sleep_func(value, debug_mode=DEBUG_MODE):
    if debug_mode:
        for i in range(value):
            time.sleep(1)
            print(i)
    else:
        time.sleep(value)


def main():
    # create a new instance of Chrome
    options = ChromiumOptions()
    options._headless = False
    options.set_argument("--window-size", "1500,800")
    driver = ChromiumPage(options)
    driver.clear_cache()
    driver.refresh()
    driver.get("https://www.tubber.com/us")

    # Wait for 5 seconds for the page to load
    sleep_func(5, DEBUG_MODE)
    # Finding the main div where the Cloudflare IFrame is located...
    sr_parent_div = driver.ele(".cf-turnstile-wrapper")
    # Finding the Shadow-root element under which the iframe object is located...
    sr_child_div = sr_parent_div.sr("tag:iframe")

    # 10 seconds wait to avoid cloudflare security...
    sleep_func(10, DEBUG_MODE)
    sr_child_div.ele("tag:input").click()
    print("=====================Reaching Homepage====================")
    # Waiting for homepage to load...
    sleep_func(10, DEBUG_MODE)
    if driver.ele("#CybotCookiebotDialog"):
        if (
            driver.ele("#CybotCookiebotDialog")
            .child("tag:div")
            .child("#CybotCookiebotDialogFooter")
            .ele("#CybotCookiebotDialogBodyButtonAccept")
        ):
            print("element found...")
            driver.ele("#CybotCookiebotDialog").child("tag:div").child(
                "#CybotCookiebotDialogFooter"
            ).ele("#CybotCookiebotDialogBodyButtonAccept").click()
    search_box = (
        driver.ele(".section__footer")
        .child("tag:div")
        .child("tag:form")
        .child("tag:div")
    )
    search_box.child("tag:div").child("tag:span").ele("tag:input").input(DESTINATION)
    try:
        sleep_func(5, DEBUG_MODE)
        # Handling if signup modal opens up...
        if driver.ele(".modal__container"):
            driver.ele(".modal__container").ele("tag:button").click()
        sleep_func(3, DEBUG_MODE)
        dropdown_box = (
            search_box.child("tag:div")
            .child("tag:span", index=3)
            .ele(".v-select__options")
        )
        dropdown_box.click()
        for child in dropdown_box.ele("tag:ul").children():
            if child.ele("@text():" + BOAT_TYPE):
                print("element found...")
                child.click()
                break
        search_box.child(".form__footer").ele("tag:button").click()
    except:
        if driver.ele(".modal__container"):
            driver.ele(".modal__container").ele("tag:button").click()
        sleep_func(3, DEBUG_MODE)
        dropdown_box = (
            search_box.child("tag:div")
            .child("tag:span", index=3)
            .ele(".v-select__options")
        )
        dropdown_box.click()
        for child in dropdown_box.ele("tag:ul").children():
            if child.ele("@text():" + BOAT_TYPE):
                print("element found...")
                child.click()
                break
        search_box.child(".form__footer").ele("tag:button").click()
    print("=====================Reached Second Page============================")
    # Waiting for page to fully load...
    sleep_func(8, DEBUG_MODE)
    # Adding the brand filter...
    filter_section = (
        driver.ele(".page__container")
        .child("tag:div", index=2)
        .child(".page__content page-content")
        .ele("tag:ul")
    )
    # Finding brand name in filters and ticking it...
    for item in filter_section.children():
        if item.ele(".filters-filter__title").text == "Brand":
            for label in item.eles("tag:label"):
                if label.child("tag:span").text in BRANDS:
                    label.child("tag:input").click()
    # Waiting for filters to apply...
    sleep_func(5, DEBUG_MODE)
    # Clicking on the first boat...
    boat_divs = (
        driver.ele(".page__container")
        .child('tag:div',index=2)
        .child("tag:div", index=3)
        .child("tag:div")
        .child("tag:div", index=3)
        .ele(".results__body")
        .children("tag:div")
    )
    print(boat_divs)
    for div in boat_divs:      
        details_div = div.child("tag:a").child(".boat-body")  
        boat_name = details_div.child("tag:div", index=1).ele("tag:span").text
        boat_length = (
            details_div.child("tag:div", index=2)
            .ele("tag:ul")
            .ele(".boat-spec-item boat-spec-item--full")
            .ele("tag:span")
            .text
        )
        boat_year = details_div.child('tag:div', index=2).ele('tag:ul').ele('tag:li', index=3).ele('tag:div').text.split(' ')[1]
        boat_obj = Boat(boat_name.split(' ')[0], boat_name, boat_year, boat_length)
        print(boat_obj)

    # Print the HTML source code
    print("ran successfully.")
    # driver.quit()


if __name__ == "__main__":
    main()
