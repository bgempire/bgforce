from . import cache, DEBUG


class Request:
    
    def __init__(self, url, returnType="bytes", submit=True, callback=None, callbackArgs=[]):
        # type: (str, str, bool, object, list) -> None
        
        self.url = url
        self.returnType = returnType
        self.status = "pending"
        self.data = None
        self._thread = None
        self._callback = callback
        self._callbackArgs = callbackArgs
        
        if submit:
            self.submit()
    
    
    def __eq__(self, obj):
        # type: (object) -> bool
        
        if type(obj) == str and self.url == obj \
        or type(obj) == Request and self.url == obj.url:
            return True
        else:
            return False
    
    
    def __repr__(self):
        return "Request(" + repr(self.url) + ", returnType=" + repr(self.returnType) + ", status=" + repr(self.status) + ")"
    
    
    def submit(self):
        from threading import Thread
        
        if DEBUG: print("> Submiting request:", self)
        self._thread = Thread(target=self._submit, daemon=True)
        self._thread.start()
    
    
    def _submit(self):
        
        try:
            from urllib.request import urlopen
            
            # Fetch data from URL
            data = urlopen(self.url).read()
            
            returnType = str(self.returnType).lower()
            
            # Process data according to return type
            if returnType == "text":
                self.data = data.decode()
            
            elif returnType == "json":
                from json import loads
                
                data = [l.strip() for l in data.decode().split("\n") if not l.strip().startswith("//")]
                self.data = loads("\n".join(data))
                
            else:
                self.data = data
            
            if DEBUG and returnType != "bytes":
                print("> Return type:", returnType)
                print(self.data)
                
            self.status = "success"
            
        except Exception as e:
            self.status = "error"
            if DEBUG: print(e)
            
        # Run callback function if provided
        if self._callback:
            self._callback([self] + list(self._callbackArgs))
            
        if DEBUG: print("> Request result:", self.status, "\n")

