# GAE XirSys

This is an example on how to use the XirSys api and make it go through an app engine backend.  
The purpose of this is to secure the secret key and ident.

How to setup:
- download the [app engine python SDK](https://cloud.google.com/appengine/docs/python/download)
- follow the steps there and install the SDK, you can either isntall the gcloud command or only the pythond sdk, more details [here](https://cloud.google.com/appengine/docs/python/quickstart)
- download this repo
- add you API keys into `app.yaml`
- cd into `/gae-xirsys` and run
```
[PATH_TO_APP_ENGINE_SDK]/dev_appserver.py ./app.yaml
```

The app doesn't do anything it just uses SimpleWebRTC to connect through the app engine server to Xirsys.  
Check the browser console for details.

In the future some examples will be added.

## Licensing

* See [LICENSE](./LICENSE)