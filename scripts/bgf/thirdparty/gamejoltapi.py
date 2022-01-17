from urllib.parse import urlencode as _urlencode, quote as _quote
from urllib.request import urlopen as _urlopen
from hashlib import md5 as _md5

from ast import literal_eval as _literal_eval
from collections import OrderedDict as _OrderedDict

_DEBUG = False

class GameJoltDataRequired(Exception):
    """ Exception raised when not all required data is provided in the request call.
    
    :param key: The data field name which is required.
    :type key: str
    """
    
    def __init__(self, key):
        self.key = key
        self.message = "Value is required, cannot be None: " + repr(key)
        super().__init__(self.message)

class GameJoltDataCollision(Exception):
    """ Exception raised when a value cannot be provided along with another.
    
    :param keys: The data field names which collided.
    :type keys: list
    """
    
    def __init__(self, keys):
        self.keys = keys
        self.message = "Values cannot be used together: " + ", ".join([repr(k) for k in self.keys])
        super().__init__(self.message)

class GameJoltAPI:
    """ The main Game Jolt API class. Aside from the required arguments, most of the 
    optional arguments are provided to avoid asking for them in every single method.
    
    :param gameId: The game ID. Required in all requests.
    :type gameId: int
    
    :param privateKey: The API private key. Required in all requests.
    :type privateKey: str
    
    :param username: Username used in some requests. Optional.
    :type username: str
    
    :param userToken: User access token used in some requests. Optional.
    :type userToken: str
    
    :param responseFormat: The response format of the requests. Can be ``"json"``, ``"xml"``, ``"keypair"`` or ``"dump"``. Optional, defaults to ``"json"``.
    :type responseFormat: str
    
    :param submitRequests: If submit the requests or just get the generated URLs from the method calls. Useful to generate URLs for batch requests. Optional, defaults to ``True``.
    :type submitRequests: bool
    
    .. py:attribute:: gameId
       :type: int
       
       The game ID. Required in all requests.
    
    .. py:attribute:: privateKey
       :type: str
       
        The API private key. Required in all requests.
    
    .. py:attribute:: username
       :type: str
       
        Username used in some requests. Optional.
    
    .. py:attribute:: userToken
       :type: str
       
        User access token used in some requests. Optional.
    
    .. py:attribute:: responseFormat
       :type: str
       
        The response format of the requests. Can be ``"json"``, ``"xml"``, ``"keypair"`` or ``"dump"``. Optional, defaults to ``"json"``.
    
    .. py:attribute:: submitRequests
       :type: bool
       
        If submit the requests or just get the generated URLs from the method calls. Useful to generate URLs for batch requests. Optional, defaults to ``True``."""
    
    def __init__(self, gameId, privateKey, username=None, userToken=None, responseFormat="json", submitRequests=True):
        self.__API_URL = "https://api.gamejolt.com/api/game/v1_2"
        self.__RETURN_FORMATS = ["json", "keypair", "dump", "xml"]
        
        self.gameId = str(gameId)
        self.privateKey = privateKey
        self.username = username
        self.userToken = userToken
        self.responseFormat = responseFormat if responseFormat in self.__RETURN_FORMATS else "json"
        self.submitRequests = submitRequests
        self.operations = {
            "users/fetch" : self.__API_URL + "/users/" + "?",
            "users/auth" : self.__API_URL + "/users/auth/" + "?",
            "sessions/open" : self.__API_URL + "/sessions/open/" + "?",
            "sessions/ping" : self.__API_URL + "/sessions/ping/" + "?",
            "sessions/check" : self.__API_URL + "/sessions/check/" + "?",
            "sessions/close" : self.__API_URL + "/sessions/close/" + "?",
            "scores/fetch" : self.__API_URL + "/scores/" + "?",
            "scores/tables" : self.__API_URL + "/scores/tables/" + "?",
            "scores/add" : self.__API_URL + "/scores/add/" + "?",
            "scores/get-rank" : self.__API_URL + "/scores/get-rank/" + "?",
            "trophies/fetch" : self.__API_URL + "/trophies/" + "?",
            "trophies/add-achieved" : self.__API_URL + "/trophies/add-achieved/" + "?",
            "trophies/remove-achieved" : self.__API_URL + "/trophies/remove-achieved/" + "?",
            "data-store/set" : self.__API_URL + "/data-store/set/" + "?",
            "data-store/update" : self.__API_URL + "/data-store/update/" + "?",
            "data-store/remove" : self.__API_URL + "/data-store/remove/" + "?",
            "data-store/fetch" : self.__API_URL + "/data-store/" + "?",
            "data-store/get-keys" : self.__API_URL + "/data-store/get-keys/" + "?",
            "friends" : self.__API_URL + "/friends/" + "?",
            "time" : self.__API_URL + "/time/" + "?",
            "batch" : self.__API_URL + "/batch/" + "?",
        }
        
    def _submit(self, operationUrl, data):
        orderedData = _OrderedDict()
        isBatch = "batch" in operationUrl
        
        if not self.submitRequests and "format" in data.keys():
            data.pop("format")
        
        for key in sorted(data.keys()):
            orderedData[key] = data[key]
        data = orderedData
        
        requestUrls = data.pop("requests") if isBatch else []
        requestAsParams = "&".join(["requests[]=" + url for url in requestUrls]) if isBatch else ""
            
        urlParams = _urlencode(data)
        urlParams += "&" + requestAsParams if isBatch else ""
        urlToSignature = operationUrl + urlParams + self.privateKey
        signature = _md5(urlToSignature.encode()).hexdigest()
        finalUrl = operationUrl + urlParams + "&signature=" + signature
        
        if self.submitRequests:
            if _DEBUG: print("Requesting URL:", finalUrl)
            response = _urlopen(finalUrl).read().decode()
            
            if self.responseFormat == "json":
                return _literal_eval(response)["response"]
            else:
                return response
        else:
            if _DEBUG: print("Generated URL:", finalUrl)
            return finalUrl

    def _validateRequiredData(self, data):
        for key in data.keys():
            if data[key] is None:
                raise GameJoltDataRequired(key)
        return True
        
    def _getValidData(self, data):
        validatedData = {}
        if self.responseFormat != "json":
            validatedData["format"] = self.responseFormat
        
        for key in data.keys():
            if data[key] is not None:
                validatedData[key] = data[key]
        return validatedData
    
    def _processBoolean(self, value):
        if value is not None:
            return str(value).lower()
    
    # Users
    def usersFetch(self, username=None, userId=None):
        """Returns a user's data.
        
        :param username: The username of the user whose data you'd like to fetch.
        :type username: str
        
        :param userId: The ID of the user whose data you'd like to fetch.
        :type userId: str, int or list
        
        .. note::
           
           - Only one parameter, ``username`` or ``userId``, is required.
           - You can pass in multiple user ids by providing a list or separating them with commas in a string (example: ``"13,89,35"``)."""
        
        if type(userId) in (list, tuple, set):
            userId = ",".join(userId)
        
        # Required data
        data = {
            "game_id" : self.gameId
        }
            
        if username is not None: 
            data["username"] = username
            
        elif userId is not None: 
            data["user_id"] = userId
        
        else:
            data["username"] = self.username
        
        self._validateRequiredData(data)
        return self._submit(self.operations["users/fetch"], data)
        
    def usersAuth(self):
        """Authenticates the user's information. This should be done before you make 
        any calls for the user, to make sure the user's credentials (username and 
        token) are valid."""
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "username" : self.username,
            "user_token" : self.userToken
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["users/auth"], data)
    
    # Sessions
    def sessionsOpen(self):
        """Opens a game session for a particular user and allows you to tell Game Jolt 
        that a user is playing your game. You must ping the session to keep it active 
        and you must close it when you're done with it.
        
        .. note::
           You can only have one open session for a user at a time. If you try to open a new session while one is running, the system will close out the current one before opening the new one.
        
        """
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "username" : self.username,
            "user_token" : self.userToken
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["sessions/open"], data)
        
    def sessionsPing(self, status=None):
        """Pings an open session to tell the system that it's still active. If the session 
        hasn't been pinged within 120 seconds, the system will close the session and you 
        will have to open another one. It's recommended that you ping about every 30 
        seconds or so to keep the system from clearing out your session.
        
        You can also let the system know whether the player is in an active or idle state 
        within your game.
        
        :param status: Sets the status of the session.
        :type status: str
        
        .. note::
           Valid Values for ``status``:
           
           - ``"active"``: Sets the session to the ``"active"`` state.
           - ``"idle"``: Sets the session to the ``"idle"`` state.
        """
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "username" : self.username,
            "user_token" : self.userToken
        }
        
        # Optional data
        optionalData = {
            "status" : status # active or idle
        }
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        return self._submit(self.operations["sessions/ping"], data)
    
    def sessionsCheck(self):
        """Checks to see if there is an open session for the user. Can be used to see 
        if a particular user account is active in the game.
        
        .. note::
           
           This endpoint returns ``"false"`` for the ``"success"`` field when no open session exists. That behaviour is different from other endpoints which use this field to indicate an error state.

        """
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "username" : self.username,
            "user_token" : self.userToken
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["sessions/check"], data)
        
    def sessionsClose(self):
        """Closes the active session."""
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "username" : self.username,
            "user_token" : self.userToken
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["sessions/close"], data)
        
    # Scores
    def scoresFetch(self, limit=None, tableId=None, guest=None, betterThan=None, worseThan=None, thisUser=False):
        """Returns a list of scores either for a user or globally for a game.
        
        :param limit: The number of scores you'd like to return.
        :type limit: int
        
        :param tableId: The ID of the score table.
        :type tableId: int
        
        :param guest: A guest's name.
        :type guest: str
        
        :param betterThan: Fetch only scores better than this score sort value.
        :type betterThan: int
        
        :param worseThan: Fetch only scores worse than this score sort value.
        :type worseThan: int
        
        :param thisUser: If ``True``, fetch only scores of current user. Else, fetch scores of all users.
        :type thisUser: bool
        
        .. note::
           
           - The default value for ``limit`` is ``10`` scores. The maximum amount of scores you can retrieve is ``100``.
           - If ``tableId`` is left blank, the scores from the primary score table will be returned.
           - Only pass in ``thisUser=True`` if you would like to retrieve scores for just the user set in the class constructor. Leave ``thisUser=False`` and ``guest=None`` to retrieve all scores.
           - ``guest`` allows you to fetch scores by a specific guest name. Only pass either the ``thisUser=True`` or the ``guest`` (or none), never both.
           - Scores are returned in the order of the score table's sorting direction. e.g. for descending tables the bigger scores are returned first.
        """
        
        # Required data
        data = {
            "game_id" : self.gameId
        }
        
        # Optional data
        optionalData = {
            "username" : self.username if guest is None and thisUser else None,
            "user_token" : self.userToken if guest is None and thisUser else None,
            "limit" : limit,
            "table_id" : tableId,
            "guest" : guest if guest is not None and not thisUser else None,
            "better_than" : betterThan,
            "worse_than" : worseThan,
        }
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["scores/fetch"], data)
        
    def scoresTables(self):
        """Returns a list of high score tables for a game."""
        
        # Required data
        data = {
            "game_id" : self.gameId
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["scores/tables"], data)
        
    def scoresAdd(self, score, sort, tableId=None, guest=None, extraData=None):
        """Adds a score for a user or guest. 
        
        :param score: This is a string value associated with the score. Example: ``"500 Points"``
        :type score: str
        
        :param sort: This is a numerical sorting value associated with the score. All sorting will be based on this number. Example: ``500``
        :type sort: int
        
        :param tableId: The ID of the score table to submit to.
        :type table_id: int
        
        :param guest: The guest's name. Overrides the ``username`` set in the constructor.
        :type guest: str
        
        :param extraData: If there's any extra data you would like to store as a string, you can use this variable.
        :type extra_data: str
        
        .. note::
           
           - You can either store a score for a user or a guest. If you're storing for a user, you must pass in the ``username`` and ``userToken`` parameters in the class constructor and leave ``guest`` as ``None``. If you're storing for a guest, you must pass in the ``guest`` parameter.
           - The ``extraData`` value is only retrievable through the API and your game's dashboard. It's never displayed publicly to users on the site. If there is other data associated with the score such as time played, coins collected, etc., you should definitely include it. It will be helpful in cases where you believe a gamer has illegitimately achieved a high score.
           - If ``tableId`` is left blank, the score will be submitted to the primary high score table.
        
        """
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "score" : score,
            "sort" : sort
        }
        
        # Optional data
        optionalData = {
            "username" : self.username if guest is None else None,
            "user_token" : self.userToken if guest is None else None,
            "table_id" : tableId,
            "guest" : guest if guest is not None else None,
            "extra_data" : extraData,
        }
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        return self._submit(self.operations["scores/add"], data)
        
    def scoresGetRank(self, sort, tableId=None):
        """Returns the rank of a particular score on a score table.
        
        :param sort: This is a numerical sorting value that is represented by a rank on the score table.
        :type sort: int
        
        :param tableId: The ID of the score table from which you want to get the rank.
        :type tableId: int
        
        .. note::
           
           - If ``tableId`` is left blank, the ranks from the primary high score table will be returned.
           - If the score is not represented by any rank on the score table, the request will return the rank that is closest to the requested score.
        """
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "sort" : sort
        }
        
        # Optional data
        optionalData = {
            "table_id" : tableId,
        }
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        return self._submit(self.operations["scores/get-rank"], data)
        
    # Trophies
    def trophiesFetch(self, achieved=None, trophyId=None):
        """Returns one trophy or multiple trophies, depending on the parameters passed in.
        
        :param achieved: Pass in ``True`` to return only the achieved trophies for a user. Pass in ``False`` to return only trophies the user hasn't achieved. Leave blank to retrieve all trophies.
        :type achieved: bool
        
        :param trophyId: If you would like to return just one trophy, you may pass the trophy ID with this parameter. If you do, only that trophy will be returned in the response. You may also pass multiple trophy IDs here if you want to return a subset of all the trophies. You do this as a list or a string with comma-separated values in the same way you would for retrieving multiple users (example: ``"13,89,35"``). Passing a ``trophyId`` will ignore the ``achieved`` parameter if it is passed.
        :type trophyId: str, int or list
        
        """
        
        if type(trophyId) in (list, tuple, set):
            trophyId = ",".join(trophyId)
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "username" : self.username,
            "user_token" : self.userToken
        }
        
        # Optional data
        optionalData = {
            "achieved" : self._processBoolean(achieved) if trophyId is None else None,
            "trophy_id" : trophyId
        }
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["trophies/fetch"], data)
        
    def trophiesAddAchieved(self, trophyId):
        """Sets a trophy as achieved for a particular user.
        
        :param trophyId: The ID of the trophy to add for the user.
        :type trophyId: int
        """
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "username" : self.username,
            "user_token" : self.userToken,
            "trophy_id" : trophyId
        }
        
        self._validateRequiredData(data)
        
        return self._submit(self.operations["trophies/add-achieved"], data)
        
    def trophiesRemoveAchieved(self, trophyId):
        """Remove a previously achieved trophy for a particular user.
        
        :param trophyId: The ID of the trophy to remove from the user.
        :type trophyId: int
        """
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "username" : self.username,
            "user_token" : self.userToken,
            "trophy_id" : trophyId
        }
        
        self._validateRequiredData(data)
        
        return self._submit(self.operations["trophies/remove-achieved"], data)
    
    # Data Storage
    def dataStoreSet(self, key, data, globalData=False):
        """Sets data in the data store.
        
        :param key: The key of the data item you'd like to set.
        :type key: str
        
        :param data: The data you'd like to set.
        :type data: str
        
        :param globalData: If set to `True`, ignores ``username`` and ``userToken`` set in constructor and processes global data instead of user data.
        :type globalData: bool
        
        .. note::
           
           You can create new data store items by passing in a key that doesn't yet exist in the data store.
        
        .. code-block:: python
           
           # Store on the key "some_global_value" the data "500" in the global data store
           result = api.dataStoreSet("some_global_value", "500", globalData=True)
           
        """
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "key" : key,
            "data" : data
        }
        
        # Optional data
        optionalData = {
            "username" : self.username,
            "user_token" : self.userToken
        }
        
        # Process global data instead of user data
        if globalData:
            optionalData["username"] = None
            optionalData["user_token"] = None
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["data-store/set"], data)
        
    def dataStoreUpdate(self, key, operation, value, globalData=False):
        """Updates data in the data store.
        
        :param key: The key of the data item you'd like to update.
        :type key: str
        
        :param operation: The operation you'd like to perform.
        :type operation: str
        
        :param value: The value you'd like to apply to the data store item. (See values below.)
        :type value: str
        
        :param globalData: If set to `True`, ignores ``username`` and ``userToken`` set in constructor and processes global data instead of user data.
        :type globalData: bool
        
        .. note::
        
           Valid Values for ``operation``:
           
           - ``"add"``: Adds the ``value`` to the current data store item.
           - ``"subtract"``: Substracts the ``value`` from the current data store item.
           - ``"multiply"``: Multiplies the ``value`` by the current data store item.
           - ``"divide"``: Divides the current data store item by the ``value``.
           - ``"append"``: Appends the ``value`` to the current data store item.
           - ``"prepend"``: Prepends the ``value`` to the current data store item.
        
        .. note::
        
           You can only perform mathematic operations on numerical data.
        
        .. code-block:: python
           
           # Adds "100" to "some_global_value" in the global data store
           result = api.dataStoreUpdate("some_global_value", "add", "100", globalData=True)
           
        """
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "key" : key,
            "operation" : operation,
            "value" : value
        }
        
        # Optional data
        optionalData = {
            "username" : self.username,
            "user_token" : self.userToken
        }
        
        # Process global data instead of user data
        if globalData:
            optionalData["username"] = None
            optionalData["user_token"] = None
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["data-store/update"], data)
        
    def dataStoreRemove(self, key, globalData=False):
        """Removes data from the data store.
        
        :param key: The key of the data item you'd like to remove.
        :type key: str
        
        :param globalData: If set to `True`, ignores ``username`` and ``userToken`` set in constructor and processes global data instead of user data.
        :type globalData: bool
        
        .. code-block:: python
           
           # Remove "some_global_value" from global data store
           result = api.dataStoreRemove("some_global_value", globalData=True)
           
        """
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "key" : key
        }
        
        # Optional data
        optionalData = {
            "username" : self.username,
            "user_token" : self.userToken
        }
        
        # Process global data instead of user data
        if globalData:
            optionalData["username"] = None
            optionalData["user_token"] = None
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["data-store/remove"], data)
        
    def dataStoreFetch(self, key, globalData=False):
        """Returns data from the data store.
        
        :param key: The key of the data item you'd like to fetch.
        :type key: str
        
        :param globalData: If set to `True`, ignores ``username`` and ``userToken`` set in constructor and processes global data instead of user data.
        :type globalData: bool
        
        .. code-block:: python
           
           # Get "some_global_value" from global data store
           result = api.dataStoreFetch("some_global_value", globalData=True)
           
        """
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "key" : key
        }
        
        # Optional data
        optionalData = {
            "username" : self.username,
            "user_token" : self.userToken
        }
        
        # Process global data instead of user data
        if globalData:
            optionalData["username"] = None
            optionalData["user_token"] = None
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["data-store/fetch"], data)
        
    def dataStoreGetKeys(self, pattern=None, globalData=False):
        """Returns either all the keys in the game's global data store, or all the keys in a user's data store.
        
        :param pattern: The pattern to apply to the key names in the data store.
        :type pattern: str
        
        :param globalData: If set to `True`, ignores ``username`` and ``userToken`` set in constructor and processes global data instead of user data.
        :type globalData: bool
        
        .. note::
           
           - If you apply a pattern to the request, only keys with applicable key names will be returned. The placeholder character for patterns is ``*``.
           - This request will return a list of the ``key`` values. The ``key`` return value can appear more than once.
        
        .. code-block:: python
           
           # Get keys from global data store starting with "some_global"
           result = api.dataStoreGetKeys("some_global_*", globalData=True)
           
        """
        
        # Required data
        data = {
            "game_id" : self.gameId
        }
        
        # Optional data
        optionalData = {
            "username" : self.username,
            "user_token" : self.userToken,
            "pattern" : pattern
        }
        
        # Process global data instead of user data
        if globalData:
            optionalData["username"] = None
            optionalData["user_token"] = None
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["data-store/get-keys"], data)
        
    # Friends
    def friends(self):
        """Returns the list of a user's friends."""
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "username" : self.username,
            "user_token" : self.userToken
        }
        
        self._validateRequiredData(data)
        
        return self._submit(self.operations["friends"], data)
    
    # Time
    def time(self):
        """Returns the time of the Game Jolt server."""
        
        # Required data
        data = {
            "game_id" : self.gameId
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["time"], data)
    
    # Batch Calls
    def batch(self, requests=[], parallel=None, breakOnError=None):
        """A batch request is a collection of sub-requests that enables developers to send multiple API calls with one HTTP request. 
        
        :param requests: An list of sub-request URLs. Each request will be executed and the responses of each one will be returned in the payload.
        :type requests: list of str
        
        :param parallel: By default, each sub-request is processed on the servers sequentially. If this is set to ``True``, then all sub-requests are processed at the same time, without waiting for the previous sub-request to finish before the next one is started.
        :type parallel: bool
        
        :param breakOnError: If this is set to ``True``, one sub-request failure will cause the entire batch to stop processing subsequent sub-requests and return a value of ``"false"`` for success.
        :type breakOnError: bool
        
        .. note::
           - The maximum amount of sub requests in one batch request is 50.
           - Dump format is not supported in batch calls.
           - The ``parallel`` and ``breakOnError`` parameters cannot be used in the same request.
        
        .. code-block:: python
           
           # Disable request submitting to get URLs from methods
           api.submitRequests = False
           
           # Generate list of request URLs
           requests = [
               api.usersFetch(),
               api.sessionsCheck(),
               api.scoresTables(),
               api.trophiesFetch(),
               api.dataStoreGetKeys("*", globalData=True),
               api.friends(),
               api.time()
           ]
           
           # Enable request submitting again
           api.submitRequests = True
           
           # Submit batch request and get all results
           result = api.batch(requests=requests)
        
        """
        
        if parallel is not None and breakOnError is not None:
            raise GameJoltDataCollision(["parallel", "break_on_error"])
        
        for i in range(len(requests)):
            requests[i] = requests[i].replace(self.__API_URL, "")
            requests[i] = requests[i].split("&signature=")[0]
            requests[i] += "&signature=" + _md5((requests[i] + self.privateKey).encode()).hexdigest()
            requests[i] = _quote(requests[i].replace(self.__API_URL, ""), safe="")
        
        # Required data
        data = {
            "game_id" : self.gameId,
            "requests" : requests if len(requests) > 0 else None
        }
        
        # Optional data
        optionalData = {
            "parallel" : self._processBoolean(parallel),
            "break_on_error" : self._processBoolean(breakOnError)
        }
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["batch"], data)

