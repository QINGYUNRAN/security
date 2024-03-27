# security
UCL ELEC0138: Security and Privacy




## Project Structure

```plaintext
security/                      # Project root containing all attack related modules and data
│
├── attacks/                   # Core attack scripts and utilities
│   ├── attackpassword/        # Password attack strategies and functions
│   │   ├── HTTPHandshakeImpersonation.py
│   │   ├── meddle_password_file.py
│   │   ├── OWNERFromDevice.py
│   │   ├── OWNERFromMD5.py
│   │   └── UDPImpersonation.py
│   │
│   ├── brute_force/           # Scripts for performing brute force attacks
│   │   ├── brute_force.py
│   │   └── worst_passwords.txt
│   │
│   ├── http_flood/            # HTTP flood attack scripts
│   │   └── syn_flood.py
│   │
│   ├── https_cert/            # Certificates for HTTPS communication
│   │   ├── cert.pem
│   │   └── key.pem
│   │
│   ├── keylogger/             # Keylogging scripts and logged data
│   │   ├── keyfile.txt
│   │   └── keylogger_detector.py
│   │
│   └── ml_detector/           # Machine learning based attack detection scripts
│   │   ├── output/            # Output files
│   │   │   └── ...
│   │   ├── attack_detector.py    
│   │   ├── utils.py
│   │   ├── trained_model_KNN.joblib
│   │   ├── trained_model_LR.joblib
│   │   ├── trained_model_RF.joblib
│   │   ├── network_traffic.csv
│   │   └── trained_model_SVM.joblib
│   │
│   ├──── 2FA.py
│   ├──── file_checker.py
│   └──── TCP.py
│
├── data/                      # General data storage for the application
│   └── files/                 # Various files such as account lists and test files
│       ├── account.csv
│       ├── test.rtf
│       └── test copy.rtf
│
├── func/                      # Utility functions for the application's backend logic
│   ├── __init__.py
│   ├── check_ip.py
│   ├── database.py
│   └── keyPressed.py
│
├── static/                    # Static files for the web interface
│   └── style.css
│
├── templates/                 # HTML template files for the web interface
│   ├── auth/                  # Authentication related templates
│   │   ├── auth_layout.html
│   │   ├── login.html
│   │   ├── profile.html
│   │   ├── register.html
│   │   └── verify.html
│   │
│   ├── home/                  # Home page and related functionality templates
│   │   ├── change_password.html
│   │   ├── checkin.html
│   │   ├── holidays.html
│   │   ├── home.html
│   │   ├── layout.html
│   │   ├── salary.html
│   │   └── alert.html
│   │
│   └── includes/              # Included HTML fragments for use in multiple templates
│
└── app.py                     # Main application file

```

### File Descriptions

- `app.py`: The Flask application's main entry point, orchestrating the security system's functionality.

#### Attack Modules

- `attacks/attackpassword/`: # Holds scripts for password attack simulations.
  - `HTTPHandshakeImpersonation.py`: Tries to impersonate handshaking protocols to test system security.
  - `meddle_password_file.py`: Modifies password records for penetration testing purposes.
  - `OWNERFromDevice.py`: Extracts device owner information under certain conditions.
  - `OWNERFromMD5.py`: Attempts to derive owner information from MD5 hash values.
  - `UDPimpersonation.py`: Performs UDP packet impersonation to test system defenses.

- `attacks/brute_force/`: # Contains strategies for brute-forcing passwords.
  - `brute_force.py`: Implements a brute force attack mechanism to crack passwords.
  - `worst_passwords.txt`: A list of common passwords used in brute force attack simulations.

- `attacks/http_flood/`: # Scripts for simulating HTTP flood attacks.
  - `syn_flood.py`: Executes a SYN flood attack to evaluate the system's resilience against DoS attacks.

- `attacks/keylogger/`: # Includes keylogger scripts for monitoring keystrokes.
  - `keylogger_detector.py`: Detects potential keylogging activity.
  - `keyfile.txt`: Logs captured keystrokes.

- `attacks/ml_detector/`: # Machine learning models for detecting network attacks.
  - `2FA.py`: A two-factor authentication testing script.
  - `utils.py`: Utility functions for the ML-based attack detector.

- `file_checker.py`: Checks file integrity to detect potential tampering.
- `TCP.py`: Analyzes TCP network traffic for anomaly detection.
- `attack_detector.py`: Main script that uses machine learning models to detect network attacks.
- 
#### Functional Utilities

- `func/`: # Utility scripts supporting the main application.
  - `check_ip.py`: Enforces IP address check and login attempt restrictions.
  - `database.py`: Manages database operations for the security system.
  - `keyPressed.py`: Functionality related to capturing and processing keystrokes.

#### Static Files and Templates

- `static/`: # Contains static assets like stylesheets for the web interface.
  - `style.css`: The main stylesheet for the web interface styling.

- `templates/`: # HTML templates for the web interface rendering.
  - `auth/`: Authentication related HTML templates.
  - `home/`: Home page and related functionalities HTML templates.
  - `includes/`: Shared HTML components used across different templates.



## Packages and Requirements

This program runs under Python version 3.10.0.
The project depends on several external libraries, which are listed in `environment.yml`. To install these dependencies, run the command below:

```sh
conda env create -f environment.yml
```


## Running the Security System

To start the security system using `app.py`, use the following command-line arguments to customize the security features:

- `--xss`: Enables or disables protection against XSS attacks. Set to `True` to enable.
- `--keylogger`: Toggles the keylogger functionality. Set to `True` to enable.
- `--filecheck`: Activates file integrity checking. Set to `True` to enable.
- `--wifiscanner`: If set to `True`, it activates the Wi-Fi network scanning feature.
- `--mldetector`: Specify the machine learning model to use for attack detection. Options are 'SVM', 'RF', 'LR', 'KNN'.
- `--train`: Decides whether to train the machine learning model. Set to `True` to initiate training.

Each feature is independently controlled and can be combined to enhance the system's security measures as required. 

For example, to enable file integrity checks and machine learning-based attack detection with the SVM model, while also initiating model training, your command would look like this:

```sh
python app.py --filecheck True --mldetector SVM --train True
```

To run the Wi-Fi scanner, simply pass True to the --wifiscanner option. You will be prompted to enter the IP address range:
```sh
python app.py --wifiscanner True
```


## Cont'
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
