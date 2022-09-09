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
* **modify send_command_timing's behavior**
* 1. increase last_read 
* 2. modify read_timeout
* 3. set read_timeout = 0

```
def send_command_timing(
    self,
    command_string: str,
    last_read:float = 2.0,
    read_timeout:float = 120.0
    )
```
* If the case where we are not capturing all the data we require then we should increase 
the last_read time 
```
data = conn.send_command_timing(
    "ping 8.8.8.8",
    last_read=8.0
)
```
* If in case we are executing a command that is continuously outputting data for a long period
of time and we're running into the ReadTimeout exception, the we should increase read_timeout 

```
data = conn.send_command_timing(
    "show ip bgp",
    read_timeout=600
    # cease reading due to read_timeout
    # will keep reading until last_read completes successfully
    read_timeout=0
)
```



