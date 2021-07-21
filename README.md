# TelegraphAPI

Asynchronus Python wrapper for telgra.ph [API](https://telegra.ph/api)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install telegraph_api.

```bash
pip install telegraph_api
```

## Documentation

You can read documentation of this package on [readthedocs]()

Documentation of original REST api can be found on [telegra.ph](https://telegra.ph/api) site

## Features
- Asynchronus 
- HTML2Nodes convertation
- File uploading
- Built with Pydantic
- Documentation is provided
## Usage

```python
# Importing required package
from telegraph_api import Telegraph
import asyncio


# Declaring asynchronous function for using await
async def main():
    # Creating new Telegraph object
    telegraph = Telegraph()
    # Creating new account
    await telegraph.create_account("My Favourite Blog", author_name="Ivan")
    # Creating new page
    new_page = await telegraph.create_page(
        "My first Telegraph Post",
        content_html="<p>Hello world!</p>" # Html content can be presented      
    )
    # Printing page url into console
    print(new_page.url)


# Running asynchronous function
asyncio.run(main())
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

I choosed [MIT](https://choosealicense.com/licenses/mit/) license
