# ✏️ Opinion Development Notebook

Create printable notebooks in booklet format to help you develop informed opinions about the world.

The notebooks are generated from this [template](./notebook.pdf). The **topic**, **cover image**, and **author name** can be customized.

## Installation

Clone this repository and install the requirements:

```{sh}
pip install -r requirements.txt
```

## Create a notebook

### Option 1: Via a Python script

To generate the template notebook with no customizations:

```{sh}
python build.py .
```

This will save the file `notebook.pdf` in the current directory.

To generate a notebook with a custom author, title, and cover image:

```{sh}
python build.py . --topic "Pipe-weed" --author "Bilbo Baggins" --image-url "https://static.wikia.nocookie.net/lotr/images/d/d9/Longbottom_leaves.JPG"
```

For more details, see `python build.py --help`.

### Option 2: Via the web app

Start the web app:

```
uvicorn main:app
```

Open http://localhost:8000 in your browser to see the web app.

## Print a notebook in booklet format

**On Linux**

You can use `pdfbook2` (`sudo apt-get install texlive-extra-utils`) to convert the notebook into booklet format:

```{sh}
pdfbook2 notebook.pdf
```

This will output a new file `notebook-book.pdf` in booklet format.

**On Windows / MacOs**

You can let the printer handle the booklet layout directly. In Adobe Acrobat Reader, choose "Booklet" in the print settings.