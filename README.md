This add-on aims to provide several utilities to reduce the time it takes to do operations on large libraries :

Available tools :


___ _Batch Mark (or Unmark) Objects as Assets_ ___
___ _Export Assets_ ___
___ _Batch Add or Remove tags_ ___ (new in V0.0.7)


___ _Batch Mark (or Unmark) Objects as Assets_ ___

Mark Objects as assets and generate the preview of all assets in the folder the user selects.

1. Go to the Asset Browser Editor and look for the add-on menu in the header

![image](https://user-images.githubusercontent.com/25156105/148301139-7daf3546-229d-4fb1-872b-e2f1d6617f37.png)

2. 
 - If you choose an external library : In the file selector, navigate to the folder where the blend files are located. 
 - If you choose to mark assets in the current file : Change the parameters in the popup window

On the right hand side you have a few options :

- Recursively search in subfolders (and sub-sub folders, etc.) of the selected folder
- Prevent creation of file.blend1 backup file when saving library file
- Prevent overwriting items that have already been marked as assets
- Generate previews (Unchecking simply marks objects as assets without generating a preview, which is way faster)
- Filter by Item Type(s)
- Filter by name, using a prefix, suffix or simply checking if the name contains specified text

![image](https://user-images.githubusercontent.com/25156105/148301410-34eee9cc-e0dd-468e-b31d-48c3704b1539.png)

3. Validate by clicking on the Blue button.

the whole process should be really fast, but one has to wait a little bit for heavier object previews to generate.

It's a good idea to enable the console with Window > Toggle System Console beforehand so you can see how many files you have marked yet.

Example Result :

![image](https://user-images.githubusercontent.com/25156105/145268274-c65c2c7d-3378-48cf-980c-ce7ef79a566f.png)


___ _Export Assets_ ___
 
 Export assets from the current file.
 
 ![image](https://user-images.githubusercontent.com/25156105/148301735-4ddb73d1-d73b-4396-9bb5-d0cd293c77d4.png)
 
All filters are additive.
- Filter by selection (export only selected objects)
- Filter by Item Type(s)
- Filter by name, using a prefix, suffix or simply checking if the name contains specified text

You can choose an existing file to append the assets to, or a new filepath will create a brand new file with the assets.


___ _Batch Add or Remove tags_ ___ (new in V0.0.7)

Batch add or remove tags from assets in current file or external library. You can filter assets like the other tools. Up to 10 tags can be added or removed at a time :

![image](https://user-images.githubusercontent.com/25156105/148535455-bedbfb62-9767-473c-95cc-c27a2b88ed63.png)
