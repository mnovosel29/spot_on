# Requirements:
- Python 3.11
- npm: '9.5.1',
- node: '18.16.0'

# Installation:

Copy the `.env.example` file to `.env` and update the values as needed.

Install python requirements:
```bash
pip install -r requirements.txt
```
Install Node.js dependencies:
```bash
npm install
```
Initialize the database:
```bash
flask db upgrade
```

Watch changes in Tailwind CSS: 
```bash
npx tailwindcss -i ./app/static/src/input.css -o ./app/static/dist/css/output.css --watch
```


# Adding Translations

**Introduction**

This document outlines the steps involved in adding a new language for internationalization (i18n) within your Flask application using Flask-Babel. By following these steps, you can seamlessly extend your application's reach to a wider audience.

**Prerequisites**

- A Flask application with Flask-Babel integration.
- Basic familiarity with terminal commands and text editing.

**Steps**

1. **Configuration Update:**

   - Locate your application's configuration file (typically `.env`).
   - Update the following environment variables:
     - `LANGUAGES`: Comma-separated list of supported language codes (e.g., `en,hr,<new-language-code>`)
     - `DEFAULT_LANGUAGE`: Set the default language for your application (`<new-language-code>`)
   - Replace `<new-language-code>` with the ISO 639-1 code for the language you're adding (e.g., `es` for Spanish, `de` for German).


2. **Extracting Translatable Strings:**

   - Open your terminal and navigate to your project's root directory.
   - Execute the following command, replacing `babel.cfg` with your Babel configuration file if it has a different name:

     ```bash
     pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
     ```

   - This command identifies strings marked for translation using the `_l` gettext function and generates a `.pot` file (`messages.pot`) containing all translatable content.


3. **Initializing New Language:**

   - Use the `pybabel` tool to create a new language file based on the `.pot` file:

     ```bash
     pybabel init -i messages.pot -d app/translations -l <language-code>
     ```

   - Replace `<language-code>` with the ISO 639-1 code of the desired language.
   - This command creates a new `.po` file (e.g., `es.po` for Spanish) within the `app/translations` directory. This file serves as the template for translations in your new language.


4. **Translating Strings:**

   - Open the newly created `.po` file located in `app/translations/<language-code>/LC_MESSAGES` in a text editor and provide translations for each string. 

   
5. **Compile translations:** 
   - Compile the .po file into a .mo (Machine Object) file, which is the format that Babel can use to serve your translations: 
   
    ```bash
    pybabel compile -d app/translations
    ```
   
    - To compile translations for the `flask_security` domain, you would run the following command:

    ```bash
    pybabel compile -d app/translations/ -i app/translations/<language-code>/LC_MESSAGES/flask_security.po -l <language-code> -D flask_security
    ```


6. Restart the application: Finally, restart your application to apply the new translations. 
