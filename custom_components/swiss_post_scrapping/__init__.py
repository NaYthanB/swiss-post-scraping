from homeassistant.helpers import discovery
import logging
from datetime import timedelta
from homeassistant.helpers.event import track_time_interval
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "swiss_post_scrapping"

_LOGGER = logging.getLogger(__name__)
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Swiss Post Scrapping from a config entry."""
    
    # # Charger la plateforme sensor
    # hass.async_create_task(
    #     hass.config_entries.async_forward_entry_setup(entry, "sensor")
    # )
    
    # return True
    # Lire les options depuis l'entrée de configuration
    email = entry.data.get("email")
    password = entry.data.get("password")
    interval_minutes = entry.data.get("interval", 5)
    interval = timedelta(minutes=interval_minutes)

    async def handle_run_selenium(call):
        """Service pour exécuter le script Selenium avec les paramètres."""
        from selenium import webdriver
        # from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium import webdriver
        from selenium.webdriver.common.action_chains import ActionChains
        import time

        # options = Options()
        # options.add_argument("--verbose")

        # driver = webdriver.Chrome(options=options)


        # Configurer les options de Firefox
        options = Options()
        options.headless = True  # Pour exécuter Firefox en mode headless (sans interface graphique)

        # Créer une instance de WebDriver avec Firefox
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(565, 700)

        try:
            tracking_numbers = []
            
            # Go to the Swiss Post login page
            driver.get("https://www.post.ch/en/login")

            # Fill in the login fields
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            password_input = driver.find_element(By.ID, "password")
            username_input.send_keys(email)
            password_input.send_keys(password)

            # Click on the login button
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.next_icon.btn-custom.active"))
            )
            login_button.click()
            time.sleep(1)

            # Go to the package tracking page
            driver.get("https://service.post.ch/ekp-web/ui/list?service=klp")
            
            # Click on the accept cookies button
            window_width = driver.execute_script("return window.innerWidth")
            window_height = driver.execute_script("return window.innerHeight")
            actions = ActionChains(driver)
            time.sleep(3)
            actions.move_by_offset(500, 500).click().perform()
            
            # Click on the delivered package menu
            delivered_package_menu = driver.find_element(By.ID, "ngb-nav-1")
            driver.execute_script("arguments[0].scrollIntoView();", delivered_package_menu)
            time.sleep(1)
            delivered_package_menu.click()
            
            # Get the tracking numbers
            rows = driver.find_elements(By.CSS_SELECTOR, ".card-body")
            for row in rows:
                driver.execute_script("arguments[0].scrollIntoView();", row)
                time.sleep(1)
                row.click()
                tracking_number = driver.find_elements(By.CSS_SELECTOR, ".h5.fw-light")
                tracking_numbers.append(tracking_number[0].text.replace(".", ""))
                driver.back()

            print("Numéros de suivi:", tracking_numbers)
            
            # Stocker les numéros de suivi dans hass.data
            hass.data[DOMAIN] = {
                "tracking_numbers": tracking_numbers
            }

        finally:
            driver.quit()
            
        # Enregistrer un service qui déclenche le script Selenium
    hass.services.register(DOMAIN, "run_selenium", handle_run_selenium)

        # Planifier une exécution périodique
    async def periodic_execution(now):
            handle_run_selenium(None)

    track_time_interval(hass, periodic_execution, interval)

    _LOGGER.info(f"My Selenium Integration is set up with swiss post login : {email} and interval: {interval_minutes} minutes.")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

# def setup(hass, config):
#     """Set up the My Selenium Integration."""
#     # Lire les options depuis la configuration
#     email = config.get(DOMAIN, {}).get("email", "")
#     password = config.get(DOMAIN, {}).get("password", "")
#     interval_minutes = config.get(DOMAIN, {}).get("interval", 5)
#     # Découverte et enregistrement du capteur
#     interval = timedelta(minutes=interval_minutes)  # 

    
# from homeassistant.helpers import discovery
# import logging
# from datetime import timedelta
# from homeassistant.helpers.event import track_time_interval
# from homeassistant.config_entries import ConfigEntry
# from homeassistant.core import HomeAssistant

# DOMAIN = "swiss_post_scrapping"

# _LOGGER = logging.getLogger(__name__)
# async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#     """Set up Swiss Post Scrapping from a config entry."""
    
#     # # Charger la plateforme sensor
#     # hass.async_create_task(
#     #     hass.config_entries.async_forward_entry_setup(entry, "sensor")
#     # )
    
#     # return True
#     # Lire les options depuis l'entrée de configuration
#     email = entry.data.get("email")
#     password = entry.data.get("password")
#     interval_minutes = entry.data.get("interval", 5)
#     interval = timedelta(minutes=interval_minutes)

#     async def handle_run_selenium(call):
#         """Service pour exécuter le script Selenium avec les paramètres."""
#         from selenium import webdriver
#         # from selenium.webdriver.chrome.options import Options
#         from selenium.webdriver.firefox.options import Options
#         from selenium.webdriver.common.by import By
#         from selenium.webdriver.support.ui import WebDriverWait
#         from selenium.webdriver.support import expected_conditions as EC
#         from selenium import webdriver
#         from selenium.webdriver.common.action_chains import ActionChains
#         import time

#         # options = Options()
#         # options.add_argument("--verbose")

#         # driver = webdriver.Chrome(options=options)


#         # Configurer les options de Firefox
#         options = Options()
#         options.headless = True  # Pour exécuter Firefox en mode headless (sans interface graphique)

#         # Créer une instance de WebDriver avec Firefox
#         driver = webdriver.Firefox(options=options)
#         driver.set_window_size(565, 700)

#         try:
#             tracking_numbers = []
            
#             # Go to the Swiss Post login page
#             driver.get("https://www.post.ch/en/login")

#             # Fill in the login fields
#             username_input = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.ID, "email"))
#             )
#             password_input = driver.find_element(By.ID, "password")
#             username_input.send_keys(email)
#             password_input.send_keys(password)

#             # Click on the login button
#             login_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.next_icon.btn-custom.active"))
#             )
#             login_button.click()
#             time.sleep(1)

#             # Go to the package tracking page
#             driver.get("https://service.post.ch/ekp-web/ui/list?service=klp")
            
#             # Click on the accept cookies button
#             window_width = driver.execute_script("return window.innerWidth")
#             window_height = driver.execute_script("return window.innerHeight")
#             actions = ActionChains(driver)
#             time.sleep(3)
#             actions.move_by_offset(500, 500).click().perform()
            
#             # Click on the delivered package menu
#             delivered_package_menu = driver.find_element(By.ID, "ngb-nav-1")
#             driver.execute_script("arguments[0].scrollIntoView();", delivered_package_menu)
#             time.sleep(1)
#             delivered_package_menu.click()
            
#             # Get the tracking numbers
#             rows = driver.find_elements(By.CSS_SELECTOR, ".card-body")
#             for row in rows:
#                 driver.execute_script("arguments[0].scrollIntoView();", row)
#                 time.sleep(1)
#                 row.click()
#                 tracking_number = driver.find_elements(By.CSS_SELECTOR, ".h5.fw-light")
#                 tracking_numbers.append(tracking_number[0].text.replace(".", ""))
#                 driver.back()

#             print("Numéros de suivi:", tracking_numbers)
            
#             # Stocker les numéros de suivi dans hass.data
#             hass.data[DOMAIN] = {
#                 "tracking_numbers": tracking_numbers
#             }

#         finally:
#             driver.quit()
            
#         # Enregistrer un service qui déclenche le script Selenium
#     hass.services.register(DOMAIN, "run_selenium", handle_run_selenium)

#         # Planifier une exécution périodique
#     async def periodic_execution(now):
#             handle_run_selenium(None)

#     track_time_interval(hass, periodic_execution, interval)

#     _LOGGER.info(f"My Selenium Integration is set up with swiss post login : {email} and interval: {interval_minutes} minutes.")
#     return True

# async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#     """Unload a config entry."""
#     unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
#     if unload_ok:
#         hass.data[DOMAIN].pop(entry.entry_id)
#     return unload_ok

# # def setup(hass, config):
# #     """Set up the My Selenium Integration."""
# #     # Lire les options depuis la configuration
# #     email = config.get(DOMAIN, {}).get("email", "")
# #     password = config.get(DOMAIN, {}).get("password", "")
# #     interval_minutes = config.get(DOMAIN, {}).get("interval", 5)
# #     # Découverte et enregistrement du capteur
# #     interval = timedelta(minutes=interval_minutes)  # 

    