### Netmiko
* Has two fundamental ways for gathering show output:
    * send_command() :
        Entirely pattern-based solution, looks for the expect_string that we can specify 
        or alternatevely it looks for the trailing prompt 

    * send_command_timing():
        Timing based solution, it doesnot look for nor care about any pattern in the output
        It basically tries to intelligently guess whether the device is done outputting

    * send_command() is most valuable of two methods but sometimes we might have need to use
    timing based solution

    for example :
    ```
    with Connection Handler(**device) as conn:
        data = ""
        commands = [
            "ping",
            "\n",
            "8.8.8.8",
            "\n",
            "\n",
            "\n"
        ]
        for cmd in commands:
            data += conn.send_command_timing(
                cmd,
                strip_command = False,
                strip_prompt = False
            )
        print(data)
    ```

