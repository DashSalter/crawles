from typing import Text, Union, Dict

from .Response import Response


def get(url: Text,
        params=Union[Dict, Text],
        headers=Union[Dict, Text],
        **kwargs) -> Response: ...


def post(url: Text,
         data=Union[Dict, Text],
         headers=Union[Dict, Text],
         **kwargs) -> Response: ...


def session_get(url: Text,
                params=Union[Dict, Text],
                headers=Union[Dict, Text],
                **kwargs) -> Response: ...


def session_post(url: Text,
                 data=Union[Dict, Text],
                 headers=Union[Dict, Text],
                 **kwargs) -> Response: ...
