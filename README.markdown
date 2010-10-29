# Eastwind

Eastwind helps backup configurations and package list and pack it to a eastwind
package.  The package can be easily applied, making installing and configuring
a lot easier.

If there is any issues or suggestions, please file an issue in
<http://github.com/eastwind/eastwind/issues>.

## Install
### Ubuntu
     sudo apt-add-repository ppa:eastwind/ppa
     sudo apt-get update
     sudo apt-get install eastwind

*Note:* on Karmic use `add-apt-repository` instead of `apt-add-repository`

### Other Distribution
     git clone git://github.com/eastwind/eastwind.git
     eastwind/bin/eastwind          # execute Eastwind

## Setup Config

In order to pack a eastwind package, the configuration file showing what to pack
should be provided, there are two ways to build the file:

1. Type the JSON file manually, for example:
        { "name": "vim",
          "actions": [
            {"config": "~/.vim"},
            {"config": "~/.vimrc"},
            {"install": "vim vim-latexsuite"}
          ]
        }
2. Use the record function of Eastwind
        eastwind record start vim
        eastwind install vim vim-latexsuite
        eastwind config ~/.vimrc
        eastwind record stop

## Pack and Unpack Eastwind Packages

 * Packing an Eastwind package
        eastwind pack vim.conf vim.eastwind
   or using the recorded configuration files
        eastwind pack-record vim vim.eastwind
 * Unpack an Eastwind package
        eastwind unpack vim.eastwind

