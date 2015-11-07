# -*- coding: utf-8 -*-
from __future__ import absolute_import
__version__ = '0.1'

import os
import re
import subprocess
from datetime import datetime

from .decorators import for_all_methods, chdir_context


BUILD_LOCATION = {
    'android': {
        'debug': 'platforms/android/build/outputs/apk/%s-debug.apk',
        'release': ('platforms/android/build/'
                    'outputs/apk/%s-release-unsigned.apk'),
        'archive': 'platforms/%s-android.zip',
        'signed': 'platforms/android/build/outputs/apk/%s-%s.apk'
    },
    'ios': {
        'debug': 'platforms/ios/build/emulator/%s.app',
        'release': 'platforms/ios/build/emulator/%s.app',
        'archive': 'platforms/%s-ios.zip'
    }
}


@for_all_methods(chdir_context)
class App(object):
    path = None
    name = None
    debug = False

    # We need to initialize the application with the path of the root
    # of the project
    def __init__(self, path, name, debug=False, *args, **kwargs):
        self.path = path
        self.name = name
        self.debug = debug
        super(App, self).__init__(*args, **kwargs)

    def __platform_list(self):
        """List platforms supported by cordova."""
        platform_ls_output = subprocess.check_output([
            'cordova', 'platform', 'ls'
        ], shell=self.debug).splitlines()

        installed = re.findall(r'[,:]\s(\w+)\s\d+', platform_ls_output[0])
        available = re.findall(r'[,:]\s(\w+)\s', platform_ls_output[1])

        return (installed, available)

    def installed_platform_list(self):
        """List the installed platforms for the project."""
        return self.__platform_list()[0]

    def available_platform_list(self):
        """List the available platforms that can be used by the project."""
        return self.__platform_list()[1]

    def add_platform(self, platform):
        """Add supported platform to the project."""
        return_code = subprocess.call([
            'cordova', 'platform', 'add', platform
        ], shell=self.debug)

        if return_code == 0:
            return True
        else:
            return False

    def remove_platform(self, platform):
        """Remove supported platfrom from the project."""
        return_code = subprocess.call([
            'cordova', 'platform', 'remove', platform
        ], shell=self.debug)

        if return_code == 0:
            return True
        else:
            return False

    def archive(self, platform):
        """Archive the android project files into a zip file."""
        os.chdir('platforms')
        return_code = subprocess.call([
            'tar', '-czf',
            '%s-%s.zip' % (
                self.name, platform
            ), platform
        ], shell=self.debug)

        if return_code == 0:
            return '%s/%s-%s.zip' % (
                os.getcwd(), self.name, platform
            )
        else:
            return False

    def build(self, platform, release=False):
        """Build cordova app for the project."""
        cmd_params = ['cordova', 'build', platform]

        if release:
            cmd_params.append('--release')

        return_code = subprocess.call(cmd_params, shell=self.debug)

        if return_code == 0:
            return os.path.join(
                self.path,
                BUILD_LOCATION[platform]
                ['release' if release else 'debug'] % (
                    'android' if platform == 'android' else self.name
                )
            )
        else:
            return False

    def sign_android_apk(self, keystore, keypass, storepass,
                         unsigned_apk=None):
        """Sign android apk for the cordova project."""
        if not unsigned_apk:
            unsigned_apk = os.path.join(
                self.path,
                BUILD_LOCATION["android"]["release"] % 'android'
            )

        return_code = subprocess.call(
            ['jarsigner',
             '-verbose',
             '-sigalg',
             'SHA1withRSA',
             '-digestalg',
             'SHA1',
             '-keystore',
             keystore,
             '-tsa',
             'http://tsa.starfieldtech.com',
             '-storepass',
             storepass,
             '-keypass',
             keypass,
             unsigned_apk,
             self.name
            ], shell=self.debug)

        signed_apk_name = os.path.join(
            self.path,
            BUILD_LOCATION["android"]["signed"] % (
                self.name,
                datetime.today().strftime("%d-%m-%y")
            )
        )

        if return_code == 0:
            if os.path.exists(signed_apk_name):
                os.remove(signed_apk_name)
            return_code = subprocess.call(
                [
                    "zipalign",
                    "-v",
                    "4",
                    unsigned_apk,
                    signed_apk_name
                ]
            )
            if return_code == 0:
                return signed_apk_name
        return False

    def prepare(self, platform):
        """Prepare cordova app for the project."""
        return_code = subprocess.call([
            'cordova', 'prepare', platform
        ], shell=self.debug)

        if return_code == 0:
            return True
        else:
            return False

    def compile(self, platform):
        """Compile the cordova source code without building the platform app."""
        return_code = subprocess.call([
            'cordova', 'compile', platform
        ], shell=self.debug)

        if return_code == 0:
            return True
        else:
            return False
