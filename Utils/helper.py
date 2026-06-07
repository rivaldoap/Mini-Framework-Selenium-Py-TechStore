import os
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from Pages.ObjectRepository_Global import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

### HIGHLIGHT ###
def Highlight(driver, element, blink=5):

    for i in range(blink):
        # HIGHLIGHT ON
        driver.execute_script("""
            arguments[0].style.border='2px solid lime';
            arguments[0].style.boxShadow='0 0 5px lime';
        """, element)
        time.sleep(0.2)

        # HIGHLIGHT OFF
        driver.execute_script("""
            arguments[0].style.border='';
            arguments[0].style.boxShadow='';
        """, element)
        time.sleep(0.2)

# BASIC FUNCTION
# def click(driver, locator, timeout=10):
#     element = WebDriverWait(driver, timeout).until(
#         EC.element_to_be_clickable(locator)
#     )
#     Highlight(driver, element)
#     time.sleep(1.5)
#     element.click()

def click(driver, locator, timeout=5):
    try:
        # Jalur Utama: Tunggu sampai element clickable lalu klik biasa
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        Highlight(driver, element)
        time.sleep(1.5)
        element.click()
    except Exception:
        # Jalur Cadangan: Jika terintersep animasi pop-up, sikat pakai JS
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        driver.execute_script("arguments[0].click();", element)


def input_text(driver, locator, text, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )
    Highlight(driver, element)
    time.sleep(1.5)
    if text is None:
        text = ""
    element.clear()
    element.send_keys(text)

def click_dropdownlist(driver, locator_dropdown, teks_pilihan, timeout=5):
    
    # Fungsi global dropdown tingkat lanjut. 
    # Mendukung dropdown native <select> (sangat stabil untuk dropdown berantai negara/kota) dan custom dropdown (li/div).
    
    pilihan_clean = str(teks_pilihan).strip()
    
    # 1. Tunggu hingga elemen dropdown utama siap di halaman, lalu scroll ke elemen tersebut
    dropdown_element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator_dropdown)
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_element)
    time.sleep(0.5)

    # 2. JALUR UTAMA: Jika dropdown menggunakan tag HTML <select> native
    if dropdown_element.tag_name == "select":
        try:
            # Gunakan class Select bawaan Selenium (paling direkomendasikan untuk updateCities())
            select = Select(dropdown_element)
            
            # Coba pilih berdasarkan teks parsial yang mengandung kata kunci dari Excel
            for option in select.options:
                if pilihan_clean.lower() in option.text.lower():
                    select.select_by_visible_text(option.text)
                    
                    if "country" in str(locator_dropdown).lower():
                        print("[INFO] Dropdown Country terpilih, menunggu sinkronisasi list City...")
                        time.sleep(1.5)
                    return
        except Exception as e:
            print(f"[INFO] Gagal menggunakan Select Native, mencoba Jalur Cadangan: {e}")

    # JALUR CADANGAN: Untuk custom dropdown (div/li) atau jika jalur utama gagal
    click(driver, locator_dropdown, timeout)
    time.sleep(0.8)
    
    xpath_opsi = (
        f"//option[contains(normalize-space(), '{pilihan_clean}')] | "
        f"//li[contains(normalize-space(), '{pilihan_clean}')] | "
        f"//div[contains(normalize-space(), '{pilihan_clean}')]"
    )
    locator_opsi = (By.XPATH, xpath_opsi)
    click(driver, locator_opsi, timeout)
    
    if "country" in str(locator_dropdown).lower():
        time.sleep(1.5)


def get_text(driver, locator, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )
    Highlight(driver, element)
    time.sleep(1.5)
    return element.text


# Untuk menemukan produk yang ingin dipilih
def get_locator_produk(nama_produk):
    xpath_statis = (
        f"//div[text()='{nama_produk}']/ancestor::div[@class='inventory_item']"
    )
    # Cari tombol 'Add to cart' yang berada di dalam kotak produk tersebut
    return (By.XPATH, xpath_statis + "//button[text()='Add to cart']")

# SCROLL BERDASARKAN PIXEL (Misal: turun 500 pixel)
# Scroll layar berdasarkan koordinat X (horizontal) dan Y (vertical)
def scroll_by_pixel(driver, x=0, y=500):
    driver.execute_script(f"window.scrollBy({x}, {y});")
    time.sleep(1.5)


# Untuk scroll presisi ke object yang dituju
def scroll_to_element(driver, locator, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )
    # scroll element ke tengah layar
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", element
    )
    Highlight(driver, element)
    time.sleep(1.5)


# Scroll layar ke bagian paling atas halaman web
def scroll_to_top(driver):
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)


# Scroll layar keatas secara halus
def scroll_to_top_smooth(driver):
    driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
    time.sleep(1.5)


# Memastikan suatu element muncul di layar halaman web
def assert_element_displayed(driver, locator, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        Highlight(driver, element)
        # print(f"\n[ASSERT] Sukses! Element {locator} terlihat di layar.")
        assert element.is_displayed() is True
    except:
        assert False, f"Gagal! Element dengan locator {locator} tidak ditemukan atau tidak muncul di layar."


# Assertion untuk memastikan text yang muncul di web sesuai dengan ekspektasi sesuai data dari excel
def assert_text_equals_validasi(driver, locator, expected_text, timeout=10):
    try:
        # Tunggu sampai elemen tersebut benar-benar muncul di layar
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        Highlight(driver, element)
        # Mengambil text asli dari elemen web tersebut (.text)
        actual_text = element.text.strip()
        print(f"[ASSERT] Menyamakan teks. Web: '{actual_text}' | Excel: '{expected_text}'")
        
        # Melakukan pengujian / assertion
        assert actual_text == str(expected_text).strip(), \
            f"Gagal! Teks di web adalah '{actual_text}', tetapi ekspektasinya '{expected_text}'"
            
        print(f"[ASSERT] Sukses! Teks cocok sesuai ekspektasi.")
        
    except TimeoutException:
        raise AssertionError(f"Gagal! Elemen dengan locator {locator} tidak ditemukan dalam waktu {timeout} detik.")

def assert_and_handle_browser_alert(driver, ekspektasi_teks, timeout=5):
    # Untuk mengambil teks dari browser alert, melakukan assertion, dan otomatis menutup alert (klik OK).

    WebDriverWait(driver, timeout).until(EC.alert_is_present())
    
    alert = driver.switch_to.alert
    teks_alert = alert.text
    print(f"[ALERT DETECTED] Teks pada alert: '{teks_alert}'")
    
    # Jalankan Assertion (Validasi teks dari Excel / ekspektasi)
    assert ekspektasi_teks in teks_alert, f"Gagal! Ekspektasi: '{ekspektasi_teks}', tapi tertera: '{teks_alert}'"
    print(f"[ASSERTION SUCCESS] Teks alert valid!")
    
    # Klik OK / Accept untuk menutup alert
    alert.accept()
    print("[ALERT CLOSED] Berhasil klik OK pada browser alert.")

def get_locator_nama_produk(nama_produk):
    # Mencari nama produk di halaman utama untuk diklik agar pop-up terbuka
    return (By.XPATH, f"//div[@class='product-name' and text()='{nama_produk}']")


def get_locator_nama_produk(nama_produk):
    return (By.XPATH, f"//div[@class='product-name' and text()='{nama_produk}']")

def get_locator_pilih_warna_produk(nama_produk, warna):
    # Membersihkan input jika di Excel terlanjur tertulis 'color-swatch blue'
    warna_bersih = warna.split()[-1] if " " in warna else warna
    warna_kapital = warna_bersih.capitalize()
    
    # XPath dinamis gabungan tanpa wall of text
    xpath = f"//div[@id='detail-color-options']//label[contains(., '{warna_kapital}')] | //div[@id='detail-color-options']//div[contains(@class, '{warna_bersih}')]"
    return (By.XPATH, xpath)

def get_locator_add_to_cart(nama_produk):
    xpath = "//div[@id='detail-color-options']/..//button[contains(@class, 'add-cart-btn')] | //button[contains(text(), 'Add to Cart')]"
    return (By.XPATH, xpath)

def handle_browser_alert(driver, timeout=10):
    """
    Fungsi global untuk menghandle JavaScript Browser Alert (Pop-up OK).
    Jika expected_alert_text diisi, fungsi akan memvalidasi teks di dalam alert tersebut.
    """
    try:
        # Tunggu sampai Alert dari browser benar-benar muncul
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        
        # Pindah fokus Selenium ke jendela Alert tersebut
        alert = driver.switch_to.alert
        actual_text = alert.text.strip()
        print(f"[ALERT DETECTED] Teks pada alert: '{actual_text}'")
        
        # Klik tombol 'OK' pada alert
        alert.accept()
        print("[ALERT CLOSED] Berhasil klik OK pada browser alert.")
        
    except TimeoutException:
        raise AssertionError("Gagal! Browser alert tidak muncul setelah ditunggu.")

# LOGOUT #
def logout(driver):
    click(driver, BTN_LOGOUT)
    time.sleep(1.5)
    assert_element_displayed(driver, LBL_TOAST_INFO)