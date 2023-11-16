# This is a helper class for file
import json

class FileObject:
    def __init__(self, file_path, action, buffer):
        self._file_path = file_path
        self._action = action
        self._buffer = buffer
        self._username = None
        self._password = None
    
    def to_json(self):
        return json.dumps({
            'file_path': self._file_path,
            'action': self._action,
            'buffer': self._buffer,
            'username': self._username,
            'password': self._password
        })
    
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data['file_path'],data['action'],data['buffer'])
    
    @property
    def file_path(self):
        return self._file_path
    
    @file_path.setter
    def file_path(self,value):
        self._file_path = value
    
    @property
    def action(self):
        return self._action
    
    @action.setter
    def action(self, value):
        self._action = value

    @property
    def buffer(self):
        return self._buffer
    
    @buffer.setter
    def buffer(self,value):
        self._buffer = value
    
    def set_login_info(self,username,password):
        self._username = username
        self._password = password
    