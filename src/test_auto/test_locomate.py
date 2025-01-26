from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Fonction pour initialiser le driver et ouvrir le site
def open_site():
    driver = webdriver.Edge()
    driver.get("https://project-locomate.netlify.app")
    driver.maximize_window()
    return driver

# Test 1 : Vérifier que le bouton de connexion fonctionne correctement
def test1():
    try:
        driver = open_site()

        # Attendre que le bouton "Connexion" soit visible
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > nav > div.navbar-end > div.buttons > a"))
        )
        element.click()

        # Attendre que la popup de connexion apparaisse
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card"))
        )

        # Remplir les champs de connexion
        driver.find_element(By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card > section > div:nth-child(1) > p > input").send_keys("vince.chaumette2@gmail.com")
        driver.find_element(By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card > section > div:nth-child(2) > p > input").send_keys("Piky0404")
        driver.find_element(By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card > section > div:nth-child(3) > p > button").click()

        # Attendre que la popup disparaisse
        WebDriverWait(driver, 10).until_not(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card"))
        )

        # Vérifier le bouton "Déconnexion"
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > nav > div.navbar-end > div.buttons > a"))
        )
        button = driver.find_element(By.CSS_SELECTOR, "#app > div > nav > div.navbar-end > div.buttons > a")
        assert button.text == "Déconnexion", "Le bouton ne s'est pas transformé en 'Déconnexion'."

        # Vérifier l'affichage de l'adresse email
        email = driver.find_element(By.CSS_SELECTOR, "#app > div > nav > div.navbar-end > div.navbar-item.has-dropdown.is-hoverable.is-align-items-center > div.output > a > strong")
        assert email.text == "vince.chaumette2@gmail.com", "L'adresse email affichée est incorrecte."

        print("Test 1 réussi !")
        return True

    except Exception as e:
        print(f"Erreur lors du test 1 : {e}")
        return False

    finally:
        driver.quit()

# Test 2 : Vérifier la réservation d'un matériel
def test2():
    try:
        driver = open_site()

        # Se connecter
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > nav > div.navbar-end > div.buttons > a"))
        )
        element.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card"))
        )

        driver.find_element(By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card > section > div:nth-child(1) > p > input").send_keys("vince.chaumette2@gmail.com")
        driver.find_element(By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card > section > div:nth-child(2) > p > input").send_keys("Piky0404")
        driver.find_element(By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card > section > div:nth-child(3) > p > button").click()

        WebDriverWait(driver, 10).until_not(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card"))
        )

        # Cliquer sur le bouton "Réserver"
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(7) > button.button.is-primary.rectangle"))
        )
        driver.find_element(By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(7) > button.button.is-primary.rectangle").click()

        # Attendre que la popup de réservation apparaisse
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > div.modal.is-active > div.modal-card"))
        )

        # Effectuer une réservation de 2 matériels et valider la réservation (changer le texte de la quantité)
        reserve_quantity = driver.find_element(By.CSS_SELECTOR, "#reservation-quantity")
        reserve_quantity.clear()
        reserve_quantity.send_keys("2")
        driver.find_element(By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > div.modal.is-active > div.modal-card > section > form > div:nth-child(4) > button.button.is-primary").click()

        # Vérifier que la réservation a été effectuée
        WebDriverWait(driver, 10).until_not(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > div.modal.is-active > div.modal-card"))
        )
        button = driver.find_element(By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(7) > button.button.is-warning.rectangle")
        assert button.text == "RENDRE", "Le bouton 'Réserver' ne s'est pas transformé en 'RENDRE'."

        button.click()

        # Vérifier que le matériel a été rendu
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(7) > button.button.is-primary.rectangle"))
        )

        print("Test 2 réussi !")
        return True

    except Exception as e:
        print(f"Erreur lors du test 2 : {e}")
        return False

    finally:
        driver.quit()

# Test 3 : Vérifier que le nombre de matériels réservés est correct
def test3():
    try:
        driver = open_site()

        # Se connecter
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > nav > div.navbar-end > div.buttons > a"))
        )
        element.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card"))
        )

        driver.find_element(By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card > section > div:nth-child(1) > p > input").send_keys("vince.chaumette2@gmail.com")
        driver.find_element(By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card > section > div:nth-child(2) > p > input").send_keys("Piky0404")
        driver.find_element(By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card > section > div:nth-child(3) > p > button").click()

        WebDriverWait(driver, 10).until_not(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.modal.is-active > div.modal-card"))
        )

        # Récupérer le nombre de matériels disponibles
        available_quantity = int(driver.find_element(By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(4)").text)

        # Cliquer sur le bouton "Réserver"
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(7) > button.button.is-primary.rectangle"))
        )
        driver.find_element(By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(7) > button.button.is-primary.rectangle").click()

        # Attendre que la popup de réservation apparaisse
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > div.modal.is-active > div.modal-card"))
        )

        # Effectuer une réservation de 5 matériels et valider la réservation (changer le texte de la quantité)
        reserve_quantity = driver.find_element(By.CSS_SELECTOR, "#reservation-quantity")
        reserve_quantity.clear()
        reserve_quantity.send_keys("5")
        driver.find_element(By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > div.modal.is-active > div.modal-card > section > form > div:nth-child(4) > button.button.is-primary").click()

        # Vérifier que la réservation a été effectuée
        WebDriverWait(driver, 10).until_not(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > div.modal.is-active > div.modal-card"))
        )
        assert driver.find_element(By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(4)").text == "{}".format(available_quantity-5), "Le nombre de matériels réservés est incorrect."

        button = driver.find_element(By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(7) > button.button.is-warning.rectangle")
        assert button.text == "RENDRE", "Le bouton 'Réserver' ne s'est pas transformé en 'RENDRE'."
        button.click()

        # Vérifier que le matériel a été rendu
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div > div.content > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(7) > button.button.is-primary.rectangle"))
        )

        print("Test 3 réussi !")
        return True

    except Exception as e:
        print(f"Erreur lors du test 3 : {e}")
        return False
    
    finally:
        driver.quit()
        

if __name__ == "__main__":
    # Exécution des tests
    results = []
    results.append(test1())
    results.append(test2())
    results.append(test3())

    # Affichage des résultats
    print(f"\nRésultats des tests : {sum(results)} réussis sur {len(results)}.")
    if False in results:
        print("\nTests échoués :" + "".join([f"\n- Test {i+1}" for i, res in enumerate(results) if not res]))
