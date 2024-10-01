---
title  : Installing hTools3
layout : page
order  : 4
---

hTools3 is packaged and distributed as a [RoboFont extension].
{: .lead}


Installing with Mechanic
------------------------

It is recommended to install hTools3 using [Mechanic], so it can automatically check for updates and install them.

1. After acquiring a license, you will receive a `hTools3.mechanic` file per email.
2. Go to the Mechanic extension’s settings.
3. Use the plus button to add the `.mechanic` file to the list of [Single Extension Items].

[RoboFont extension]: http://robofont.com/documentation/extensions/
[Mechanic]: http://github.com/robofont-mechanic/mechanic-2
[Single extension items]: http://robofont.com/documentation/extensions/managing-extension-streams/#adding-single-extension-items


Installing manually
-------------------

The hTools3 extension can also be installed manually if you have the extension package.

Simply double-click the file `hTools3.roboFontExt` to have it installed in RoboFont.

<div class="card text-dark bg-light my-3">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
If you install hTools3 manually, you will *not* be notified automatically about updates!
{: .card-text }
</div>
</div>


Installing from source
----------------------

hTools3 can be used directly from the source code if you have access to the repository.

This mode allows developers to make changes to the code while using and testing the tools in RoboFont.

1. Clone the repository using `git clone` (recommended) or download the source code.
2. In the RoboFont Preferences window, go to [Extensions > Start Up Scripts].
3. Add the file `hTools3/Lib/start.py` to the list of start-up scripts.
4. Save the settings and restart RoboFont – hTools3 will now appear in the main menu.

[Extensions > Start Up Scripts]: https://robofont.com/documentation/workspace/preferences-window/extensions/#start-up-scripts
