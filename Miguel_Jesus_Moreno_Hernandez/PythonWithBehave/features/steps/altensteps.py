import os
import csv
from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time

# Variables
URL = "https://www.alten.es/"
BROWSER = "chrome"
HOME = "Home - ALTEN Spain"
BUT_ACCEPT_COOKIES = (By.XPATH, '//button[@id="tarteaucitronPersonalize2"]')
DWN_SECTORES = (By.XPATH, '//ul[@id="menu-header-es-1"]//span[text()="Sectores"]')
RESULTS_FOLDER = 'results'
BUT_HOME = (By.XPATH, '//ul[@id="menu-header-es-1"]//span[text()="Home"]')
SEARCH_ICON = (By.XPATH, '//div[@id="header-toolbar-2"]/div//button/span')
SEARCH_INPUT = (By.XPATH, '//div[@id="header-toolbar-2"]//input')
RESULT_SEARCH = (By.XPATH, '//div[@id="header-toolbar-2"]//span[contains(text(),"resultados")]')

if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)


def open_csv():
    csv_file_path = os.path.join(RESULTS_FOLDER, 'results.csv')
    file_exists = os.path.isfile(csv_file_path)
    csv_file = open(csv_file_path, mode='a', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    if not file_exists:
        csv_writer.writerow(['Sector', 'Result', 'Error Message'])
    return csv_file, csv_writer


def log_result_to_csv(csv_writer, sector, result, error_message=""):
    csv_writer.writerow([sector, result, error_message])


def after_step(context, step):
    if step.status == 'failed':
        # Log the error to the CSV
        csv_file, csv_writer = open_csv()
        log_result_to_csv(csv_writer, context.current_test, 'FAILED', step.exception)
        csv_file.close()

        # Save screenshot
        screenshot_path = os.path.join(RESULTS_FOLDER, f"Error_{context.current_test}_Failed.png")
        context.driver.save_screenshot(screenshot_path)


def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        context.driver.quit()


# Setup function to open the browser and navigate to the Alten page
@given('I have opened the Alten Page')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()
    context.driver.get(URL)
    wait = WebDriverWait(context.driver, 30)
    but_accept_cookies = wait.until(EC.visibility_of_element_located(BUT_ACCEPT_COOKIES))
    wait.until(EC.element_to_be_clickable(BUT_ACCEPT_COOKIES)).click()
    assert context.driver.title == HOME, "Page has not loaded correctly"
    context.driver.save_screenshot(os.path.join(RESULTS_FOLDER, "Main_Page_Loaded.png"))
    print("\n==== Browser Opened and Maximized ====\n")
    time.sleep(2)


# Step function to open the dropdown and select a sector
@when('I open the dropdown Sectores and choose "{sector}"')
def step_impl(context, sector):
    context.current_test = sector
    print(f"\n==== Verify step: Open dropdown Sectores and choose '{sector}' ====\n")
    wait = WebDriverWait(context.driver, 10)

    dropdown_button = wait.until(EC.visibility_of_element_located(DWN_SECTORES))
    wait.until(EC.element_to_be_clickable(DWN_SECTORES))

    # Perform mouse over action
    actions = ActionChains(context.driver)
    actions.move_to_element(dropdown_button).perform()

    sector_option_xpath = f'//ul[@id="menu-header-es-1"]//span[text()="{sector}"]'
    sector_option = wait.until(EC.visibility_of_element_located((By.XPATH, sector_option_xpath)))
    wait.until(EC.element_to_be_clickable((By.XPATH, sector_option_xpath)))
    sector_option.click()


# Step function to verify the page for the selected sector
@then('I should see the page for "{sector}"')
def step_impl(context, sector):
    wait = WebDriverWait(context.driver, 10)
    option_xpath = f'//h1[contains(translate(text(), "ABCDEFGHIJKLMÑNOPQRSTUVWXYZÁÉÍÓÚ&", "abcdefghijklmñnopqrstuvwxyzáéíóú&"), "{sector.lower()}")]'
    option_uppercase_is_visible = False
    option_is_visible = False

    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, option_xpath)))
        option_is_visible = True
    except TimeoutException:
        pass  # Suprimir el error

    try:
        option_xpath_upper = f'//h1[contains(text(),"{sector.upper()}")]'
        wait.until(EC.visibility_of_element_located((By.XPATH, option_xpath_upper)))
        option_uppercase_is_visible = True
    except TimeoutException:
        pass

    if option_is_visible or option_uppercase_is_visible:
        context.driver.save_screenshot(os.path.join(RESULTS_FOLDER, f"Page_{sector}_Loaded.png"))
        context.result = 'PASSED'
        context.error_message = ""
        assert True, "The page with option " + sector + " has loaded correctly"
    else:
        context.result = 'FAILED'
        context.error_message = f"Page {sector} not loaded correctly"
        context.driver.save_screenshot(os.path.join(RESULTS_FOLDER, f"Error_{sector}_Not_Loaded.png"))
        assert False, "The page with option " + sector + " has not loaded"


@then('I go to the home page')
def step_impl(context):
    print("\n==== Verify step: Go To Home ====\n")
    wait = WebDriverWait(context.driver, 30)
    but_home = wait.until(EC.visibility_of_element_located(BUT_HOME))
    wait.until(EC.element_to_be_clickable(BUT_HOME))
    but_home.click()
    assert context.driver.title == HOME, "Page has not loaded correctly"
    context.driver.save_screenshot(os.path.join(RESULTS_FOLDER, "To_Main_Page_Loaded.png"))
    print("\n==== Go To Home verified ====\n")


# Step function for search text
@when('I search text "{text}"')
def step_impl(context, text):
    context.current_test = text
    print(f"\n=== Verify Search for text: '{text}' ===\n")
    wait = WebDriverWait(context.driver, 30)

    try:
        search_icon = wait.until(EC.visibility_of_element_located(SEARCH_ICON))
        wait.until(EC.element_to_be_clickable(SEARCH_ICON))
        search_icon.click()

        search_input = wait.until(EC.visibility_of_element_located(SEARCH_INPUT))
        wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
        search_input.send_keys(text)

        result_search = wait.until(EC.visibility_of_element_located(RESULT_SEARCH))
        wait.until(EC.element_to_be_clickable(RESULT_SEARCH))

        context.driver.save_screenshot(os.path.join(RESULTS_FOLDER, f"Search_{text}_Results.png"))
        context.result = 'PASSED'
        context.error_message = ""
    except TimeoutException:
        context.result = 'FAILED'
        context.error_message = f"Search for '{text}' failed"
        context.driver.save_screenshot(os.path.join(RESULTS_FOLDER, f"Error_Search_{text}_Failed.png"))

    print("\n=== Search Verified ===\n")


# Tear down function to close the browser and generate a CSV
@then('I close the browser and generate a CSV for "{sector}"')
def step_impl(context, sector):
    csv_file, csv_writer = open_csv()
    log_result_to_csv(csv_writer, sector, context.result, context.error_message)
    csv_file.close()
    context.driver.quit()
    print("\n==== Browser Closed and CSV Generated ====\n")
