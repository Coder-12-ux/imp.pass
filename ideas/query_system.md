# Commands

-   set
-   get
-   delete
-   update

# Menu Items

-   set
-   get
-   delete
-   update

<br>

parameters with '\*' are optional or based on the flags

# **set**

    parameters: (pid) (password)
    description: saves a new password
    flags: none

# **get**

    parameters: (pid)
    description: prints the password
    flags: 2, c - copy, e - echo

# **delete**

    parameters: (pid)
    description: deletes the password from the database
    flags: none

# **update**

    parameters: (pid) (newPid)* (newPassword)
    description: replaces the previous password saved with new password given.
    flags: -p: replaces the pid with the new pid

# **other options**
    parameters: (option)
    description: some other operations :
        - changing the master password
        - changing the username

