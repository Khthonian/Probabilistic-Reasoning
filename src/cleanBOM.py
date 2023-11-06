def cleanBOM(filePath):
    """
    A function to remove Byte Order Mark (BOM) in-place from a file.

    Parameters:
    - filePath (str): The path to the dataset.
    """

    # Open the file for reading and read from the beginning
    with open(filePath, 'r+b') as file:
        content = file.read()

        # Decode the content
        content_str = content.decode('utf-8-sig')

        # Encode the content back to bytes and write back to file
        file.seek(0)
        file.write(content_str.encode('utf-8'))
        file.truncate()
