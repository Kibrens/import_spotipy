# Define the root directory where your artist folders are located
$rootDirectory = "C:\Users\cabra\OneDrive\Music"

# Define the path of the output text file for this new list
$outputFile = "C:\Users\cabra\OneDrive\Music\output_artists.txt"

# Get all artist folders (subdirectories) in the root directory
$artistFolders = Get-ChildItem -Path $rootDirectory -Directory

# Loop through each artist folder
foreach ($artist in $artistFolders) {
    # Get all album folders inside the artist folder
    $albumFolders = Get-ChildItem -Path $artist.FullName -Directory
    
	# Loop through each album folder
    foreach ($album in $albumFolders) {
        # Get all .mp3 files inside the album folder and its subfolders
        $mp3Files = Get-ChildItem -Path $album.FullName -Filter *.mp3 -Recurse
        
        # Check if there are any .mp3 files in the album folder or its subfolders
        if ($mp3Files) {
            # Extract the names without extensions and add them to the output file
            $mp3Files.Name | ForEach-Object { $_.Replace(".mp3", "") } | Out-File -FilePath $outputFile -Append -Force
        }
    }
}
