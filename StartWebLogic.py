from ConnectionSSH import ConnectionSSH
import ReadProperties

connectionSSH = ConnectionSSH()

ConfigParser = ReadProperties.ConfigParser()
prop = ConfigParser.read_config()

ssh = connectionSSH.get_ssh_connection()
shell = ssh.invoke_shell()
shell.send('WLS_USER=' + prop.get('weblogic', 'start.weblogic.username') +'\n')
shell.send('export WLS_USER\n')
shell.send('WLS_PW=' + prop.get('weblogic', 'start.weblogic.password') +'\n')
shell.send('export WLS_PW\n')
shell.send('nohup ' + prop.get('weblogic', 'start.script') + ' &> pyStartWebLogic.out&\n')

runCommand = connectionSSH.run_command('tail -100f pyStartWebLogic.out\n')

trys = 0

for output, channel in runCommand:
    if '<Server state changed to RUNNING.>' in output:
        print('WebLogic is RUNNING!')
        shell.send('rm -Rf pyStartWebLogic.out\n')
        quit()
    if 'Ensure that another server is not running in the same directory' in output:
        trys += 1
        print('Ensure that another server is not running in the same directory.  Try (%d/3)' % trys)
    if 'AdminServer.lok. Server may already be running' in output:
        lines = output.split('\t')
        for line in lines:
            if 'AdminServer.lok. Server may already be running' in line:
                lineSplit = line.split(' ')
                for string in lineSplit:
                    if 'lok.' in string:
                        print('Server may already be running. The .lok exist (%s)' % string)
                        quit()
        quit()

connectionSSH.ssh.close()
