# ✏️ Opinion Development Notebook

Create printable notebooks in booklet format to yelp you keep track and develop informed opinions about the world.

The notebooks are generated from this [template](./notebook.pdf). The **topic**, **cover image**, and **author name** can be customized.

## Installation

Clone the repository and install the requirements using `pip`:

```{sh}
pip install -r requirements.txt
```

## Create a notebook

To generate the template notebook with no customizations:

```{sh}
python build.py .
```

This will save the file `notebook.pdf` in the current directory.

To generate a notebook with customizations:

```{sh}
python build.py . -t "Going to Mars" -a "Elon Musk" -i "http://upload.wikimedia.org/some_image.png"
```

For more details, see `python build.py --help`.