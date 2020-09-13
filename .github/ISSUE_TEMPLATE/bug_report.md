---
name: Bug report
about: Create a report to help us improve
title: "[BUG] <bug title>"
labels: bug
assignees: MartinHeroux

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behaviour:
```python
>>> from spike2py import TrialInfo, Trial
>>> post_fatigue_info = TrialInfo(file='post_fatigue.mat')
>>> post_fatigue = Trial(post_fatigue_info)
>>> post_fatigue. [tab]
# Channel 'Biodex_torque' not present
```

**Expected behaviour**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Python:**
 - Version [e.g. 3.8]
 - Dependencies and version [e.g. numpy (1.19.1)]

**Additional context**
Add any other context about the problem here.

**PLEASE REMOVE THIS TEMPLATE BEFORE SUBMITTING**
