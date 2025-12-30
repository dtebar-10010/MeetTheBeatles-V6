# Meet The Beatles

A small Django project for demonstration and tests.

## Recommended Git setup (Windows) 

To avoid commit/editor/credential issues on Windows, we recommend the following settings:

- Use the Git credential manager for HTTPS authentication:

  git config --global credential.helper manager

- Use Visual Studio Code as the commit editor (waits for the message to be entered):

  git config --global core.editor "code --wait"

These settings help avoid problems with credential prompts and editor scripts when committing or pushing. If you prefer SSH authentication, configure an SSH key and use the `git@github.com:` remote URL instead.

---

## Deploying to PythonAnywhere 🚀

Quick steps to deploy this project to PythonAnywhere (recommended production configuration):

1. Create a secure SECRET_KEY locally and **do not** commit it to the repo:

   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

2. On PythonAnywhere (Web tab) add the following Environment variables:
   - `SECRET_KEY` (value from step 1)
   - `DJANGO_DEBUG=False`
   - `ALLOWED_HOSTS=yourusername.pythonanywhere.com`
   - Optionally: `DATABASE_URL` (if using an external DB)
   - Optionally set: `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_HSTS_SECONDS=3600`

3. Either connect your repo from the Web tab or clone it in a Bash console on PythonAnywhere.

4. In a Bash console on PythonAnywhere run:

   ```bash
   git pull origin <branch>
   python3 -m pip install -r requirements.txt
   python3 manage.py migrate --noinput
   python3 manage.py collectstatic --noinput
   ```

5. Reload the web app using the Web tab.

You can also use the included `deploy.sh` (on PythonAnywhere run `bash deploy.sh`) to perform steps 3–4. Run `python manage.py check --deploy` locally to see recommended production changes and follow the warnings before flipping `DJANGO_DEBUG` to `False`.

See `.env.example` for example environment variable names and values.
