
import hashlib
from magic import Magic
# pip install python-magic-bin==0.4.14
import datetime
from PySide6.QtWidgets import QTextEdit

class MetadataViewer:
    def __init__(self, parent=None):
        self.metadata_text_edit = QTextEdit(parent)
        self.metadata_text_edit.setReadOnly(True)


    def display_metadata(self, metadata, data, file_content):
        if not metadata:
            self.metadata_text_edit.setHtml("<b>No metadata available.</b>")
            return

        def format_epoch_time(epoch_time):
            try:
                # Check if the epoch_time is None or not a number
                if epoch_time is None or not isinstance(epoch_time, (int, float)):
                    return 'N/A'

                # Convert to datetime and format
                return datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                print(f"Error converting timestamp: {epoch_time}, Error: {e}")
                print(epoch_time)
                return 'Invalid Timestamp'

        # Generate hashes and determine MIME type
        md5_hash = hashlib.md5(file_content).hexdigest()
        sha256_hash = hashlib.sha256(file_content).hexdigest()
        mime_type = Magic().from_buffer(file_content)

        # Format times
        created_time = format_epoch_time(metadata.crtime)
        modified_time = format_epoch_time(metadata.mtime)
        accessed_time = format_epoch_time(metadata.atime)
        changed_time = format_epoch_time(metadata.ctime)

        extended_metadata = f"""
                    <style>
                        body {{
                            margin: 0;
                            padding: 0;
                            font-family: Arial, sans-serif;
                        }}
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
                        }}
                        td, th {{
                            border: 1px solid #ddd;
                            padding: 8px;
                            word-wrap: break-word;
                            text-align: left;
                        }}
                        th {{
                            background-color: #4CAF50;
                            color: white;
                        }}
                        tr:nth-child(even) {{
                            background-color: #f2f2f2;
                        }}
                        tr:hover {{
                            background-color: #ddd;
                        }}
                    </style>
                   <b>File Metadata:</b><br>
                    <table>
                        <tr><th>Attribute</th><th>Value</th></tr>
                        <tr><td>Name</td><td>{data.get('name', 'N/A')}</td></tr>
                        <tr><td>Inode Number</td><td>{data.get('inode_number', 'N/A')}</td></tr>
                        <tr><td>Size</td><td>{metadata.size if metadata.size else 'N/A'}</td></tr>
                        <tr><td>Created Time</td><td>{created_time}</td></tr>
                        <tr><td>Modified Time</td><td>{modified_time}</td></tr>
                        <tr><td>Accessed Time</td><td>{accessed_time}</td></tr>
                        <tr><td>Changed Time</td><td>{changed_time}</td></tr>
                        <tr><td>MIME Type</td><td>{mime_type}</td></tr>
                        <tr><td>MD5 Hash</td><td>{md5_hash}</td></tr>
                        <tr><td>SHA-256 Hash</td><td>{sha256_hash}</td></tr>
                    </table>
               """

        self.metadata_text_edit.setHtml(extended_metadata)

    def get_widget(self):
        return self.metadata_text_edit

    def clear(self):
        self.metadata_text_edit.clear()
