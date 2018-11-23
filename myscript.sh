#  output date
dateString=$(date)
echo $dateString


#  Config variables
readonly CORRECT_SCRIPT_WORKING_PATH=/home/mancar/nespresso
readonly GIT_REPOSITORY_NAME="nespressoAPI"
readonly GIT_CLONE_LINK="git@github.com:ermissa/nespressoAPI.git"
#readonly UPDATE_LOOP_DELAY="60"



#  change pwd to project folder
cd $CORRECT_SCRIPT_WORKING_PATH


#  set remote
git remote set-url origin git@github.com:ermissa/nespressoAPI.git


#  Autofill variables
readonly CORRECT_REPO_PATH="$CORRECT_SCRIPT_WORKING_PATH/$GIT_REPOSITORY_NAME"

#  Meanings of Exit Codes
#1:  Need sudo
#2:  Unable to cd into cloned directory
#3:  CORRECT_SCRIPT_WORKING_PATH is wrong
#4:  Project folder is not a git folder???
#5:  git is not installed
#6:  Unable to cd into cloned directory in infinite loop part
#7:  someone deleted to repo folder while script is running
#and it can not be opened again, probably wrong configs


#  Print some info
echo "Parent path:"$CORRECT_PARENT_PATH
echo
echo "Git repository name:"$GIT_REPOSITORY_NAME
echo
echo "Repository path is:"$CORRECT_REPO_PATH
echo
echo "Git clone url:"$GIT_CLONE_LINK
echo
echo "Infinite loop delay:"$UPDATE_LOOP_DELAY
echo



#  Check if git is installed
git --version > /dev/null
if [ "$?" = "0" ]; then
    #  git is installed
    :
else
    echo "INSTALL GIT FIRST!!!"
    echo "INSTALL GIT FIRST!!!"
    echo "INSTALL GIT FIRST!!!"
    exit 5
fi



#  1-Check if we have sudo permission
#this step is currently skipped, because sudo is bad
if false; then
if [ $(id -u) = "0" ]; then
    #  sudo is on
    :
else
    echo "Script requires super user permissions!"
    exit 1
fi
echo "1 OK"
fi



#  2-Check if the script is running in the correct directory
if [ "$PWD" = $CORRECT_SCRIPT_WORKING_PATH ]; then
    #  Running directory is correct
    #if we can cd into CORRECT_REPO_PATH, this means project is already cloned and we can skip cloning step
    cd $CORRECT_REPO_PATH
    if [ "$?" = "0" ]; then
        #  Project is already cloned
        echo "Project is already cloned, skipping cloning."
    else
        #  Unable to cd into project folder, need to git clone
        echo "Cloning git repository..."
        git clone $GIT_CLONE_LINK
        cd $CORRECT_REPO_PATH
        if [ "$?" = "0" ]; then
            echo "Successfuly entered to repository folder"
        else
            echo "Unable to cd into repository folder, terminating script!(2)"
            exit 2
        fi
    fi
else
    echo "You are running the script from the wrong directory!"
    echo "Correct directory is:"
    echo $CORRECT_SCRIPT_WORKING_PATH
    exit 3
fi
echo "2 OK"



#  3-Check if the folder is a git directory
#  see git rev-parse --help for more details
git rev-parse --is-inside-work-tree
if [ "$?" = "0" ]; then
    #  Working directory is a git repository directory
    echo "This folder is a real git repository folder."
else
    echo "This folder is not a git repository folder!(4)"
    exit 4
fi
echo "3 OK"



#  4-(Constantly) check if repo needs update

#  Check if some crazy person deleted repository folder
if [ -d "$CORRECT_REPO_PATH" ]; then
    #  repo folder still exist
    :
else
    echo $CORRECT_REPO_PATH" is not a valid directory!"
    echo "Going back to parent directory and cloning the project folder again!"
    cd $CORRECT_SCRIPT_WORKING_PATH
    if [ "$?" = "0" ]; then
        git clone $GIT_CLONE_LINK
        cd $CORRECT_REPO_PATH
        if [ "$?" = "0" ]; then
            echo "Successfuly entered to repository folder"
        else
            echo "Unable to cd into repository folder, terminating script!(2)"
            exit 6
        fi
    else
        echo "Script has failed..."
        echo "Make sure config variables are set correctly and run the script again..."
        exit 7
    fi
fi



git remote update
#  Taken from:https://stackoverflow.com/questions/3258243/check-if-pull-needed-in-git
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "Branch is already up to date."
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    echo "Performing a git pull..."
    git pull
fi

