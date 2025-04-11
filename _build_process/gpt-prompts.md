I have a site being built by astro.
It generarates static html pages.
The images used in the html are drawn from a database of images. In dev mode, I do not pay attention to the size of the image, allowing my flexibility of resizing for visual presentaiton with ust the height and width properties. This means that the image used in dev mode, and when the site is actually built is always high resplution and too large for actual use in final production deployment.

I have a python script that I run after I have run "npm build" this script parses all the html files and find the images. It uses the height and width properties, or some other way to determine the optimcaldimenstion to resize the oritingal image to. The script will

1. Resize images diemantions as needed
2. optimize for image quality to be acceptible on the web at best byte size.

The images are not always straight forward <img> tags with height and width.
Some images only the width is important.
some images only the height is important.
Some images widh is defined by css, not an img property
Some images can be large enough that the same image can be used as thumbnail and full sized in a modal popup. For example, a 500px wide image forced into a 250px thumbnail, using the same 500px file is acceptble so long as the 500px image is oprimized for web.

I need the best way to

1. Extract the images src links from the html files
2. Determins the required sizes
3. Optimize and save the files
4. make sure that the <img src> property points to the correct optimized file

I will be asking questions based on that. This is just background information. I am not asking you to generate code after this prompt.

For this conversation, do not provide code unless I ask for it. If I am asking a clarification question, answer that only.

If I ask for partial code, make sure to be clear WHERE to put them in relation to the rest of the code.

If I ask for full code, gove me the entire file with the changes clearly marked.
For example:

[existing code:]

# Change 1

[some new code]
[existing code:]

# Change 2

[some new code]

Then in the explenation explain
"At Change 1 we did...."

#########

First, I have an initial script that goes throug hthe build in /dist/ and find all the links to images that need to be moved from their original location on my local computers photo library, to the /dist/ directory which will eventually be pushed to production server.

This is only

1. Finding image referecens
2. copying the file from libarry to dist/ build
3. changing the absolute links in the files from pointing to the external source to become relative to the build

It does not yet resize images. THe resizing is done in a separate step
However, I am fine to combine it if it makes more sense, and resize the images as they are moved.
I am doing it in steps not to break it up and easier to debug.
Here is the moving script.
I do not need any code generated yet. This is for reference.

#####

Here is my resizing script.
This is not working prefectly.
Due to my html, and lack of standard formats I think, There are issues that some images get missed, such as the sliders
Some are getting resized to the wrong size.
Some should be made into multiple sizes, etc.

This is for your reference. I am not asking for code yet.

###

1. Currently it is renaming the file to have {filename}-{newsize} and updating the html

I think that this is not needed, because by the time I am building, I do not need as much flexibility and the layout will not change, I can resize it to exactly the size I need.

Therefore, does it make sense to
A) Resize at the same time as I copy
OR

B) Or, copy file to "{filename}-master.jpg/png"
and, as I copy, generate a json list of the files, with the width and/or height it will be resized to.

then, run the resize script to use the file list as the basis for resizing.
It will resize {filename}-master to the target file name
This way, I can make minor tweeks to the master list to change individual file sizes, without having to rebuild and rerun the scripts each time I amke a change.

This will also mean that the src names in the actual html should not need to be touched, since the large file will not be called "master" and that will always be available and remaned to whatever the html already looks for. Removing need to edit the html

I am not asking for code yet, just thoughts and reference

#####

For the html, I am currently looking in each element to find the target files size, but some are sized using css. How to handle that?

I can put an extra data-target-size["300"] or something in the tag
or

<!-- filename width 300 -->

comment near it in the build.

But doing this seems like it might be easier to

A) Make the resize script in a way that I can easily add edge cases as they become apparent to have them resized on a case by caase

- Add theedge cases to thescript? Or have a separate file with edge cases that is read intot hte script?

B) this is where the json would come in handy, because I can instead just adjust the dimentions in the json without worrying about edge cases

#####

I think I will go with B.

I will give my thoughts. Please tell me the pros and cons and if there is a better way.

I will adjust the step1_collect.py

1. to clollect the images into the same file structure.
2. name the copied image as {name}-master.{ext}
3. Remove the absolute urls, making them all relative

Questions:

Where do I

- change the html to normalize the file names to remove spaces etc?

If I am normallizing the names, it means I will be rewriting the html anyway. so do I keep that in the json? the -master name, and the normallized name, so that it will be easier to do search replace when I resize?

#######

Regarding additional complexity

"Additional Complexity:

You’re introducing an extra file (the JSON) that must be generated and maintained. This extra dependency requires you to be careful that the JSON and the HTML remain synchronized."

I the json will be generated every time freshly when I run the script, so no special additonal complexity.

If there are places where I want to make custom changes, I will do it in a separate file for those individual iages that is not overwritten each time the script is run, that way when the script is run again, my changes will persist between runs, and when resizeing, my static file will take presidnce

####

Ok, I want to break it down into steps.
I will make a script for each step to keep it clear in my head, but with flexibility that once I am more comfortable I can combine the scripts.

The first step is just to copy the images from library to curent dist
rename images as "-master"
normalize names and remove absolute
generate json - or just a list of images.

Should I include the part that checks the image sizes in this step? was I buld the json, or for now, just get a list of images which I can then go over in step 2 to get the initial sizes?

Here is my old file
[code]

####

OK, adjust this to make it collect the images and make a list of them.
At this point, the list is not json, just a list of one path / line.

Should I rename the file to -master now? or wait until I resize. If I rename now, I will not be able to look at the build to make sure that all images have been captured. If I keep them as the same file name as the html src tags ask for, I can still view it in a django dev server and it iwll look correct even thoguh the images are still large.

Then, when I do the resize, I will generate a -master for each one.?
