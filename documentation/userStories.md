# User Stories
---
## Task Lists
1. ### __As a user, I want to create lists, so that I can start planning tasks.__
   - _Implemented in index. There is a form at the top to name and create new lists._
2. ### __As a user, I want to delete lists, so that I can get rid of clutter.__
   - _Implemented in index. Each list now has its own delete button._
3. ### __As a user, I want to rename lists, so that I can fix mistakes.__
   - _Implemented in index and /renameList. Each list now has an edit button that takes you to a renaming page._
4. ### __As a user, I want to open a task list, so that I can start working on it.__
   - _Implemented in index. Each list name is a link to its own page._
5. ### __As a user, I want to close a task list, so that I can see all my lists again.__
   - _Possible by using the browser's back feature to return to index._
---
## Tasks
1. ### __As a user, I want to add new tasks to my list, so that I can keep track of them.__
    - _Implemented in /list. There is a form at the top to enter task text and add it to the list._
        - There's a bug here. It works for a list that already has tasks, but not an empty list.
          - I can see them added to empty lists in /admin, but it's not visible in /list.html
2. ### __As a user, I want to mark tasks as completed, so that I can tell what I need to work on.__
    - _Implemented in /list. Each task now has a toggle button to mark completion._
3. ### __As a user, I want to edit tasks, so that I can fix mistakes.__
4. ### __As a user, I want to delete tasks, so that I can clean up my list.__
    - _Implemented in /list. Each task now has a button to delete it._
---
## Meta
1. ### __As a user, I want to protect my system, so that only I can access it.__