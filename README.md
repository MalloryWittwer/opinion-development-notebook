# Opinion Development Notebook

Create printable notebooks in booklet format to yelp you keep track and develop informed opinions about the world.

The notebooks are generated from this [template]().

**Customizations:**

- Topic
- Cover image
- Name

## Installation

Using `pip`:

```{sh}
pip install -r requirements.txt
```

## Create a new notebook

Run the python script:

```{sh}
python build.py . -t "Going to Mars" -a "Elon Musk" -i "http://upload.wikimedia.org/some_image.png"
```

This will save `booklet.pdf`