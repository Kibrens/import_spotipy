# Define the directory to search for .mp3 files
$directory = "C:\Users\cabra\OneDrive\Music"

# Define the path of the output text file
$outputFile = "C:\Users\cabra\OneDrive\Music\output.txt"

# Get all .mp3 files in the specified directory
$mp3Files = Get-ChildItem -Path $directory -Filter *.mp3

# Extract the file names without the extension and save them to the output file
$mp3Files.Name | ForEach-Object { $_.Replace(".mp3", "") } | Out-File -FilePath $outputFile -Force
