![](https://raw.githubusercontent.com/wdbm/dendrotox/master/media/dendrotox.png)

`dendrotox` is a Python module designed to enable Python code to interact with the [Tox](https://tox.chat/) distributed communications network, including for the purposes of scripts communicating with people or other scripts. It uses a 2015 version of [ToxCore](https://github.com/irungentoo/toxcore/releases/tag/api_old_version) and [ratox](https://github.com/kytvi2p/ratox) for interfacing with the Tox network and [megaparsex](https://github.com/wdbm/megaparsex) for parsing.

In particular, `dendrotox` interacts with the filesystem provided by the FIFO Tox client [ratox](https://github.com/kytvi2p/ratox). `dendrotox` also provides functionality to send and receive messages, to parse input, to send files, to request confirmations, to provide information such as IP address and weather information, and to run arbitrary commands, including functionality to launch reverse-SSH connections and to restart a script.

# setup

```Bash
sudo apt-get install\
    autoconf        \
    autotools-dev   \
    automake        \
    build-essential \
    checkinstall    \
    check           \
    cmake           \
    git             \
    libtool         \
    libsodium-dev   \
    yasm
```

```Bash
cd ~
mkdir Tox
cd Tox
```

Install the Sodium crypto library.

```Bash
git clone https://github.com/jedisct1/libsodium.git
cd libsodium
git checkout tags/1.0.3
./autogen.sh
./configure
make check
sudo checkinstall --install --pkgname libsodium --pkgversion 1.0.0 --nodoc
sudo ldconfig
cd ..
```

Install the libvpx codec.

```Bash
git clone https://chromium.googlesource.com/webm/libvpx
cd libvpx
git checkout tags/v1.4.0
./configure --enable-shared --disable-static
make -j$(nproc)
sudo make install
cd ..
```

Install ToxCore.

```Bash
wget --content-disposition https://codeload.github.com/irungentoo/toxcore/tar.gz/api_old_version
tar -xvf toxcore-api_old_version.tar.gz
cd toxcore-api_old_version
autoreconf --install --force
mkdir _build
cd _build
../configure
make -j$(nproc)
sudo make install
sudo ldconfig
cd ../..
```

Install `ratox`.

```Bash
#git clone git://git.2f30.org/ratox.git
git clone https://github.com/kytvi2p/ratox.git
cd ratox
make -j$(nproc)
sudo make install
```

Install dendrotox.

```Bash
sudo pip install dentrodox
```

When `ratox` is launched for the first time, it creates a file `.ratox.tox` at the working directory to store Tox profile details. While running, the file `id` contains the Tox ID.

# examples

`dendrotox` is imported and launched in the following way:

```Python
import dendrotox

dendrotox.start_messaging()

print("Tox ID: " + dendrotox.self_ID())
```

A message can be sent to a contact in the following way, where a contact is specified using a string containing their Tox ID:

```Python
dendrotox.send_message(
    contact = Tox_ID,
    text    = "oohai"
)
```

A message can be sent to multiple contacts in the following way, where contacts are specified as a list of strings containing contacts' Tox IDs.

```Python
dendrotox.send_message(
    contacts = [Tox_ID_1, Tox_ID_2],
    text     = "sup"
)
```

A list of unseen messages received recently can be accessed in the following ways:

```Python
messages = dendrotox.received_messages()

print(messages[0].sender())
```

```Python
message = dendrotox.last_received_message()

print(message.__repr__())
```

See example bot code for more advanced usage, including message parsing, confirmations and running commands.

# dendrotox_alert.py

The script `dendrotox_alert.py` is a command line script that can be used to send a message to contacts. It attempts to connect with any specified contacts before attempting to send a message to them. If no contacts are specified, it attempts to send a message to all known contacts.

```Bash
dendrotox_alert.py --text="alert"
```
