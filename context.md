In property-map folder there is my project added, hosted currently
as cm-rentals.com
It basically reads a table from Supabase database and displays properties on the map, including dispaying their images - it's an app in Streamlit Framework

However, the issue is that I have uploaded only a few images to a Supabase, and for all the other properties I have used other links, like links from Facebook, and most of them have expired unfortunately, causing blank images on my website

But adding images on Supabase Storage is quite a mundane process, as one-by-one I have to:
- save the image locally
- upload it to Supabase using the UI, while choosing file name and also sharing the link with selected expire date (was going with 10 years now)
- copy generated URL to the SQL table, so it can be displayed in the app

So as I wanted to learn Panel a little bit, python framework to build web apps, I want you to create Panel app that will simplify the process a little bit for me:
- it will display the content of the main table (not all fields are required), and it will show whether the image is displayed correctly or not
- if image is not displayed correctly, the UI will allow an action to be taken, which is uploading a new image
- A new image should be added either through URL, or through direct file input (should accept only image extension like jpg, png, webp)
- And then the image will be uploaded to Supabase Storage using given property name, and the URL will be generated for 10 years
- And that URL will be added in the table, in proper image_url table


General context:
- For communication with Supabase, please use Supabase library and follow the same syntax as I did in my Database class (db.py file)
- For Supabase credentials we will use .env file (same as in original Streamlit project)
- Use venv
- Only read from property-map folder, do not change everything there
- Generate the app, so all the files, in supabase-img-linker-ui folder