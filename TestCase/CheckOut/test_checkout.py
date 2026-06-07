import os
import sys
import time

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

import pytest
from TestCase.Login.test_login import test_login as perform_login
from Pages.ObjectRepository_Global import *
from Excel.CheckOut.excel_reader_checkout_positive import(
    checkout_positive as read_excel_positive
)
from Utils.helper import *

cek_pilihan_excel = read_excel_positive()

@pytest.mark.parametrize("data_excel", cek_pilihan_excel)
def test_checkout_positive(data_excel):
    if not data_excel:
        pytest.skip("Tidak ada baris data yang ditandai 'RUN'.")

    driver = perform_login()

    try:
        list_produk_kolom = [
            {"nama": data_excel.get("PRODUK_1"), "warna": data_excel.get("WARNA_PRODUK_1")},
            {"nama": data_excel.get("PRODUK_2"), "warna": data_excel.get("WARNA_PRODUK_2")},
            {"nama": data_excel.get("PRODUK_3"), "warna": data_excel.get("WARNA_PRODUK_3")},
        ]

        for produk in list_produk_kolom:
            if not produk["nama"]:
                continue
            
            # Klik nama produk untuk memunculkan Pop-up Detail
            NAMA_PRODUK_LOCATOR = get_locator_nama_produk(produk['nama'])
            scroll_to_element(driver, NAMA_PRODUK_LOCATOR)
            click(driver, NAMA_PRODUK_LOCATOR)
            
            time.sleep(1.5)
            
            # Pilih Warna di dalam pop-up
            if produk["warna"]:
                RADIO_WARNA = get_locator_pilih_warna_produk(produk["nama"], produk["warna"])
                scroll_to_element(driver, RADIO_WARNA)
                time.sleep(0.5)
                click(driver, RADIO_WARNA)  # <--- Jauh lebih clean, pintar, dan tanpa hardcode
                print(f"[COLOR] Berhasil memilih warna '{produk['warna']}' untuk {produk['nama']}")

            BTN_ADD_TO_CHART = get_locator_add_to_cart(produk["nama"])
            scroll_to_element(driver, BTN_ADD_TO_CHART)
            click(driver, BTN_ADD_TO_CHART)
            time.sleep(1.5)

            # Alert Handle
            handle_browser_alert(driver)
            time.sleep(1)

        click(driver, BTN_CHART)
        click(driver, BTN_PLACE_ORDER)
        input_text(driver, FLD_FULLNAME, data_excel["FULLNAME"])
        # Ambil data dari kolom Excel
        country_dari_excel = data_excel.get("COUNTRY")
        if country_dari_excel:
            click_dropdownlist(driver, DDL_COUNTRY, country_dari_excel)
            print(f"[COUNTRY] Berhasil memilih country : {country_dari_excel}")
        
        city_dari_excel = data_excel.get("CITY")
        if city_dari_excel:
            click_dropdownlist(driver, DDL_SELECT_CITY, city_dari_excel)
            print(f"[CITY] Berhasil memilih city : {city_dari_excel}")
        
        input_text(driver, FLD_CARD_NUMBER, data_excel["CARD_NUMBER"])
        month_dari_excel = data_excel.get("MONTH")
        if month_dari_excel:
            click_dropdownlist(driver, DDL_MONTH, month_dari_excel)
            print(f"[MONTH] Berhasil memilih month: {month_dari_excel}")
        
        year_dari_excel = data_excel.get("YEAR")
        if year_dari_excel:
            click_dropdownlist(driver, DDL_YEAR, year_dari_excel)
            print(f"[YEAR] Berhasil memilih month: {year_dari_excel}")
        
        scroll_to_element(driver, BTN_PAY_NOW)
        click(driver, BTN_PAY_NOW)
        time.sleep(1)
        # handle_browser_alert(driver)
        nama_user = data_excel.get("FULLNAME")
        text_expectation = f"Terima kasih {nama_user}! Pesanan Anda telah dibuat."
        assert_and_handle_browser_alert(driver, text_expectation)
        time.sleep(1)

    except Exception as e:
        print(f"Terjadi error saat checkout: {e}")
        raise e
    finally:
        click(driver, BTN_LOGOUT)
        driver.quit()