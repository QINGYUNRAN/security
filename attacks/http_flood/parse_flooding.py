import pyshark
import pandas as pd

import sys


def main(filename: str):
    data = []
    cap = pyshark.FileCapture(filename)
    first_timestamp = 0
    for packet in cap:
        if first_timestamp == 0:
            first_timestamp = packet.sniff_time.timestamp()
        info = ""
        protocol = ""
        if "IP" in packet:
            protocol = "IP"
            if "ICMP" in packet:
                protocol = "ICMP"
            if "TCP" in packet:
                protocol = "TCP"
                if (
                    hasattr(packet.tcp, "flags_syn")
                    and str(packet.tcp.flags_syn) == "1"
                ):
                    info += "[SYN]"
                if (
                    hasattr(packet.tcp, "flags_ack")
                    and str(packet.tcp.flags_ack) == "1"
                ):
                    info += "[ACK]"
            if "UDP" in packet:
                protocol = "UDP"
            row = {
                "No.": packet.number,
                "Time": packet.sniff_time.timestamp() - first_timestamp,
                "Source": packet.ip.src,
                "Destination": packet.ip.dst,
                "Protocol": protocol,
                "Length": packet.length,
                "Info": info,
            }
            data.append(row)
    df = pd.DataFrame(data)
    df.to_csv(filename.split(".")[0] + ".csv")


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
