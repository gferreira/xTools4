txt = '''\
latestVersion=on
updateMechanic=on
readChangelog=on
foundBugs=on
bugsReport=in some of the batch tools, thereâ€™s an error message after the dialog is closed
issueTracker=on
isSatisfied=verySatisfied
isEssential=on
mostUsedTools=all of them except the batch tools maybe
leastUsedTools=never used batch find 
replace, for example. but itâ€™s good to have it there, you never know when youâ€™ll need it
moreProductive=on
featureRequests=the glyph tools, maybe their UI could be placed somewhere in the background of the glyph editor? to make it quicker to toggle things on/off.
useAPI=on
wouldRecommend=on
reasonsDelayRF4=my RF3 tools are working great. Iâ€™ve put a lot of time into them, and I donâ€™t have time at the moment to update all my code. I need to stay productive as a designer/foundry right now.
upgradeTime=6Months
comments=keep up the good work! all the best
'''

subs = [('â€™', '’')]

for L in txt.split('\n'):
    try:
        key, value = L.split('=')
    except:
        value += L

    for sub in subs:
        if sub[0] in value:
            value = value.replace(*sub)

    print(key)
    print(value)
    print()
