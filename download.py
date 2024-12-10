import os
import requests
import zipfile
from io import BytesIO

# Function to download a ZIP file from Jenkins
def download_artifact(jenkins_url, job_name, build_number, artifact_path, output_dir):
    # Jenkins API URL to get the artifact
    artifact_url = f"{jenkins_url}/job/{job_name}/{build_number}/artifact/{artifact_path}"
    
    # Send a GET request to Jenkins to fetch the artifact
    response = requests.get(artifact_url, stream=True)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the filename from the URL (or set a default name)
        artifact_name = artifact_path.split('/')[-1]
        zip_path = os.path.join(output_dir, artifact_name)
        
        # Write the content of the ZIP file to disk
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Artifact downloaded successfully to {zip_path}")
        return zip_path
    else:
        print(f"Failed to download artifact. HTTP Status code: {response.status_code}")
        return None

# Function to unzip the downloaded artifact
def unzip_artifact(zip_path, extract_to_dir):
    if zip_path and os.path.exists(zip_path):
        try:
            # Open the ZIP file and extract its contents
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_dir)
                print(f"Artifact extracted to {extract_to_dir}")
        except zipfile.BadZipFile:
            print("Error: The downloaded file is not a valid ZIP file.")
    else:
        print(f"Error: ZIP file does not exist at {zip_path}")

if __name__ == "__main__":
    # Configuration
    jenkins_url = "http://your-jenkins-server"  # Your Jenkins server URL
    job_name = "your-job-name"  # Jenkins job name
    build_number = "your-build-number"  # Build number (e.g., 42)
    artifact_path = "path/to/your/artifact.zip"  # Path to your artifact
    output_dir = "./downloaded_artifacts"  # Directory where the ZIP will be saved
    extract_to_dir = "./extracted"  # Directory to unzip the artifact into

    # Ensure output directories exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(extract_to_dir, exist_ok=True)

    # Download the artifact
    zip_path = download_artifact(jenkins_url, job_name, build_number, artifact_path, output_dir)
    
    # Unzip the artifact
    unzip_artifact(zip_path, extract_to_dir)
