package org.example;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;


import static org.junit.Assert.assertEquals;

public class TNRA {
    private WebDriver driver;

    @Before
    public void setUp() {

        // Configure the path to the EdgeDriver
        System.setProperty("webdriver.edge.driver", "C:\\Users\\vchau\\Documents\\Scolarite\\Polytech Tours\\5A\\Test sécurité logiciel\\test_logiciel\\src\\test_auto\\msedgedriver.exe");

        // Options for Edge
        EdgeOptions options = new EdgeOptions();
        options.addArguments("--headless"); // Run Edge in headless mode

        // Initialize the driver
        driver = new EdgeDriver(options);

    }

    @Test
    public void testTitle() {
        // Ouvrez le site web
        driver.get("https://6781299acf9bc609ee48ce4b--startling-dasik-debb61.netlify.app/");

        // Vérifiez le titre de la page
        String expectedTitle = "Example Domain";
        String actualTitle = driver.getTitle();
        assertEquals(expectedTitle, actualTitle);
    }

    @Test
    public void testElementById() {
        // Ouvrez le site web
        driver.get("https://6781299acf9bc609ee48ce4b--startling-dasik-debb61.netlify.app/");

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