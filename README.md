# ✏️ Opinion Development Notebook

Create printable notebooks in booklet format to help you develop informed opinions about the world.

The notebooks are generated from this [template](./notebook.pdf). The **topic**, **cover image**, and **author name** can be customized.

## Installation

Clone this repository and install the requirements:

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
python build.py . --topic "Pipe-weed" --author "Bilbo Baggins" --image-url "https://static.wikia.nocookie.net/lotr/images/d/d9/Longbottom_leaves.JPG"
```

For more details, see `python build.py --help`.