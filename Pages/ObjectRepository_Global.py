from selenium.webdriver.common.by import By

# LOGIN
BTN_LOGIN_FRONT                 = (By.XPATH, "//button[@id='btn-login']")
FLD_USERNAME                    = (By.XPATH, "//input[@id='input-login-username']")
FLD_PASSWORD                    = (By.XPATH, "//input[@id='input-login-password']")
BTN_LOGIN                       = (By.XPATH, "//button[@class='btn btn-primary'][normalize-space()='Log in']")

# SIGNUP
BTN_SIGNUP_FRONT                = (By.XPATH, "//button[@id='btn-signup']")
FLD_SIGNUP_USERNAME             = (By.XPATH, "//input[@id='input-signup-username']")
FLD_SIGNUP_PASSWORD             = (By.XPATH, "//input[@id='input-signup-password']")
BTN_SIGNUP                      = (By.XPATH, "//button[@class='btn btn-primary'][normalize-space()='Sign up']")

LBL_USER_INFO                   = (By.XPATH, "//div[@class='user-info']")
LBL_TOAST_INFO                  = (By.XPATH, "//span[@id='toast-msg']")
# LBL_TOAST_SUCCESS_LOGOUT        = (By.XPATH, "//span[@id='toast-msg']")

LBL_NEGATIVE_SIGNUP_USERNAME    = (By.XPATH, "//div[@id='signup-username-error']")
LBL_NEGATIVE_SIGNUP_PASSWORD    = (By.XPATH, "//div[@id='signup-password-error']")

# LOGOUT
BTN_LOGOUT                      = (By.XPATH, "//button[normalize-space()='Log out']")

# HEADER Tech Store
LBL_HEADER_TECHSTORE            = (By.XPATH, "//a[@aria-label='TechStore Home']")

BTN_ADD_TO_CHART                = (By.XPATH, "//button[@id='detail-btn-add-cart']")

BTN_CHART                       = (By.XPATH, "//button[@aria-label='Open cart']")
BTN_PLACE_ORDER                 = (By.XPATH, "//button[contains(text(),'Place Order →')]")

FLD_FULLNAME                    = (By.XPATH, "//input[@id='order-name']")
DDL_COUNTRY                     = (By.XPATH, "//select[@id='order-country']")
DDL_SELECT_CITY                 = (By.XPATH, "//select[@id='order-city']")
FLD_CARD_NUMBER                 = (By.XPATH, "//input[@id='order-card']")
DDL_MONTH                       = (By.XPATH, "//select[@id='order-month']")
DDL_YEAR                        = (By.XPATH, "//select[@id='order-year']")
BTN_PAY_NOW                     = (By.XPATH, "//button[normalize-space()='Pay Now']")