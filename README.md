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
python3 main.py [path] --filter [filter_type] --value [filter_value] --group [group_by_type]
```

### Filters and Grouping
You can filter or group the disk usage results using several criteria.

Available filters and grouping options:

| Filter/Grouping | Description                    |
|-----------------|:-------------------------------|
| `extension`     | Filter/Group by extension.     |
| `size`          | Filter/Group by file size      |
| `file_count`    | Filter/Group by file count.    |
| `date_created`  | Filter/Group by date created.  |
| `date_modified` | Filter/Group by date modified. |
| `owner`         | Filter/Group by owner.         |
| `nesting`       | Filter/Group by nesting level. |

To specify the specific value for filtering, use the `--value` or `-v` option.

To launch the interactive UI, use the `--interactive` or -`i` option.

### Examples

#### Basic Usage
To simply visualize disk usage of the /home/user directory:
```sh
python3 main.py /home/user
```

#### Filtering by Extension
To visualize disk usage of the /home/user directory, filtering only .txt files:

```sh
python3 main.py /home/user --filter extension --value .txt
```

#### Grouping by Size
To visualize disk usage of the /home/user directory, grouping results by file size:

```sh
python3 main.py /home/user --group size
```

#### Filter and Group
To filter by .txt extension and then group by owner:

```sh
python3 main.py /home/user --filter extension --value .txt --group owner
```

#### Interactive Mode
To launch the interactive UI for the /home/user directory:

```sh
python3 main.py /home/user --interactive
```

### Help

To get help on the available options and actions, use the `-h` or `--help` option. The command format is:

```sh
python3 main.py --help
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