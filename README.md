# Snirf Validator :microscope:

## Table of Contents

- [Background](#background)
- [Installation](#installation)
- [Usage](#usage)
  - [Flowchart](#flowchart)
  - [Demo](#demo)
- [API](#api)
- [Maintainers](#maintainers)
- [Contributors](#contributors)
- [License](#license)


## Background :bulb:

## Installation :floppy_disk:

## Usage :clipboard:
The `Snirf.py` mainly performs two functions: read a snirf file and save the result. The saved file can pass: SNIRF validator, HDFviewer, and [Homer3](https://github.com/BUNPC/Homer3). The idea of how `snirf.py` works and a demo of how to use can be found below.
### Flowchart
[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgIEFbRklsZSBVcGxvYWRdIC0tPiBCe0ZpbGUgVmFsaWRhdGlvbn1cbiAgIEIgLS0-IENbVmFsaWRdIC0tPiBFW1JlYWQgdGhlIEZpbGVdIC0tPkZbU2F2ZSB0aGUgRklsZV1cbiAgIEIgLS0-IERbTm90IFZhbGlkXSAtLT4gR1tSZWplY3RdXG4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgIEFbRklsZSBVcGxvYWRdIC0tPiBCe0ZpbGUgVmFsaWRhdGlvbn1cbiAgIEIgLS0-IENbVmFsaWRdIC0tPiBFW1JlYWQgdGhlIEZpbGVdIC0tPkZbU2F2ZSB0aGUgRklsZV1cbiAgIEIgLS0-IERbTm90IFZhbGlkXSAtLT4gR1tSZWplY3RdXG4iLCJtZXJtYWlkIjoie1xuICBcInRoZW1lXCI6IFwiZGVmYXVsdFwiXG59IiwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)
### Demo
To run this app you must have python installed.
To run this app you must indicate where the dataset is loacted. This is done by passing the location of the dataset to `oneSnirfClass` and using build-in function `SnirfLoad`. A minimal exmaple of how to run snirf.py is:
```python
import Snirf
```
```python
oneSnirfClass=Snirf.SnirfLoad('/Users/Jiazhenliu/Downloads/resting_state_2/Subj86/resting_hrf_20.snirf')
```
To save the result, you must use buid-in funciton `SnirfSave`. A minimal example of how to save the result is:
```python
Snirf.SnirfSave(oneSnirfClass,'/Users/Jiazhenliu/Desktop/testingresult.snirf')
```

## API

## Maintainers :hammer_and_wrench:
[@Christian Arthur :melon:](https://github.com/chrsthur)<br>
[@Juncheng Zhang :tangerine:](https://github.com/andyzjc)<br>
[@Jeonghoon Choi :pineapple:](https://github.com/jeonghoonchoi)<br>
[@Jiazhen Liu :grapes:](https://github.com/ELISALJZ)<br>

## Contributors
This project exsists thanks to all people who contribute. <br>
<center class= "half">
<a href="https://github.com/sstucker">
<img src="https://github.com/sstucker.png" width="50" height="50">
</a>

<a href="https://github.com/rob-luke">
<img src="https://github.com/rob-luke.png" width="50" height="50">
</a>

<a href="https://github.com/chrsthur">
<img src="https://github.com/chrsthur.png" width="50" height="50">
</a>

<a href="https://github.com/andyzjc">
<img src="https://github.com/andyzjc.png" width="50" height="50">
</a>

<a href="https://github.com/jeonghoonchoi">
<img src="https://github.com/jeonghoonchoi.png" width="50" height="50">
</a>

<a href="https://github.com/ELISALJZ">
<img src="https://github.com/ELISALJZ.png" width="50" height="50">
</a>
                                                     </center>

## License








