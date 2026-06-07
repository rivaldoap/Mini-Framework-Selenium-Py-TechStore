import os
import sys
import time

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

import pytest
from Pages.ObjectRepository_Global import *
from Excel.SignUp.excel_reader_signup_positive import signup_positive
from Excel.SignUp.excel_reader_signup_negative import signup_negative
from Utils.helper import *
from Utils.driver_factory import *

@pytest.mark.parametrize("data_excel", signup_positive())
def test_signup_positive(data_excel):

    driver = start_browser()
    driver.get(data_excel.get("URL"))

    click(driver, BTN_SIGNUP_FRONT)
    input_text(driver, FLD_SIGNUP_USERNAME, data_excel.get("SIGNUP_USERNAME"))
    input_text(driver, FLD_SIGNUP_PASSWORD, data_excel.get("SIGNUP_PASSWORD"))
    click(driver, BTN_SIGNUP)
    assert_element_displayed(driver, LBL_USER_INFO)

    print(f"User {data_excel.get('SIGNUP_USERNAME')} berhasil didaftarkan!")
    
    time.sleep(2)
    click(driver, BTN_LOGOUT)
    driver.quit()


@pytest.mark.parametrize("data_excel", signup_negative())
def test_signup_negative(data_excel):
    driver = start_browser()
    driver.get(data_excel.get("URL"))

    click(driver, BTN_SIGNUP_FRONT)
    input_text(driver, FLD_SIGNUP_USERNAME, data_excel.get("SIGNUP_USERNAME"))
    input_text(driver, FLD_SIGNUP_PASSWORD, data_excel.get("SIGNUP_PASSWORD"))
    click(driver, BTN_SIGNUP)

    error_message = data_excel.get("ASSERTION")

    #
    if "Username" in error_message and "Password" in error_message:
        assert_text_equals_validasi(driver, LBL_NEGATIVE_SIGNUP_USERNAME, "Username minimal 3 karakter.")
        assert_text_equals_validasi(driver, LBL_NEGATIVE_SIGNUP_PASSWORD, "Password minimal 6 karakter.")
    elif "Username" in error_message:
        assert_text_equals_validasi(driver, LBL_NEGATIVE_SIGNUP_USERNAME, error_message)
    elif "Password" in error_message:
        assert_text_equals_validasi(driver, LBL_NEGATIVE_SIGNUP_PASSWORD, error_message)
    
    time.sleep(2)
    driver.quit()