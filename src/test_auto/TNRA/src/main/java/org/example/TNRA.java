package org.example;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class TNRA {
    private WebDriver driver;

    @Before
    public void setUp() {
        // Configurez le chemin vers le driver Chrome
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");

        // Options pour Chrome
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless"); // Exécute Chrome en mode headless (sans interface graphique)

        // Initialisez le driver
        driver = new ChromeDriver(options);
    }

    @Test
    public void testTitle() {
        // Ouvrez le site web
        driver.get("https://example.com");

        // Vérifiez le titre de la page
        String expectedTitle = "Example Domain";
        String actualTitle = driver.getTitle();
        assertEquals(expectedTitle, actualTitle);
    }

    @Test
    public void testElementById() {
        // Ouvrez le site web
        driver.get("https://example.com");

        // Trouvez l'élément par son ID et vérifiez son texte
        WebElement element = driver.findElement(By.id("example-id"));
        String expectedText = "Expected Text";
        String actualText = element.getText();
        assertEquals(expectedText, actualText);
    }

    @After
    public void tearDown() {
        // Fermez le navigateur
        if (driver != null) {
            driver.quit();
        }
    }
}