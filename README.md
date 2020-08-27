# MCPI-Central
Minecraft Pi centralized API.

## Getting started
### Prerequisites
To use the API you need to have `Python >= 3.7.x` pre-installed.

### Installation
To install the API server and client, download or clone the repository and install the Python 3.x module using `pip`:
```shell
git clone https://github.com/MCPI-Devs/mcpi-central.git
cd mcpi-central
pip3 install .
```

## API
The client API exposes the following methods through the `APIClient` class:

### `def login()`
| Authentication required |                      Endpoint                  | Method  | Query parameters |
| :---------------------: | :--------------------------------------------: | :-----: | :--------------: |
|           :x:           | [/auth](https://mcpi-devs.herokuapp.com/auth)  | **GET** |      `code`      |

Listens to `http://localhost:19140`, waits for a Discord OAuth callback and exchanges the `code` for the `token`. You can generate this callback by opening [this link](https://discord.com/oauth2/authorize?client_id=744320103566540912&redirect_uri=http%3A%2F%2Flocalhost%3A19140%2Fauth&response_type=code&scope=identify%20email), logging-in and authorizing the app in a web browser.

### `def new_server(name, ip, port)`
| Authentication required |                             Endpoint                         | Method  |   Query parameters   |
| :---------------------: | :----------------------------------------------------------: | :-----: | :------------------: |
|   :heavy_check_mark:    | [/servers/new](https://mcpi-devs.herokuapp.com/servers/new)  | **GET** | `name`, `ip`, `port` |

Adds a new server to the database. The server should not already exist, to update a server information, use `update_server`.

### `def update_server(name, ip, port)`
| Authentication required |                                Endpoint                            | Method  |   Query parameters   |
| :---------------------: | :----------------------------------------------------------------: | :-----: | :------------------: |
|   :heavy_check_mark:    | [/servers/update](https://mcpi-devs.herokuapp.com/servers/update)  | **GET** | `name`, `ip`, `port` |

Updates an existing server in the database. The user requesting this action should be the owner of the server.

### `def get_server(name)`
| Authentication required |                        Endpoint                    | Method  | Query parameters |
| :---------------------: | :------------------------------------------------: | :-----: | :--------------: |
|           :x:           | [/server](https://mcpi-devs.herokuapp.com/server)  | **GET** |      `name`      |

Returns the information of an existing server in the database.

### `def get_servers()`
| Authentication required |                         Endpoint                     | Method  | Query parameters |
| :---------------------: | :--------------------------------------------------: | :-----: | :--------------: |
|           :x:           | [/servers](https://mcpi-devs.herokuapp.com/servers)  | **GET** |       None       |

Returns the names of the first 50 servers in the database.

## FAQ
### Where can I find an usage example?
There is a [`test.py`](https://github.com/MCPI-Devs/mcpi-central/blob/master/src/test.py) in the [`src`](https://github.com/MCPI-Devs/mcpi-central/tree/master/src) folder. It contains a basic usage example.

### Why the `login` function doesn't open a web browser directly?
Because some developers could want to use custom methods to open the authorization page, like WebViews.

## Licensing
All the code of this project is licensed under the [GNU General Public License version 2.0](https://github.com/MCPI-Devs/proxy/blob/master/LICENSE) (GPL-2.0).

All the documentation of this project is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) (CC BY-SA 4.0) license.

![CC BY-SA 4.0](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)
