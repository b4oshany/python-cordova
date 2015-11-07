===============================================
python-cordova
===============================================

This is a very simple Python library to interface with the Cordova (Phonegap) command line tool.


Key concepts
===============================================
- Interact with the Cordova CLI directly from Python
- Enables building and archiving PhoneGap applications from your Python code
- Interact with Jarsigner and Zipalign to sign and verify android apks.


***Note:***
This uses Google's methodology of
[manually signing apks](http://developer.android.com/tools/publishing/app-signing.html#signing-manually)
using [Jarsigner] and [Zipalign] to verify and sign apks.


Usage
===============================================

.. code-block:: python
   import cordova

   application = cordova.App(
       'PhoneGap Application',
       APPLICATION_ROOT
   )

   # Build a debug version for any platform application.
   application.build('android') # or any installed platform
   application.archive('ios') # or any installed platform

   # Build a relase version for any platform application
   application.build('android', release=True) # or any installed platform
   application.build('ios', release=True) # or any installed platform

   # Signing Android application (apk)
   application.sign_android_apk(keystore="/path/to/keystore", keypass="passcode", storepass="passcode")



Requirements
============

* [NodeJs]
* [NPM]
* [Jarsigner]
* [Zipalign]
* [Cordova]


[NodeJs]: https://nodejs.org/en/
[NPM]: https://www.npmjs.com/
[Jarsigner]: http://docs.oracle.com/javase/6/docs/technotes/tools/windows/jarsigner.html
[Zipalign]: http://developer.android.com/tools/help/zipalign.html
[Cordova]: https://cordova.apache.org/
