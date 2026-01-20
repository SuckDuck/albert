from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pynput import keyboard
from pathlib import Path
import pyautogui
import re, json
import time

BASE_DIR = Path(__file__).resolve().parent
PROFILE_DIR = BASE_DIR / "selenium_profile"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)
APP_URL = "https://grupomaz.bitrix24.com/marketplace/app/133/"

# set the profile dir
options = Options()
options.add_argument(f"--user-data-dir={PROFILE_DIR}")
options.add_argument("--profile-directory=Default")

# remove the "Chrome is being controlled..." label
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# other stuff
options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
options.add_argument("--start-fullscreen")

# use this to search IDs:
# curl -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d '{"filter":{"NAME":"Misael%"}}' https://grupomaz.bitrix24.com/rest/49171/dcrc5uvz83uiac14/user.get > response.json
users_queue = [
    #49171, Esteban Huertas
    149,   #Patrick Batista
    153,   #Luis Valerin
    74955, #David Lopez
    141291,#Jose Arrieta
    9      #Misael Artavia
]
current_user = 0

albert_options = {
    "callKey":"KeyX",
    "scroll":"130",
    "user":users_queue[0],
    "wasConnected":True,
}

# < ==== INPUT INIT ==============================================>
KEY = keyboard.KeyCode.from_char("x")
held = set()
down = set()
up = set()
panic_timer = 0.0

def on_press(key):
    if key not in held:
        down.add(key)
    held.add(key)

def on_release(key):
    held.discard(key)
    up.add(key)

keyboard.Listener(on_press=on_press, on_release=on_release).start()

def set_focus(d):
    wait = WebDriverWait(d, 10**9)
    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.app-frame")))
    wait.until(lambda d: iframe.size["width"] > 10 and iframe.size["height"] > 10)
    time.sleep(1)

    #in case of menu overlays?
    pyautogui.keyDown("esc")
    time.sleep(0.01)
    pyautogui.keyUp("esc")
    time.sleep(0.2)

    w, h = pyautogui.size()
    x = w // 3
    y = h // 2
    pyautogui.click(x, y)

def inject_albert_options(driver, options: dict, timeout: int = 20):
    wait = WebDriverWait(driver, timeout)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.app-frame")))

        iframes = driver.find_elements(By.CSS_SELECTOR, "iframe.app-frame")
        if not iframes:
            raise RuntimeError("No iframes found with class app-frame")

        for iframe in iframes:
            driver.switch_to.default_content()
            driver.switch_to.frame(iframe)

            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body#boring-albert-kiosk")))
                driver.execute_script("window.albertOptions = arguments[0];", options)
                return
            except TimeoutException:
                continue

        raise RuntimeError("Could not find the correct iframe (with body#boring-albert-kiosk)")

    finally:
        driver.switch_to.default_content()

def install_albert_console_hook(driver):
    driver.execute_script("""
    (function () {
      if (window.__albertHookInstalled) return;
      window.__albertHookInstalled = true;

      const origLog = console.log;

      console.log = function (...args) {
      if (args[0] === "_onCallLeave" && args[1] && args[1].call && ("wasConnected" in args[1].call)) {
        origLog(JSON.stringify({
          albertEvent: "onCallLeave",
          wasConnected: args[1].call.wasConnected
        }));
      }
      return origLog.apply(console, args);
    };
    })();
    """)

while True:
    driver = webdriver.Chrome(options=options)
    driver.get(APP_URL)
    inject_albert_options(driver, albert_options, 10**9)
    current_user += 1
    if current_user >= len(users_queue):
        current_user = 0
    albert_options["user"] = users_queue[current_user]
    albert_options["wasConnected"] = True
    install_albert_console_hook(driver)
    set_focus(driver)
   
    try:
        while True:
            time.sleep(1/30)
            # initialize eveeything if the front end gets reloaded
            nav_type = driver.execute_script("""return performance.getEntriesByType('navigation')[0]?.type""")
            if (nav_type == "reload" or panic_timer > 3):
                panic_timer = -1
                driver.get(APP_URL)
                current_user += 1
                if current_user >= len(users_queue):
                    current_user = 0
                albert_options["user"] = users_queue[current_user]
                albert_options["wasConnected"] = True
                inject_albert_options(driver, albert_options, 10**9)
                install_albert_console_hook(driver)
                set_focus(driver)

            # bitrix doesn't return to the app page once the call is finished
            # so we have to do this shit to return main page
            for entry in driver.get_log("browser"):
              msg = entry.get("message", "")
              if '\\"albertEvent\\":\\"onCallLeave\\"' in msg:
                  m = re.search(r'\{\\\"albertEvent\\\":\\\"onCallLeave\\\".*?\}', entry.get("message", ""))
                  payload = json.loads(m.group(0).replace('\\"', '"'))
                  
                  # reseting the app...
                  albert_options["wasConnected"] = payload["wasConnected"]
                  driver.get(APP_URL)
                  inject_albert_options(driver, albert_options, 10**9)
                  current_user += 1
                  if current_user >= len(users_queue):
                      current_user = 0
                  albert_options["user"] = users_queue[current_user]
                  albert_options["wasConnected"] = True
                  install_albert_console_hook(driver)
                  set_focus(driver)

            # < ==== INPUT LOOP ==============================================>
            if KEY in held and panic_timer > -1: panic_timer += 1/30
            if KEY in up: panic_timer = 0
            
            down.clear()
            up.clear()

            driver.title #force an action

    except:
        try: driver.quit()
        except: pass
        
        print("Browser closed, launching again...")
        time.sleep(5)

#Correo :           albert#.electromaz@gmail.com
#Contraseña GMAIL:  MaZ$2023.
#Contraseña BITRIX: 0123456789Aa