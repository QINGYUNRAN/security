<!--
 * @Author: uceewl4 uceewl4@ucl.ac.uk
 * @Date: 2024-03-05 11:10:24
 * @LastEditors: uceewl4 uceewl4@ucl.ac.uk
 * @LastEditTime: 2024-03-16 12:41:40
 * @FilePath: /security/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# security
UCL ELEC0138: Security and Privacy


file check may need to combine with database
database password encryption MD5


<!-- brute force kali commands -->
<!-- 1. sudo apt install openssh-client
2. sudo service ssh start
3. sudo hydra -l root -P /usr/share/wordlists/metasplpoit/unix_passwords.txt 127.0.0.1 ssh -t 4 -V -->
<!-- or 192.168.64.3 -->

to map tcpdump data into tcpdump_output.txt file:
cd Desktop/project
sudo tshark -i lo -Y "(udp || tcp.flags.syn == 1 || icmp)" -T fields -e frame.time_epoch -e ip.src -e frame.len -e _ws.col.Protocol -e _ws.col.Info -E header=y -E separator=, -E quote=d -E occurrence=f > ~/Desktop/project/tcpdump_output.txt

UDP Flood:
sudo hping3 --udp --flood --rand-source --destport 24 -c 500 127.0.0.1

SYN Flood:
sudo hping3 --syn --flood --destport 80 -c 500 127.0.0.1

ICMP Flood:
sudo hping3 --icmp --flood -c 500 127.0.0.1
