<h1 align="center">Welcome to DiskUsage 👋</h1>
<p>
  <a href="https://github.com/gx56q/CloudBackup/blob/master/LICENSE" target="_blank">
    <img alt="License: MIT license" src="https://img.shields.io/badge/License-MIT license-yellow.svg" />
  </a>
</p>

> Utility for visualizing disk usage.

## Installation
To use DiskUsage, follow these steps:

#### 1. Clone the repository:
```sh
git clone https://github.com/gx56q/DiskUsage.git
```
#### 2. Navigate to the project directory:
```sh
cd DiskUsage
```
#### 3. Install the required dependencies using pip:
```sh
pip install -r requirements.txt
```

## Usage

DiskUsage provides a command-line interface for visualizing disk usage. To use DiskUsage, follow these steps:

```sh
python3 main.py [path] -filter [filters] -group [group_by]
```

### Filters and Grouping

Available filters and grouping options:

| Filter/Grouping | Description                                |
|-----------------|:-------------------------------------------|
| -e, --extension | Filter/Group by extension.                 |
| -s, --size      | Filter/Group by file size/number of files. |
| -d, --date      | Filter/Group by date.                      |
| -o, --owner     | Filter/Group by owner.                     |
| -n, --nesting   | Filter/Group by nesting level.             |

#### Help

To get help on the available options and actions, use the -h or --help option. The command format is:

```sh
python3 main.py --help
```


### Example

To visualize disk usage of the /home/user directory, grouped by extension, use the following command:

```sh
python3 main.py /home/user -filter -e -group -s
```

## Author

👤 **Voinov Andrey**

* Github: [@gx56q](https://github.com/gx56q)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/gx56q/CloudBackup/issues). 

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2023 [Voinov Andrey](https://github.com/gx56q).<br />
This project is [MIT license](https://github.com/gx56q/CloudBackup/blob/master/LICENSE) licensed.

***