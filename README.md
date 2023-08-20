# Google-HPS-2023-Team8
A project created by Team 8 of Google Hardware Product Sprint (HPS) Program 2023.

- [System Testing](#system-testing)
    - [Prerequisite](#prerequisite)
        - [Arduino](#arduino)
        - [Raspberry Pi](#raspberry-pi)

## System Testing

### Prerequisite

#### Arduino

1. Use Arduino IDE to upload `./src/arduino/main/main.ino`.
2. Force sensor: `PIN A1-A5`.
3. LED strand: `PIN 6`.


#### Raspberry Pi

1. Open Terminal/PowerShell.
2. `cd` (change directory) to the project directory.
    ```sh
    cd [your_path]/Google-HPS-2023-Team8
    ```
3. Use `ls` (list) to check if you are in the right place. (For more information, use `ls -al`) Terminal should show something like these:
    ```sh
    (...)
    -rw-r--r--    1 andrewchiu  staff  1068 Jul 21 04:28 LICENSE
    -rw-r--r--    1 andrewchiu  staff   660 Aug 20 08:53 README.md
    (...)
    ```
4. Update the project by `git`.
    1. Check the status of git by
        ```sh
        git status
        ```
    2. Terminal should show something like these:
        ```sh
        (...)
        nothing to commit, working tree clean
        ```

        > If it says `no changes added to commit (use "git add" and/or "git commit -a")`, then commit or drop the changes first.
    3. `pull` from remote
        ```sh
        git pull
        ```
        > If some warnings or errors show, please connect to Andrew.

5. Use python to run the tests.
    ```sh
    python3 ./tests/[test_name].py
    ```