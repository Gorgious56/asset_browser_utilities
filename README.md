When dealing with hundreds of library files it becomes tedious to mark their contents as assets.

Using python to automate the process is a perfect fit for such task.

However marking objects as assets using python doesn't automatically generate their previews like using the interface does.

This aims to mark all objects as assets and generate the preview of all files in the folder the user selects.

1. Go to File > Import > Batch Generate Previews

![image](https://user-images.githubusercontent.com/25156105/145441833-549197a3-848d-4ea7-acc4-8f570075c27e.png)

2. In the file selector, navigate to the folder where the blend files are located. 

On the right hand side you have a few options :

- Recursively search in subfolders (and sub-sub folders, etc.) of the selected folder
- Prevent creation of file.blend1 backup file when saving library file
- Prevent overwriting items that have already been marked as assets
- Unmark assets instead of marking items
- Generate previews (Unchecking simply marks objects as assets without generating a preview, which is way faster)
- And a few toggles to choose which data types you want to mark as assets


![image](https://user-images.githubusercontent.com/25156105/147601200-6c676a3e-8736-4aa8-983f-9dee73af01ce.png)


3. Validate by clicking on the Blue button.

Count ~ 1 second per asset to generate their assets and previews. It should be quasi-instantaneous if you uncheck the setting to generate previews.

It's a good idea to enable the console with Window > Toggle System Console beforehand so you can see how many files you have marked yet.

Example Result :

![image](https://user-images.githubusercontent.com/25156105/145268274-c65c2c7d-3378-48cf-980c-ce7ef79a566f.png)
