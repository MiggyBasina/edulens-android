import os
from kivy.utils import platform

class MobileFilePicker:
    @staticmethod
    def pick_csv_file(callback):
        """Pick CSV file - platform-specific"""
        if platform == 'android':
            # Android file picker
            from android.storage import primary_external_storage_path
            from android import mActivity
            from jnius import autoclass
            
            # Use Android Intent
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            
            intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.setType("*/*")
            intent.addCategory(Intent.CATEGORY_OPENABLE)
            
            # Start activity
            mActivity.startActivityForResult(intent, 1)
            
        else:
            # Desktop fallback
            from tkinter import filedialog
            import tkinter as tk
            
            root = tk.Tk()
            root.withdraw()
            
            file_path = filedialog.askopenfilename(
                title="Select CSV file",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            root.destroy()
            
            if file_path and callback:
                callback(file_path)