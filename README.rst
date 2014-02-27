Introduction
============

This program is designed for Floodlight Static Flow Pusher API.

Due to Floodlight Static Flow Pusher API is too difficult to use. This 
program provide a better UI and simple foolproof.

And also, this program is written in pure Python, so you can run it on Windows,
too. (All you need is installing Python 2.x on Windows)

Ref: http://www.openflowhub.org/display/floodlightcontroller/Static+Flow+Pusher+API


Usage
=====

``Usage: ./flow_injector.py action config_file``

``action`` can be:

- add
    Add all the flows in config_file. (POST /wm/staticflowentrypusher/json)
  
- show
    Show all the flows on the switch. (GET /wm/staticflowentrypusher/list/)
    
- clean
    Clean all the flows on the switch. (GET /wm/staticflowentrypusher/clear/)

config_file is in `ini format <http://en.wikipedia.org/wiki/INI_file>`_.  It
requires ``server`` and ``port`` properties in ``controller`` section.
The other sections are optinal. The name of the section means its name, the
properties is same as `Static Flow Pusher API`__.

.. note:: If all your flows have same property (ex: switch), you can specify
    them in ``DEFAULT`` section (see template.ini).

__ http://www.openflowhub.org/display/floodlightcontroller/Static+Flow+Pusher+API

Future work
===========
1. More foolproof. (ip, mac format check, fields correctness)
2. 'actions' fields foolproof.
3. Move to Python3.

