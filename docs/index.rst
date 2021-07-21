.. TelegraphAPI documentation master file, created by
   sphinx-quickstart on Mon Jul 19 10:05:41 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Index Page
============

Installation
----------------

.. code-block:: shell-session

   $ pip install telegraph_api

Example Usage
----------------

.. code-block:: python

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


.. toctree::
   :maxdepth: 4
   :caption: Contents:

   api
   models




