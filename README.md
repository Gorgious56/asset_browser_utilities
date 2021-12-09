When dealing with hundreds of library files it becomes tedious to mark their contents as assets.

Using python to automate the process is a perfect fit for such task.

However marking objects as assets using python doesn't automatically generate their previews like using the interface does.

This aims to mark all objects as assets and generate the preview of all files in the folder the user selects.

It might bug out if the file contains hundreds of objects. It is recommended to keep a low number of objects per file.

Go to File > Import > Batch Generate Previews

![image](https://user-images.githubusercontent.com/25156105/145441833-549197a3-848d-4ea7-acc4-8f570075c27e.png)

In the file selector, navigate to the folder where the blend files are located. Validate.

Count ~ 2 seconds per file to generate their assets and previews.
It's a good idea to enable the console with Window > Toggle System Console beforehand so you can see how many files you have marked yet.

Example Result :

![image](https://user-images.githubusercontent.com/25156105/145268274-c65c2c7d-3378-48cf-980c-ce7ef79a566f.png)
