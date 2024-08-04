import json
import os
import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def drive_login():
    """Log in to Google Drive using stored credentials.

    Returns:
        pydrive2.drive.GoogleDrive: An authenticated Google Drive instance.
    """
    directorio_credenciales = 'credentials_module.json'
    
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credenciales)
    else:
        gauth.Authorize()

    return GoogleDrive(gauth)

def upload_to_drive(file_path, folder_id):
    """Uploads a file to Google Drive, updating it if it already exists.

    Args:
        file_path (str): The local file path of the file to upload.
        folder_id (str): The ID of the Google Drive folder to upload the file to.
    """

    credenciales = drive_login()
    file_list = credenciales.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    
    # Check if the file already exists in Google Drive
    for file in file_list:
        if file['title'] == os.path.basename(file_path):
            existing_file = credenciales.CreateFile({'id': file['id']})
            existing_file.SetContentFile(file_path)
            existing_file.Upload()
            print(f"File '{file_path}' updated on Google Drive.")
            return
    
    # If the file doesn't exist, upload it as a new file
    new_file = credenciales.CreateFile({'parents': [{'kind': 'drive#fileLink', 'id': folder_id}]})
    new_file['title'] = os.path.basename(file_path)
    new_file.SetContentFile(file_path)
    new_file.Upload()
    print(f"File '{file_path}' uploaded as a new file on Google Drive.")

def delete_file(file_path):
    """Delete a file from the local disk.

    Args:
        file_path (str): The local file path of the file to delete.
    """
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except PermissionError:
        print(f"No permission to delete file '{file_path}'.")

def drive_list_files(folder_id): 
    """Lists files in a specified Google Drive folder.

    Args:
        folder_id (str): The ID of the Google Drive folder to list files from.

    Returns:
        list: A list of file metadata dictionaries for files in the specified folder.
    """

    # Authenticates to Google Drive and retrieves the file list from the specified folder
    credenciales = drive_login()
    file_list = credenciales.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    return file_list

def download_from_drive(file_id, file_name):
    """Downloads a file from Google Drive.

    Args:
        file_id (str): The ID of the file to download from Google Drive.
        file_name (str): The name of the file to save locally.

    Returns:
        str: The local file path of the downloaded file.
    """

    # Authenticates to Google Drive and downloads the specified file
    credenciales = drive_login()
    file_path = os.path.join(os.getcwd(), file_name)
    file_obj = credenciales.CreateFile({'id': file_id})
    file_obj.GetContentFile(file_name)
    return file_path

def check_existing_file(folder_id, existing_file_name, new_data, data_format):
    """Checks if a file exists in a specified Google Drive folder and appends or uploads new data accordingly.

    Args:
        folder_id (str): The ID of the Google Drive folder to check for the existing file.
        existing_file_name (str): The name of the existing file to check for.
        new_data (DataFrame or dict): The new data to append or upload.
        data_format (str): The format of the data ('csv' or 'json').

    Raises:
        ValueError: If the data_format is not 'csv' or 'json'.
    """
    
    file_id = None
    existing_files = drive_list_files(folder_id)
    
    for file in existing_files:
        if file['title'] == existing_file_name:
            file_id = file['id']
            break

    if file_id:
        file_path = download_from_drive(file_id, existing_file_name)
        if data_format == 'csv':
            existing_data = pd.read_csv(file_path)
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
            combined_data.to_csv(file_path, index=False)
        elif data_format == 'json':
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
            existing_data['data'].extend(new_data['data'])
            with open(file_path, 'w') as f:
                json.dump(existing_data, f)
        
        upload_to_drive(file_path, folder_id)
        print("New data has been appended to the existing file on Google Drive.")
        delete_file(file_path)
    else:
        file_path = existing_file_name
        if data_format == 'csv':
            new_data.to_csv(file_path, index=False)
        elif data_format == 'json':
            with open(file_path, 'w') as f:
                json.dump(new_data, f)
        
        upload_to_drive(file_path, folder_id)
        print("Data has been uploaded as a new file on Google Drive.")

