import os
import re
import requests

def retrieve_image_urls():
    # Get the current working directory
    current_directory = os.getcwd()

    # Walk through the current directory and its subdirectories
    for root, dirs, files in os.walk(current_directory):
        # Iterate through all files in the current directory
        for file in files:
            # Check if the file has a ".md" extension
            if file.endswith(".md"):
                # Get the full path of the markdown file
                file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, "new_md.md")

                # Open the markdown file in read mode
                with open(new_file_path, "w") as fw:
                    with open(file_path, "r") as f:
                        # Read the contents of the file
                        file_contents = f.readlines()

                        # Use regex to find image URLs
                        base_pattern = r'^\!\[.*\]\((.*\.(png|jpg|jpeg|gif|bmp|svg))\?.*\)$'
                        regex_pattern = r'^\!\[.*\]\((.*\.(png|jpg|jpeg|gif|bmp|svg)\?.*)\)$'

                        # Create a new folder to save the images
                        images_folder_name = "images"
                        images_folder = os.path.join(root, images_folder_name)
                        if not os.path.exists(images_folder):
                            os.makedirs(images_folder)

                        for line in file_contents:
                            if re.search(regex_pattern, line):
                                base_url = re.search(base_pattern, line).group(1)
                                url = re.search(regex_pattern, line).group(1)
                                url = re.sub(r"blend64=.*?&", "", url)
                                image_filename = os.path.basename(base_url)
                                image_path = os.path.join(images_folder, image_filename)

                                response = requests.get(url)
                                with open(image_path, "wb") as img_file:
                                    img_file.write(response.content)

                                caption = re.search(r"^!\[(.*)\]\(.*\)$", line).group(1)
                                fw.write(f"![{caption}](/{images_folder_name}/{image_filename})")

                                print(f"Image downloaded: {image_filename}")
                            else:
                                fw.write(line)

# Test the function
retrieve_image_urls()