# GroundStation
MVC GroundStation

This is a Ground station intended to recieve data from our radio and then output it in whatever fashion we want.


Getting Started

Download PyCharm, Git Bash, or some other command line interface (Bash for Windows 10, etc.)

Create a folder on your computer. For example,

mkdir ~/git/Karman
Navigate to this directory in the comand line interface. If you are using Cygwin or Bash, this means typing

cd ~/git/Karman
Where ~ means "My home directory" (C:\Users<username>"), and cd means "change directory".

Clone the repository by using the command:

git clone https://github.com/AIAANortheastern/GroundStation.git
This creates a folder called "GroundStation" in the current directory. You can change the name of this if you would like.

Go into the GroundStation folder (using cd) and type

git branch
You should see that there is one branch called "master".

Create and switch to a new branch by typing

git checkout -b my_fancy_branch_name
But call it something descriptive for the task you are working on.

Now if you want to commit your changes, you can do the following:

git add .
git commit -m "add xyz, change foo to do bar"
Pushing your changes to your brand new branch is as easy as typing

git push -u origin my_fancy_branch_name
If you are working on a branch with other people, always do a git pull before a git push. After the first push all you need to do is type "git push" to push to github.

Once you've decided that your code is rock solid, and you've tested it extensively, you can issue a pull request, where you'll be asking the other developers to reveiw your code, and if it's up to par they'll merge it either into a larger development branch or master.

Good practices

If you commit something that doesn't compile, I will find you, and I will make you fix it until it does.

Rule #1: Don't merge if it doesn't compile.
Corrolary to Rule #1: Avoid merging if you have compiler warnings.
Rule #2: Don't merge if it doesn't compile.
Naming conventions:



Variables and functions should use the snake_case convention

Class names will have the first letter of each word capitalized: ClassName
