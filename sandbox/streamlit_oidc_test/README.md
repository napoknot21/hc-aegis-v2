# Streamlit OIDC Test

Mini sandbox separe du projet principal pour tester l'authentification Microsoft avec :

- `st.login()`
- `st.logout()`
- `st.user`

## 1. Installer les dependances

```bash
pip install -r sandbox/streamlit_oidc_test/requirements.txt
```

Si tu utilises une venv locale, lance de preference Streamlit depuis cette venv.

## 2. Generer le fichier secrets a partir des variables AEGIS

Le sandbox peut reutiliser directement :

- `AEGIS_MSAL_CLIENT_ID`
- `AEGIS_MSAL_CLIENT_SECRET_VALUE`
- `AEGIS_MSAL_TENANT_ID`

Puis genere la config Streamlit :

```bash
python sandbox/streamlit_oidc_test/bootstrap_secrets.py
```

Variables optionnelles :

- `AEGIS_STREAMLIT_REDIRECT_URI`
- `AEGIS_STREAMLIT_COOKIE_SECRET`

Si tu preferes, tu peux aussi partir du fichier d'exemple :

```bash
cp sandbox/streamlit_oidc_test/.streamlit/secrets.toml.example sandbox/streamlit_oidc_test/.streamlit/secrets.toml
```

## 3. Config Microsoft Entra ID

Dans ton app registration Microsoft :

- ajoute une redirect URI web : `http://localhost:8501/oauth2callback`
- utilise ton tenant ID dans `server_metadata_url`

## 4. Lancer le test

```bash
streamlit run sandbox/streamlit_oidc_test/app.py
```

## 5. Ce que tu verras

- ecran de login Microsoft
- bouton logout
- contenu de `st.user`
- verification simple des tokens exposes
