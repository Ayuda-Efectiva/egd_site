# EGD Site based on Frappe

Effective Altruism Day Website based on Frappe Framework.


# Setup locally

## Install Frappe 14
Follow all steps for your OS within official guide: [https://frappeframework.com/docs/v14/user/en/installation](https://frappeframework.com/docs/v14/user/en/installation).


## Create your personal "frappe-bench" environment (customizable)

Into your home folder:

```
cd ~
bench init frappe-bench
```

## Create a new site inside your "frappe-bench" folder

```
cd ~/frappe-bench
bench new-site egd.local
```

## Install app on created site

```
cd ~/frappe-bench
bench get-app git@github.com:Ayuda-Efectiva/egd_site.git
bench update --requirements
bench --site egd.local install-app egd_site
```

## Load your local site

```
cd ~/frappe-bench
bench start
```

Add **egd.local** to your hosts file pointing to **localhost** and load **egd.local:[port]** in your browser. If you are not sure about the port, just check the port inside file "~/frappe-bench/Procfile" within line starting with "web:"

Now you can load the url http://egd.local:[port] into your browser.

# Multilanguage

There are two folders with translatable or localizable text.


## Markdown/HTML pages inside /egd_site/www/xx

Whole site navigation structure with code and translatable text. There is one folder **xx** per language.

At the top of the markdown pages there are some variables. Two of them needs translation too:

  * **title**: html page title
  * **meta_description**: Meta tag description


## xx.csv files inside /egd_site/translations/

Contains one file per language named as **xx.csv** where **xx** is the language.

Each CSV file is formed by three columns:

  * **Column 1 (do not modify)**: File where the translation key is located (it could be in different locations too)
  * **Column 2 (do not modify)**: Translation key
  * **Column 1**: Translation for CSV language. You can use **,** (comma) but you need to wrap whole translation with **"**.


# License

MIT
