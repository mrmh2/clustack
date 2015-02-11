#export PATH=$PWD/bin:$PWD/scripts:$PATH
#PS1="(cs) "$PS1
#export CLUSTACK_ROOT=`pwd`

MYDIR=$BASH_SOURCE

if [ $MYDIR == '.' ]; then
    MY_PATH=`pwd`
else
    MY_PATH=`pwd`/$MYDIR
fi

export CLUSTACK_ROOT=`dirname $MY_PATH`
PATH=$CLUSTACK_ROOT/bin:$PATH
PS1="(cs) "$PS1
