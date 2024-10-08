---
title     : Installing xTools4
layout    : page
order     : 4
permalink : /how-tos/installing-xtools4
---

xTools4 is packaged and distributed as a [RoboFont extension].
{: .lead}

* Table of Contents
{:toc}


Installing with Mechanic
------------------------

It is recommended to install xTools4 using [Mechanic], so you can easily check for updates and upgrade to the latest version of the tools.

1. After acquiring a license, you will receive a `xTools4.mechanic` file per email.
2. Go to the Mechanic extension’s settings.
3. Use the plus button to add the `.mechanic` file to the list of [Single Extension Items].

[RoboFont extension]: http://robofont.com/documentation/extensions/
[Mechanic]: http://github.com/robofont-mechanic/mechanic-2
[Single extension items]: http://robofont.com/documentation/extensions/managing-extension-streams/#adding-single-extension-items


Installing manually
-------------------

The xTools4 extension can also be installed manually if you have the extension package.

Simply double-click the file `xTools4.roboFontExt` to have it installed in RoboFont.

<div class="card text-dark bg-light my-3">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
If you install xTools4 manually, you will *not* be notified automatically about updates!
{: .card-text }
</div>
</div>


Installing from source
----------------------

xTools4 can be used directly from the source code if you have access to the repository.

This mode allows developers to make changes to the code while using and testing the tools in RoboFont.

1. Clone the repository using `git clone` (recommended) or download the source code.
2. In the RoboFont Preferences window, go to [Extensions > Start Up Scripts].
3. Add the file `xTools4/Lib/start.py` to the list of start-up scripts.
4. Save the settings and restart RoboFont – xTools4 will now appear in the main menu.

[Extensions > Start Up Scripts]: https://robofont.com/documentation/workspace/preferences-window/extensions/#start-up-scripts
