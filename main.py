from DrissionPage import ChromiumPage, ChromiumOptions
import time
import json
from datetime import datetime
from boat import Boat
from scrapingException import ScrapingException

DEBUG_MODE = True
# DESTINATION = "Oosterschelde"
DESTINATION = "Yerseke"
# BOAT_TYPE = "Sailing Yacht"
BOAT_TYPE = "Motorboat"
# BRANDS = ["Dufour", "Beneteau", "Jeanneau"]
BRANDS = ["Bavaria"]


def sleep_func(value, debug_mode=True):
    if debug_mode:
        for i in range(value):
            time.sleep(1)
            print(i)
    else:
        time.sleep(value)

def setting_filters(driver, retry=True):
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

    print("filter section element: ", filter_section)
    # Finding brand name in filters and ticking it...
    brand_counter = 0
    for item in filter_section.children():
        print("li item: ", item)
        if item.ele(".filters-filter__title").text == "Brand":
            print("found brand filter...")
            for label in item.eles("tag:label"):
                print("label: ", label)
                if label.child("tag:span").text in BRANDS:
                    print("Label found...")
                    label.child("tag:input").click()
                    brand_counter += 1
            if brand_counter >= 1:
                print(
                    "Filter for "
                    + str(brand_counter)
                    + " out of "
                    + str(len(BRANDS))
                    + " are applied"
                )
            else:
                raise ScrapingException(
                    "None of the targeting brands are available"
                )
    # checking if after iterating all of the filter headers if we don't find Brand filter...
    if brand_counter < 1:
        print(brand_counter)
        if retry:
            driver.refresh()
            setting_filters(driver, retry=False)
        else:
            # Even after retry if the brand filter dont show up we will raise an exception...
            print("Brand filter not found..")
            raise ScrapingException("No boat available at this moment")

def main():
    try:
        # create a new instance of Chrome
        options = ChromiumOptions()
        options._headless = False
        options.set_argument("--window-size", "1500,800")
        driver = ChromiumPage(options)
        driver.clear_cache()
        driver.refresh()
        driver.get("https://www.tubber.com/us")

        # Wait for 7 seconds for the page to load
        sleep_func(5, DEBUG_MODE)
        # Finding the main div where the Cloudflare IFrame is located...
        if driver.ele("#PYMIw2"):  # .cf-turnstile-wrapper
            print("found cloudflare firewall..")
            sr_parent_div = driver.ele("#PYMIw2").child().child().child()
            # Finding the Shadow-root element under which the iframe object is located...
            sr_child_div = sr_parent_div.sr("tag:iframe")

            # 10 seconds wait to avoid cloudflare security...
            sleep_func(10, DEBUG_MODE)
            # Update: cloudflare has a #document element under iFrame so we need to identify the input tag in it...
            iframe_sr_parent = sr_child_div.ele("tag:body")
            iframe_sr_child = iframe_sr_parent.sr("tag:input")
            iframe_sr_child.click()
        else:
            print("didnt found cloudflare firewall...")
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
        search_box.child("tag:div").child("tag:span").ele("tag:input").input(
            DESTINATION
        )
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

        # Sometimes brand filter doesnt show up so Setting filters with retry once...
        setting_filters(driver)
        # Waiting for filters to apply...
        sleep_func(5, DEBUG_MODE)
        # Clicking on the first boat...
        boat_divs = (
            driver.ele(".page__container")
            .child("tag:div", index=2)
            .child("tag:div", index=3)
            .child("tag:div")
            .child("tag:div", index=3)
            .ele(".results__body")
            .children("tag:div")
        )
        print(boat_divs)
        boats = []
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
            boat_year = (
                details_div.child("tag:div", index=2)
                .ele("tag:ul")
                .ele("tag:li", index=3)
                .ele("tag:div")
                .text.split(" ")[1]
            )
            boat_obj = Boat(boat_name.split(" ")[0], boat_name, boat_year, boat_length)

            print("==============moving to boat details page===================")
            div.child("tag:a").click()
            print(driver.latest_tab)
            print(driver.tabs_count)
            print(driver.tab_ids)
            details_tab = driver.get_tab(driver.tab_ids[0])
            sleep_func(10, DEBUG_MODE)
            availability_slots = (
                details_tab.ele(".page__container")
                .child("tag:div", index=2)
                .ele(".boat-calendar")
                .ele(".available-prices")
                .ele(".prices-list")
                .children("tag:div")
            )
            next_btn = (
                details_tab.ele(".page__container")
                .child("tag:div", index=2)
                .ele(".boat-calendar")
                .ele(".available-prices")
                .ele("tag:button", index=2)
            )
            btn_trigger = 4
            for index, slot in enumerate(availability_slots):
                start_date = slot.ele("tag:p").text
                end_date = slot.ele("tag:p", index=2).text
                availability = slot.ele("tag:p", index=3).text
                price = None
                if availability.lower() == "available":
                    price = slot.ele("tag:p", index=4).text
                if index == btn_trigger:
                    next_btn.click()
                    btn_trigger += 2
                    sleep_func(3, DEBUG_MODE)
                boat_obj.add_schedule(start_date, end_date, availability, price)
            details_tab.close()
            print(boat_obj)
            boats.append(boat_obj)
        with open(
            "./scraped_jsons/data_" + str(datetime.now().timestamp()) + ".json", "w"
        ) as file:
            json.dump([boat.__dict__() for boat in boats], file)
        print("ran successfully.")
        if not DEBUG_MODE:
            driver.quit()
    except ScrapingException as err:
        print("ScrapingException: ", err)
    except Exception as err:
        print("Exception: ", err)
    finally:
        if not DEBUG_MODE:
            driver.quit()


if __name__ == "__main__":
    main()
