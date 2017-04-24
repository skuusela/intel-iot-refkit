import os
import subprocess
from time import sleep
from oeqa.oetest import oeRuntimeTest

class NftablesTest(oeRuntimeTest):

    test_path = "/opt/nftables-test/"
    reject_script = "nftables_reject.sh"
    drop_script = "nftables_drop.sh"
    reject_script_path = os.path.join(os.path.dirname(__file__), "files", reject_script)
    drop_script_path = os.path.join(os.path.dirname(__file__), "files", drop_script)

    def setUp(self):
        # Copy test scripts to device
        self.target.run("mkdir -p " + self.test_path)
        self.target.copy_to(self.reject_script_path, self.test_path)
        self.target.copy_to(self.drop_script_path, self.test_path)

    def tearDown(self):
        self.target.run("rm -r " + self.test_path)

    def check_ssh_connection(self, port="22"):
        process = subprocess.Popen(("ssh -o UserKnownHostsFile=/dev/null " \
                                    "-o ConnectTimeout=3 " \
                                    "-o StrictHostKeyChecking=no root@" + \
                                    self.target.ip +" -p "+ port +" ls").split(),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        output, err = process.communicate()
        output = output.decode("utf-8")
        returncode = process.returncode
        return output, returncode

    def test_reject(self):
        '''
        Test rejecting SSH with nftables
        '''
        # Check that SSH gets rejected when nftables rejects it
        self.target.run("nohup " + self.test_path + self.reject_script + " &>/dev/null &")
        output, returncode = self.check_ssh_connection()
        self.assertIn("Connection refused", output, msg="Error message: %s" % output)
        sleep(3) # Wait for script to make iptables accept SSH again

        # Check that SSH can connect
        output, returncode = self.check_ssh_connection()
        self.assertEqual(returncode, 0, msg="Error message: %s" % output)

    def test_drop(self):
        '''
        Test dropping SSH with nftables
        '''
        # Check that SSH gets timeout when nftables drops it
        self.target.run("nohup " + self.test_path + self.drop_script + " &>/dev/null &")
        output, returncode = self.check_ssh_connection()
        self.assertIn("Connection timed out", output, msg="Error message: %s" % output)
        sleep(5) # Wait for script to make iptables accept SSH again

        # Check that SSH can connect
        output, returncode = self.check_ssh_connection()
        self.assertEqual(returncode, 0, msg="Error message: %s" % output)

    def test_nat(self):
        '''
        Test nat forwarding
        '''
        # Check that SSH can't connect to port 2222
        output, returncode = self.check_ssh_connection(port="2222")
        self.assertIn("Connection timed out", output, msg="Error message: %s" % output)

        # Check that port 2222 gets redirected and SSH can connect
        self.target.run("nft add table nat")
        self.target.run("nft add chain nat prerouting {type nat hook prerouting priority 0 \;}")
        self.target.run("nft add chain nat postrouting {type nat hook postrouting priority 100 \;}")
        self.target.run("nft add rule nat prerouting tcp dport 2222 redirect to 22")
        output, returncode = self.check_ssh_connection(port="2222")
        self.assertEqual(returncode, 0, msg="Error message: %s" % output)
        self.target.run("nft delete table nat")

        # Check that SSH can't connect to port 2222
        output, returncode = self.check_ssh_connection(port="2222")
        self.assertIn("Connection timed out", output, msg="Error message: %s" % output)
