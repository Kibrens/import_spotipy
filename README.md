As a prerequisite you'll need to install spotipy

Open CMD and run:
pip install spotipy

You will also need Developer access to your account
https://developer.spotify.com/dashboard/applications
Setup an aplication using the callback URL provided in the .py file. They have to match

To create your playlist in spotify
Step 1:
  Create a txt file with all the songs you want to "import" to Spotify
Step 2:
  Run the Python script making sure you change the path to your list file so the script can access it
Step 3:
  Open Spotify and make sure your playlist and files are there :)


It helps greatly to have a sanitized library to begin with. The script will query spotify's database for those songs so having ${artist} - ${songname} is a good way to start
