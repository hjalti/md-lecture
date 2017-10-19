Markdown lectures
=================

What is it?
-----------

Md-lecture is a tool for generating PDF lectures from Markdown documents. At
the moment only one template is provided for the generated lectures, namely for
Reykjavík University.


Dependencies
------------

Md-lecture uses [pandoc](https://pandoc.org/) to generate PDF documents from
markdown. Pandoc uses LaTeX to generate PDF documents. Both pandoc and a LaTeX
compiler (e.g. texlive) must be installed.

Installation
------------

Install via `pip`. Either globally

```
sudo pip install git+https://github.com/hjalti/md-lecture@master
```

or in a virtualenv

```
pip install git+https://github.com/hjalti/md-lecture@master
```


Basic usage
-----------

After installation the program can be run with the command `mdl`.

To start with, move to a directory which is to serve as a base directory for
a group of lectures and initialize using

```
mdl init
```

This creates a directory `.lecture`, in the current directory, which contains
the template used to generate PDF lectures from markdown files in all
subdirectories of the current directory.

To create a new lecture, make a new directory move into it. To initialize a markdown file, run

```
mdl new lecture
```

which will create a markdown file *lecture.md* for the lecture.

To build lecture from a markdown file, run

```
mdl make
```

in the same directory as *lecture.md*. This will generate the lecture in the file *lecture.pdf*.

Similar to `make` you can run

```
mdl watch
```

which runs a daemon that rebuilds the markdown file each time it changes.


Advanced usage
--------------

With the `make` and `watch` commands, you can add the option `-p` (or
`--post-hook`) to run the input file through a python script before being
handed over to pandoc. The argument specified should be the name of a python
module which should contain the function `process` which takes a single
argument, the path to the target file. The function returns a string containing
the markdown that will be piped to pandoc to produce the slides.

Hooks should be added to the hooks directory in the template directory. As an
example a hook called pyeval is provided, which evaluates all lines starting
with `>>>` in the document and outputs the result of the evaluation in the
following line.
