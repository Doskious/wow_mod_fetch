# Download-and-Install Updated WoW AddOns

Based on a Chrome Bookmark folder to pages that auto-download the zip files.

This code includes a boatload of stuff that is specific to the system it was originally written for.

- May not work out-of-the-box on Windows or OS X
- Not easily configurable (lots of hard-coded assumptions about the locations of things)
- Not as thoroughly commented as one might prefer.
- Assumes you don't have to worry about internet bandwidth

Sersiously, if you have significant bandwidth or internet usage limitations or costs, this is probably not the right solution for you, because it loops through a bookmark list of sites (which have to be to web pages that, after each one is loaded, automatically download the AddOn) and opens them in new tabs in a dedicated Chrome instance.  This results in Every. Single. Addon. File. getting downloaded Every. Single. Time. that the application is executed with its default options.  If that would cause problems, this is not a good solution for managing your WoW AddOns, I'm sorry.

I wrote this as a reaction to the sale/handoff of the CurseForge AddOn Manager functionality from Twitch (using the Twitch App) to Overwolf (and their own app which (1) seems to come with a bunch of strings attached and (2) is not able to be run (thanks to their selection of code-libraries) in Linux), and because I have concerns about the compatability (both current and future) of other existing solutions with the Overwolf Terms.
